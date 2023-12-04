include "globals.mzn";

%rectangles par shapes, les indices des rectangles par shape
%offset des rectangles 
%grosseur des rectangles
%liste qui associe chaque rectangles avec une liste de coordonnées de perimetre on peu se servir de la liste de shape pour faiore le check
%pour l'overlap on utilise geost

%constantes
int: nShapes;
int: lastRectangleIndex = sum(rectanglesCountPerShape)+1;
set of int: SHAPES = 1..nShapes;
set of int: SURFACE = 0..max(surfacePerShape);
set of int: RECTANGLES = 1..lastRectangleIndex;
array[SHAPES] of int :   surfacePerShape;
array[SHAPES] of int :   rectanglesCountPerShape;
array[DIMENSIONS] of int : boundingBox;
set of int: DIMENSIONS = 1..2;
set of int: RECTPERSHAPE  = 1..max(rectanglesCountPerShape);
set of int: OFFSET = 0..max(boundingBox);

%variables
var 1..lastRectangleIndex-1: rectanglesCount;
array[RECTANGLES,DIMENSIONS] of var SURFACE:  rect_size;
array[RECTANGLES,DIMENSIONS] of var OFFSET:  rect_offset;
array[RECTANGLES,DIMENSIONS] of var OFFSET:  real_rect_offset;
array[SHAPES,RECTPERSHAPE] of var RECTANGLES:   shape;
% 4 valeurs, 2 premieres = ranges de x, 2 dernieres range de y pour les valeurs de perimetre. y est avec un x au debut ou a la fin du rect. x est avec le y du dessus ou du dessous du rect
array[RECTANGLES,1..4] of var int: rect_edges;%jsais pas si cest une bonne idee dutiliser SURFACE
var OFFSET: min_offset = min(i in 1..rectanglesCount, j in DIMENSIONS)(rect_offset[i, j]);
%array[RECTANGLES,1..4] of  var OFFSET: rect;%1,2 size 3,4 offset
%contraintes

constraint forall (i in SHAPES)(forall (j in RECTPERSHAPE)(if j<= rectanglesCountPerShape[i] then shape[i,j] <=rectanglesCount
else shape[i,j]== lastRectangleIndex endif));

constraint forall(i in RECTANGLES)(if i <= rectanglesCount then rect_size[i,1]>0 /\ rect_size[i,2]>0 /\ i in shape[SHAPES,RECTPERSHAPE]else rect_size[i,1]==0 /\ rect_size[i,2]==0 endif);

constraint forall (i in SHAPES)(sum(j in 1..rectanglesCountPerShape[i])(rect_size[shape[i,j],1]*rect_size[shape[i,j],2]) == surfacePerShape[i]);

constraint forall(i in SHAPES)(diffn_nonstrict_k(
array2d(1..rectanglesCountPerShape[i],DIMENSIONS,[rect_offset[shape[i, j], k] | j in 1..rectanglesCountPerShape[i], k in DIMENSIONS]),array2d(1..rectanglesCountPerShape[i],DIMENSIONS,[rect_size[shape[i, j], k] | j in 1..rectanglesCountPerShape[i], k in DIMENSIONS])));

constraint forall(i in RECTANGLES)(rect_edges[i,1]==rect_offset[i,1] /\ rect_edges[i,2]==rect_offset[i,1] + rect_size[i,1] 
/\ rect_edges[i,3]== rect_offset[i,2] /\ rect_edges[i,4]==rect_offset[i,2] + rect_size[i,2]);

constraint forall(i in SHAPES)(if rectanglesCountPerShape[i] >1 then forall(j in 2..rectanglesCountPerShape[i])(
  count(k in 1..(j-1))((rect_edges[shape[i,j],1]<rect_edges[shape[i,k],2] /\ rect_edges[shape[i,j],2]>rect_edges[shape[i,k],1] 
  /\ (rect_edges[shape[i,j],3] == rect_edges[shape[i,k],4]\/rect_edges[shape[i,j],4] == rect_edges[shape[i,k],3]))
  \/(rect_edges[shape[i,j],3]<rect_edges[shape[i,k],4] /\ rect_edges[shape[i,j],4]>rect_edges[shape[i,k],3] 
  /\ (rect_edges[shape[i,j],1] == rect_edges[shape[i,k],2]\/rect_edges[shape[i,j],2] == rect_edges[shape[i,k],1])) )>=1) endif);
 
 
%constraint forall(i in RECTANGLES)(forall(j in DIMENSIONS)(rect[i,j]==rect_size[i,j] /\ rect[i,j+2]==rect_offset[i,j]));
constraint forall(i in 1..rectanglesCount-1)(count(j in i+1..rectanglesCount)(rect_size[i,DIMENSIONS]==rect_size[j,DIMENSIONS]/\ 
rect_offset[i,DIMENSIONS]==rect_offset[j,DIMENSIONS])==0);
 
constraint forall(i in 1..rectanglesCount)(forall(j in DIMENSIONS)(real_rect_offset[i,j] = rect_offset[i,j]-min_offset));

solve satisfy;