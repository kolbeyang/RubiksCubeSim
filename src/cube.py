
"""
Cube's faces are coded like this
0 0 0
0 0 0  white
0 0 0
1 1 1 2 2 2
1 1 1 2 2 2  green red
1 1 1 2 2 2
      3 3 3 4 4 4
      3 3 3 4 4 4   yellow blue
      3 3 3 4 4 4
            5 5 5
            5 5 5    orange
            5 5 5

facecodes are integers (0-5) associated with each face
They are used to index the faces array.
"""

import random

#represents a single Rubik's Cube
class Cube():
    WHITE = 0
    GREEN = 1
    RED = 2
    YELLOW = 3
    BLUE = 4
    ORANGE = 5

    face_symbols = {"U":0, "F":1, "R":2, "D":3, "B":4, "L":5}

    def __init__(self):
        """
        initializes the cube, creates 3D list to represent all the colors
        self.faces is list of 3x3 arrays
        initializes the orientation to have white on top and green in front
        """
        #initialize the main data structure
        self.faces = []
        for color in range(6):
            face = []
            for _ in range(3):
                face.append([color, color, color])
            self.faces.append(face)

        self.orientation = [Cube.WHITE, Cube.GREEN, Cube.RED, Cube.YELLOW, Cube.BLUE, Cube.ORANGE]
        self.orientation_offset = [0,0,0,0,0,0]

    def get_face_for_display(self, relative_facecode):
        """
        Returns a 3x3 array reprenting a specific face
        This method rotates the array so that it will display correctly
        :param relative_facecode: The relative facecode of the face to display, U,F,R,etc.
        :return: A 3x3 Array of colorcodes to display
        """
        absolute_facecode = self.orientation[relative_facecode]
        output = self.faces[absolute_facecode]
        offset = self.orientation_offset[absolute_facecode]
        for _ in range(offset):
            output = self._rotate_3x3_array(output, 1)

        return output

    def x_rotation(self, direction):
        """
        Rotate the cube "forward"
        all elements of the self.orientation list must change except for R and L (indices 2 and 5)
        :param direction: the direction to rotate the cube in, 1 for forward, -1 for backward
        :return: None
        """
        indices = [0,4,3,1]
        if direction == 1: #clockwise
            offsets = [-1,0,1,1,0,-1]
        else: #counterclockwise
            offsets = [0,-1,-1,0,1,1]
        self.cube_rotation(indices, direction, offsets)

    def y_rotation(self, direction):
        """
        Rotate the cube right
        :param direction: the direction to rotate the cube in, 1 for right, -1 for left
        :return: None
        """
        indices = [1,2,4,5]
        if direction == 1: #clockwise
            offsets =[-1,0,1,1,0,-1]
        else: #counterclockwise
            offsets = [1,1,0,-1,-1,0]
        self.cube_rotation(indices, direction, offsets)

    def z_rotation(self, direction):
        """
        Rotate the cube clockwise
        :param direction: the direction to rotate the cube in, 1 for CW, -1 for CCW
        :return: None
        """
        indices = [0,2,3,5]
        if direction == 1: #clockwise
            offsets = [1,1,0,-1,-1,0]
        else: #counterclockwise
            offsets = [0,-1,-1,0,1,1]
        self.cube_rotation(indices, direction, offsets)

    def cube_rotation(self, indices, direction, offsets):
        """
        This methods rotates the entire cube "in hand"
        This method is called by the x_rotation, y_rotation, and z_rotation methods
        This does not actually affect the state of the cube, just its orientation
        In any given rotation, only 4 faces change in the orientation array
        These are given in order by the indices array
        :param indices: An array of relative facecodes
        :param direction: The direction to rotate in
        :param offsets: The change in offsets associated with a given rotation
        :return: None
        """
        #handle offsets
        for i in range(6):
            #facecode of the face at the orientation i, (U,F,R,D,B,L)
            facecode = self.orientation[i]
            current_offset = self.orientation_offset[facecode]
            delta_offset = offsets[i]
            #print("cube_rotation: facecode", facecode, "current_offset", current_offset, "delta_offset", delta_offset)
            self.orientation_offset[facecode] = (current_offset + delta_offset) % 4

        #print("cube_rotation: offests", self.orientation_offset)

        if direction == -1:
            temp = self.orientation[indices[0]]
            for i in range(len(indices) - 1):
                current_index = indices[i]
                next_index = indices[i+1]
                self.orientation[current_index] = self.orientation[next_index]
            self.orientation[indices[3]] = temp
        elif direction == 1:
            temp = self.orientation[indices[3]]
            for i in range(len(indices) - 1, 0, -1):
                current_index = indices[i]
                next_index = indices[i-1]
                self.orientation[current_index] = self.orientation[next_index]
            self.orientation[indices[0]] = temp

        else:
            raise("cube_rotation: invalid direction")

    def facecode_of_face_in_direction(self, source_facecode, direction):
        """
        Returns the facecode of the face in the given direction from the source face
        the direction (0-3) specifies directions clockwise (up, right, down, left)
        :param source_facecode: the facecode of the source face
        :param direction: the direction (0-3) from the source face
        :return: the facecode of the face in the given direction from the source face
        """
        difference = 0

        if source_facecode%2 == 0:
            #even
            if direction == 0: #up
                difference = 4
            elif direction == 1: #right
                difference = 2
            elif direction == 2: #down
                difference = 1
            elif direction == 3: #left
                difference = 5
        else:
            #odd
            if direction == 0: #up
                difference = 5
            elif direction == 1: #right
                difference = 1
            elif direction == 2: #down
                difference = 2
            elif direction == 3: #left
                difference = 4

        return (source_facecode + difference) % 6

    def translate_direction(self, source_facecode, direction):
        """
        The border face is the face bordering the source face in the given direction
        in what direction does the source face border the border face?
        No need to actually access the border face, a simple formula can compute this
        :param source_facecode: the facecode of the source face
        :param direction: the direction of the border face from the source face
        :return: the direction of the source face from the border face
        """
        if source_facecode % 2 == 0:
            #even
            if direction == 0 or direction == 3:
                return 1
            elif direction == 1 or direction == 2:
                return 0
        else:
            #odd
            if direction == 0 or direction == 3:
                return 2
            elif direction == 1 or direction == 2:
                return 3

        return -1

    def get_indices(self, direction):
        """
        gets the indices of the three cells in the given direction
        For example, if the direction is up (0), this method will return the
        upper left [0,0], upper center [0,1], and upper right [0,2]
        :param direction: the direction from center of indices to return
        :return: a list of [row, col] coordinates in clockwise order
        """
        row_indices = [0,0,0]
        col_indices = [0,0,0]

        if direction == 0:
            #top
            row_indices = [0,0,0]
            col_indices = [0,1,2]
        elif direction == 1:
            #right
            row_indices = [0,1,2]
            col_indices = [2,2,2]
        elif direction == 2:
            #bottom
            row_indices = [2,2,2]
            col_indices = [2,1,0]
        elif direction == 3:
            #left
            row_indices = [2,1,0]
            col_indices = [0,0,0]

        output = []
        for i in range(3):
            output.append([row_indices[i], col_indices[i]])

        return output

    def get_border(self, rotate_facecode, direction):
        """
        Returns the three squares on face_2 that border the rotate_face
        :param rotate_facecode: the facecode of the face to rotate
        :param direction: the direction to rotate in, 1 for CW and -1 for CCW
        :return: an array of the 3 symbols that border the rotate face at the given direction
        """
        #what is the face bordering in the given direction?
        border_facecode = self.facecode_of_face_in_direction(rotate_facecode, direction)
        border_face = self.faces[border_facecode]

        #what side of this bordering face does the rotating face make contact with?
        #the rotate_face touches the border face at this side on the border face
        source_direction = self.translate_direction(rotate_facecode, direction)

        indices = self.get_indices(source_direction)

        output = [0,0,0]
        for i in range(3):
            coordinates = indices[i]
            output[i] = border_face[coordinates[0]][coordinates[1]]

        return output

    def set_border(self, rotate_facecode, direction, colors):
        """
        Sets the three symbols at the (direction)ward border of rotate face using the given colors
        :param rotate_facecode: the facecode of the face to rotate
        :param direction: the direction of the border to set
        :param colors: a list of colorcodes to set the border to
        :return: None
        """
        #what is the face bordering in the given direction?
        border_facecode = self.facecode_of_face_in_direction(rotate_facecode, direction)
        border_face = self.faces[border_facecode]

        #what side of this bordering face does the rotating face make contact with?
        #the rotate_face touches the border face at this side on the border face
        source_direction = self.translate_direction(rotate_facecode, direction)

        indices = self.get_indices(source_direction)

        for i in range(3):
            coordinates = indices[i]
            border_face[coordinates[0]][coordinates[1]] = colors[i]

    def _rotate_3x3_array(self, old_face, rot_direction):
        """
        Rotates the 9 symbols within the 3x3 face array
        :param facecode: the facecode of the face to rotate
        :param rot_direction: the direction to rotate in, 1 for CW, -1 for CCW
        :return: None
        """
        new_face = []
        for i in range(len(old_face)):
            new_row = []
            for j in range(len(old_face[0])):
                new_row.append(-1)
            new_face.append(new_row)

        if rot_direction == 1:
            #clockwise
            for new_row_index in range(len(new_face)):
                for new_col_index in range(len(new_face[0])):
                    old_row_index = 2 - new_col_index
                    old_col_index = new_row_index
                    new_face[new_row_index][new_col_index] = old_face[old_row_index][old_col_index]

            return new_face
        elif rot_direction == -1:
            #counterclockwise
            for new_row_index in range(len(new_face)):
                for new_col_index in range(len(new_face[0])):
                    old_row_index = new_col_index
                    old_col_index = 2 - new_row_index
                    new_face[new_row_index][new_col_index] = old_face[old_row_index][old_col_index]

            return new_face

        raise("_rotate_face: invalid rotation direction")

    def scramble(self):
        """
        Scrambles the cube,
        Applies 20 random moves
        :return: None
        """
        moves = ["U", "F", "R", "D", "B", "L"]
        direction = ["", "\'"]

        for _ in range(20):
            notation = moves[random.randint(0,5)] + direction[random.randint(0,1)]
            self.parse_move_notation(notation)

    def rotate(self, facecode, rot_direction):
        """
        Handles all transformatinos to rotate the given face in the given direction
        :param facecode: the facecode of the face to rotate
        :param rot_direction: the rotation direction, 1 for CW, -1 for CCW
        :return: None
        """
        borders = []
        for i in range(4):
            borders.append(self.get_border(facecode, i))


        if rot_direction == 1:
            #clockwise
            border = borders.pop(3)
            borders.insert(0, border)
        else:
            #counterclockwise
            border = borders.pop(0)
            borders.append(border)


        for i in range(4):
            self.set_border(facecode, i, borders[i])

        self.faces[facecode] = self._rotate_3x3_array(self.faces[facecode], rot_direction)

    def color_from_number(self, colorcode):
        """
        Used in the to_string to convert colorcodes to characters
        :param colorcode: the colorcode to find the color for
        :return: a length one string representing the color
        """
        color_list = ["w", "g", "r", "y", "b", "o"]
        return color_list[colorcode]

    def parse_move_notation(self, string):
        """
        Takes a string in 3x3 cube move notation,
        parses the string,
        applies the given transformations to the cube
        :param string: a string of 3x3 moves in notation
        :return: None
        """
        moves = string.split(" ")

        for move in moves:
            side = move[0] #ex. R or U or L
            relative_facecode = Cube.face_symbols[side] #0-5
            absolute_facecode = self.orientation[relative_facecode] #0-5 specifies exactly which color

            direction = 1
            iterations = 1
            if len(move) > 1:
                if move[1] == "\'":
                    direction = -1
                elif move[1] == "2":
                    iterations = 2

            for _ in range(iterations):
                self.rotate(absolute_facecode, direction)

    def to_string(self):
        """
        :return: The cube net as a string
        """


        map = [
             [0, -1, -1],
             [1, 2, -1],
            [-1, 3, 4],
            [-1,-1, 5]
        ]

        output_rows = []
        #initialize
        for i in range(len(map) * 3):
            row = []
            for i in range(len(map[0]) * 3):
                row.append(" ")
            output_rows.append(row)

        for i in range(len(map)):
            row = map[i]
            for j in range(len(map[0])):
                if row[j] == -1:
                    facecode = -1
                else:
                    facecode = row[j]
                base_row = i*3
                base_col = j*3

                if facecode != -1:
                    #nonempty
                    for r in range(3):
                        for c in range(3):
                            output_rows[base_row + r][base_col + c] = self.color_from_number(self.faces[facecode][r][c])


        #join everything in the row
        for i in range(len(output_rows)):
            output_rows[i] = " ".join(output_rows[i])

        return "\n".join(output_rows)




        return output


