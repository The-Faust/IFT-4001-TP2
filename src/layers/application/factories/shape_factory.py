from typing import List, Set


class ShapeFactory:
    def remove_duplicates(
        self,
        rect_size: List[List[int]],
        rect_offset: List[List[int]],
        shapes: List[List[int]],
        valid_shapes: List[List[int]]
    ):
        rect_to_delete: List[int] = []

        # TODO: This is .... not good we probably should try to refactor this so that there are less loops...
        for i in range(len(rect_size)-1):
            for j in range(i + 1, len(rect_size)):
                if i not in rect_to_delete and j not in rect_to_delete:
                    if rect_size[i] == rect_size[j] and rect_offset[i] == rect_offset[j]:
                        rect_to_delete.append(j)
                        for k in range(len(shapes)):
                            for l in range(len(shapes[k])):
                                if shapes[k][l] == j + 1:
                                    shapes[k][l] = i + 1

        rect_to_delete.sort(reverse=True)
        for i in rect_to_delete:
            # TODO: Duplication de code ne devrait pas exister
            for j in range(len(shapes)):
                for k in range(len(shapes[j])):
                    if shapes[j][k] > i+1:
                        shapes[j][k] -=1

            rect_size.pop(i)
            rect_offset.pop(i)


        shape_to_delete: List[int] = []
        for i in range(len(shapes) - 1):
            for j in range(i + 1, len(shapes)):
                if i not in shape_to_delete and j not in shape_to_delete:
                    if shapes[i] == shapes[j]:
                        # TODO: Duplication de code ne devrait pas exister
                        shape_to_delete.append(j)

                        for k in range(len(valid_shapes)):
                            for l in range(len(valid_shapes[k])):
                                if (valid_shapes[k])[l] == j + 1:
                                    valid_shapes[k][l] = i + 1

        shape_to_delete.sort(reverse=True)
        for i in shape_to_delete:
            # TODO: Duplication de code ne devrait pas exister
            for j in range(len(valid_shapes)):
                for k in range(len(valid_shapes[j])):
                    if valid_shapes[j][k] > i+1:
                        valid_shapes[j][k] -=1

            shapes.pop(i)

    # Pourquoi on ne gère pas tout ça dans le modèle?
    def rotate_shapes(
        self,
        rect_size: List[List[int]],
        rect_offset: List[List[int]],
        shape: List[List[int]],
        valid_shapes: List[List[int]]
    ):
        initial_len: int = len(shape)
        for i in range(initial_len):

            if len(shape[i]) > 1:
                # ordre -> sens horaire
                x_max: int = rect_size[shape[i][0] - 1][0] + rect_offset[shape[i][0] - 1][0]
                y_max: int = rect_size[shape[i][0] - 1][1] + rect_offset[shape[i][0] - 1][1]
                new_shapes: List[List[int]] = [[], [], []]

                for j in range(1, len(shape[i])):
                    x: int = rect_size[shape[i][j] - 1][0] + rect_offset[shape[i][j] - 1][0]
                    y: int = rect_size[shape[i][j] - 1][1] + rect_offset[shape[i][j] - 1][1]
                    if x > x_max: x_max = x
                    if y > y_max: y_max = y

                for j in range(len(shape[i])):
                    current_rect: int = shape[i][j] - 1
                    inverted_x: int = x_max - (rect_offset[current_rect][0] + rect_size[current_rect][0])
                    inverted_y: int = y_max - (rect_offset[current_rect][1] + rect_size[current_rect][1])

                    # rot1
                    new_shapes[0].append(self.add_rectangle([rect_size[current_rect][1], rect_size[current_rect][0]],
                                                        [rect_offset[current_rect][1], inverted_x], rect_size,
                                                        rect_offset))

                    # rot2
                    new_shapes[1].append(self.add_rectangle(rect_size[current_rect],
                                                        [inverted_x, inverted_y], rect_size, rect_offset))

                    # rot3
                    new_shapes[2].append(self.add_rectangle([rect_size[current_rect][1], rect_size[current_rect][0]],
                                                        [inverted_y, rect_offset[current_rect][0]], rect_size,
                                                        rect_offset))

                for j in range(3): valid_shapes[i].append(self.add_shape(shape, new_shapes[j]))



            elif rect_size[shape[i][0] - 1][1] != rect_size[shape[i][0] - 1][0]:
                valid_shapes[i].append(self.add_shape(shape, [
                    self.add_rectangle([rect_size[shape[i][0] - 1][1], rect_size[shape[i][0] - 1][0]],
                                       [0, 0], rect_size, rect_offset, True)]))


    def add_rectangle(
        self,
        size: List[int],
        offset: List[int],
        rect_size: List[List[int]],
        rect_offset: List[List[int]],
        size_only: bool = False
    ) -> int:
        if size_only:
            for i in range(len(rect_size)):
                if rect_size[i] == size:
                    return i + 1

        else:
            for i in range(len(rect_size)):
                if rect_size[i] == size and rect_offset[i] == offset:
                    return i + 1

        rect_size.append(size)
        rect_offset.append(offset)

        return len(rect_size)

    def add_shape(self, shape: List[List[int]], new_shape: List[int]) \
            -> int:
        for i in range(len(shape)):
            if shape[i] == new_shape: return i + 1

        shape.append(new_shape)

        return len(shape)
