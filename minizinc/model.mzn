include "globals.mzn";
include "data1.dzn";
%le dernier objet dans valid_shapes doit correspondre à un rectangle vide.
%valid_shapes contient l'ensemble des rotations possibles pour un objet, les objets sont ordonnés du plus grand au plus petit.
%c'est plus optimal d'avoir le minimum de rectangles

% constantes
int: k;
int: nObjects;
int: nRectangles;
int: nShapes; 

set of int: DIMENSIONS = 1..k;
set of int: OBJECTS    = 1..nObjects;
set of int: RECTANGLES = 1..nRectangles;
set of int: SHAPES     = 1..nShapes;

array[DIMENSIONS] of int:             l;
array[DIMENSIONS] of int:             u;
array[RECTANGLES,DIMENSIONS] of int:  rect_size;
array[RECTANGLES,DIMENSIONS] of int:  rect_offset;
array[SHAPES] of set of RECTANGLES:   shape;
array[OBJECTS] of set of SHAPES: valid_shapes;
 %variables
array[OBJECTS,DIMENSIONS] of var int: x;
array[OBJECTS] of var SHAPES:         kind;
array[OBJECTS] of var OBJECTS: chosen_objects;
var 0..nObjects : chosen_objects_count; 
var 0..(u[1]-l[1])*(u[2]-l[2]) : surface;

%contraintes
constraint if chosen_objects_count < nObjects then forall(i in chosen_objects_count +1 ..nObjects )(chosen_objects[i]=nObjects) endif;
constraint all_different_except(chosen_objects,nObjects..nObjects);
constraint forall (obj in OBJECTS) (
    if(obj >chosen_objects_count) then kind[obj] = nShapes else kind[obj] in valid_shapes[chosen_objects[obj]] /\ not(kind[obj]==nShapes) endif 
);
constraint geost_bb(k,rect_size,rect_offset,shape,x,kind,l,u);

constraint surface = sum(i in 1..nObjects, j in 1..length(shape[valid_shapes[i][1]]))(if i in chosen_objects then 
rect_size[shape[valid_shapes[i][1]][j], 1]*rect_size[shape[valid_shapes[i][1]][j], 2] else 0 endif);

constraint increasing(chosen_objects);
constraint (x[1,1]<= ceil(l[1]/2) /\ x[1,2]<= ceil(u[1]/2));

%constraint x[1,1]<= ceil((u[1]-l[1])/2) /\ x[1,2]<= ceil((u[2]-l[2])/2);

solve :: int_search(chosen_objects, smallest, indomain_min  , complete) maximize surface;