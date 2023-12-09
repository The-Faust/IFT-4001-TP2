from typing import List, Set


class ShapeFactory:
    # Pourquoi on ne gère pas tout ça dans le modèle?
    def remove_duplicates(
        self,
        rect_size: List[List[int]],
        rect_offset: List[List[int]],
        shapes: [{int}],
        valid_shapes: [{int}]
    ):
        """

        Args:
            rect_size:
            rect_offset:
            shapes:
            valid_shapes:

        Returns:

        """
        shapes = [list(shape) for shape in shapes]
        rect_to_delete: List[int] = []

        # TODO: This is .... not good we probably should try to refactor this so that there are less loops...
        for i in range(len(rect_size)-1):
            for j in range(i + 1, len(rect_size)):
                if i not in rect_to_delete and j not in rect_to_delete:
                    if rect_size[i] == rect_size[j] and rect_offset[i] == rect_offset[j]:
                        rect_to_delete.append(j)
                        for k in range(len(shapes)):
                            for l in range(len(shapes[k])):
                                if list(shapes[k])[l] == j + 1:
                                    shapes[k][l] = i + 1

        rect_to_delete.sort(reverse=True)
        for i in rect_to_delete:
            # TODO: Duplication de code ne devrait pas exister
            for j in range(len(shapes)):
                for k in range(len(shapes[j])):
                    if list(shapes[j])[k] > i+1:
                        shapes[j][k] -=1

            rect_size.pop(i)
            rect_offset.pop(i)

        for i in range(len(shapes)):
            shapes[i] = set(shapes[i])

        for i in range(len(valid_shapes)):
            valid_shapes[i] = list(valid_shapes[i])

        shape_to_delete: List[int] = []
        for i in range(len(shapes) - 1):
            for j in range(i + 1, len(shapes)):
                if i not in shape_to_delete and j not in shape_to_delete:
                    if shapes[i] == shapes[j]:
                        # TODO: Duplication de code ne devrait pas exister
                        shape_to_delete.append(j)

                        for k in range(len(valid_shapes)):
                            for l in range(len(valid_shapes[k])):
                                if list(valid_shapes[k])[l] == j + 1:
                                    valid_shapes[k][l] = i + 1

        shape_to_delete.sort(reverse=True)
        for i in shape_to_delete:
            # TODO: Duplication de code ne devrait pas exister
            for j in range(len(valid_shapes)):
                for k in range(len(valid_shapes[j])):
                    if list(valid_shapes[j])[k] > i+1:
                        valid_shapes[j][k] -=1

            shapes.pop(i)

        for i in range(len(valid_shapes)):
            valid_shapes[i] = set(valid_shapes[i])

    # Pourquoi on ne gère pas tout ça dans le modèle?
    def rotate_shapes(
        self,
        shape: [{int}],
        rect_size: List[List[int]],
        rect_offset: List[List[int]],
        valid_shapes: [{int}]
    ):
        initial_len: int = len(shape)
        for i in range(initial_len):

            if len(shape[i]) > 1:
                # ordre -> sens horaire
                x_max: int = rect_size[list(shape[i])[0] - 1][0] + rect_offset[list(shape[i])[0] - 1][0]
                y_max: int = rect_size[list(shape[i])[0] - 1][1] + rect_offset[list(shape[i])[0] - 1][1]
                new_shapes: List[Set[int]] = [set(), set(), set()]

                for j in range(1, len(shape[i])):
                    x: int = rect_size[list(shape[i])[j] - 1][0] + rect_offset[list(shape[i])[j] - 1][0]
                    y: int = rect_size[list(shape[i])[j] - 1][1] + rect_offset[list(shape[i])[j] - 1][1]
                    if x > x_max: x_max = x
                    if y > y_max: y_max = y

                for j in range(len(shape[i])):
                    current_rect: int = list(shape[i])[j] - 1
                    inverted_x: int = x_max - (rect_offset[current_rect][0] + rect_size[current_rect][0])
                    inverted_y: int = y_max - (rect_offset[current_rect][1] + rect_size[current_rect][1])


                    # rot1
                    new_shapes[0].add(self.add_rectangle([rect_size[current_rect][1], rect_size[current_rect][0]],
                                                        [rect_offset[current_rect][1], inverted_x], rect_size,
                                                        rect_offset))

                    # rot2
                    new_shapes[1].add(self.add_rectangle(rect_size[current_rect],
                                                        [inverted_x, inverted_y], rect_size, rect_offset))

                    # rot3
                    new_shapes[2].add(self.add_rectangle([rect_size[current_rect][1], rect_size[current_rect][0]],
                                                        [inverted_y, rect_offset[current_rect][0]], rect_size,
                                                        rect_offset))

                for j in range(3): valid_shapes[i].add(self.add_shape(shape, new_shapes[j]))



            elif rect_size[list(shape[i])[0] - 1][1] != rect_size[list(shape[i])[0] - 1][0]:
                valid_shapes[i].add(self.add_shape(shape, {
                    self.add_rectangle([rect_size[list(shape[i])[0] - 1][1], rect_size[list(shape[i])[0] - 1][0]],
                                       [0, 0], rect_size, rect_offset, True)}))

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

    def add_shape(self, shape: [{int}], new_shape: {int}) \
            -> int:
        for i in range(len(shape)):
            if shape[i] == new_shape: return i + 1

        shape.append(new_shape)

        return len(shape)
