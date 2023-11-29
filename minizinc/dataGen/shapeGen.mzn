include "globals.mzn";
include "testData.dzn";
%rectangles par shapes, les indices des rectangles par shape
%offset des rectangles 
%grosseur des rectangles
%liste qui associe chaque rectangles avec une liste de coordonnées de perimetre on peu se servir de la liste de shape pour faiore le check
%pour l'overlap on utilise geost

%constantes
int: nShapes;
int: dimensions;
set of int: SHAPES = 1..nShapes;
set of int: SURFACE = 0..max(surfacePerShape);
set of int: RECTANGLES = 1..sum(rectanglesCountPerShape)+1;
array[SHAPES] of int :   surfacePerShape;
array[SHAPES] of int :   rectanglesCountPerShape;
set of int: DIMENSIONS = 1..dimensions;
set of int: RECTPERSHAPE  = 1..max(rectanglesCountPerShape);

%variables
array[RECTANGLES,DIMENSIONS] of var SURFACE:  rect_size;
array[RECTANGLES,DIMENSIONS] of var int:  rect_offset;
array[SHAPES,RECTPERSHAPE] of var RECTANGLES:   shape;
% 4 valeurs, 2 premieres = ranges de x, 2 dernieres range de y pour les valeurs de perimetre. y est avec un x au debut ou a la fin du rect. x est avec le y du dessus ou du dessous du rect
array[RECTANGLES,1..4] of var SURFACE: rect_edges;%jsais pas si cest une bonne idee dutiliser SURFACE

%contraintes
constraint forall (i in SHAPES)(forall (j in RECTPERSHAPE)(if j<= rectanglesCountPerShape[i] then rect_size[shape[i,j],1]>=1 /\rect_size[shape[i,j],2]>=1 
else rect_size[shape[i,j],1]==0 /\rect_size[shape[i,j],2]==0 endif));

constraint forall(i in RECTANGLES)(if i < sum(rectanglesCountPerShape)+1 then rect_size[i,1]>0 /\ rect_size[i,2]>0 else rect_size[i,1]==0 /\ rect_size[i,2]==0 endif);


constraint forall (i in SHAPES)(sum(j in 1..rectanglesCountPerShape[i])(rect_size[shape[i,j],1]*rect_size[shape[i,j],2]) == surfacePerShape[i]);

constraint forall(i in SHAPES)(diffn_nonstrict_k(
array2d(1..rectanglesCountPerShape[i],1..2,[rect_offset[shape[i, j], k] | j in 1..rectanglesCountPerShape[i], k in 1..2]),array2d(1..rectanglesCountPerShape[i],1..2,[rect_size[shape[i, j], k] | j in 1..rectanglesCountPerShape[i], k in 1..2])));

constraint forall(i in RECTANGLES)(rect_edges[i,1]==rect_offset[i,1] /\ rect_edges[i,2]==rect_offset[i,1] + rect_size[i,1] 
/\ rect_edges[i,3]== rect_offset[i,2] /\ rect_edges[i,4]==rect_offset[i,2] + rect_size[i,2]);

constraint forall(i in SHAPES)(if rectanglesCountPerShape[i] >1 then forall(j in 2..rectanglesCountPerShape[i])(
  count(k in 1..(j-1))((rect_edges[shape[i,j],1]<rect_edges[shape[i,k],2] /\ rect_edges[shape[i,j],2]>rect_edges[shape[i,k],1] 
  /\ (rect_edges[shape[i,j],3] == rect_edges[shape[i,k],4]\/rect_edges[shape[i,j],4] == rect_edges[shape[i,k],3]))
  \/(rect_edges[shape[i,j],3]<rect_edges[shape[i,k],4] /\ rect_edges[shape[i,j],4]>rect_edges[shape[i,k],3] 
  /\ (rect_edges[shape[i,j],1] == rect_edges[shape[i,k],2]\/rect_edges[shape[i,j],2] == rect_edges[shape[i,k],1])) )>=1) endif);
  
 %constraint forall(i in SHAPES)(rect_offset[shape[i,1],1]==0 /\ rect_offset[shape[i,2],2]==0);
  
solve satisfy;