"""
Kolbe Yang
This file draws the 27 squares of color on the cube's 3 faces
"""

import pygame
from pygame.locals import *

colors = [
    [215,193,162],#white
    [96,156,93],#green
    [186,96,64],#red
    [210,178,66],#yellow
    [101,128,135],#blue
    [205,130,77]#orange
]

u_coordinates_raw = "(177, 228)\
(211, 200)\
(258, 173)\
(300, 152)\
(218, 251)\
(252, 220)\
(300, 194)\
(351, 171)\
(260, 277)\
(303, 248)\
(351, 222)\
(394, 202)\
(300, 299)\
(344, 277)\
(389, 251)\
(433, 230)"

l_coordinates_raw = "(173, 379)\
(168, 328)\
(169, 277)\
(176, 229)\
(210, 406)\
(211, 358)\
(213, 308)\
(218, 256)\
(255, 434)\
(255, 384)\
(255, 333)\
(260, 280)\
(303, 449)\
(302, 402)\
(300, 353)\
(301, 303)"

f_coordinates_raw = "(300, 300)\
(345, 276)\
(391, 253)\
(433, 230)\
(303, 351)\
(352, 326)\
(395, 303)\
(438, 277)\
(300, 401)\
(352, 377)\
(394, 352)\
(439, 325)\
(303, 451)\
(346, 436)\
(394, 407)\
(432, 374)"

def parse_coordinates(coordinates_raw):
    """
    Parses the coordinates of a given face
    :param coordinates_raw: the raw coordinates from above
    :return: A 4x4 array made from the coordinates
    """
    coordinates_raw = coordinates_raw[1: len(coordinates_raw) - 1 ]
    coordinates_raw = coordinates_raw.replace(" ", "")
    coordinates_raw = coordinates_raw.split(")(")

    count = 0
    output = []
    for row in range(4):
        coordinate_row = []
        for col in range(4):
            pair = []
            coordinates_string = coordinates_raw[count].split(",")
            for string in coordinates_string:
                pair.append(int(string))
            count += 1
            coordinate_row.append(pair)
        output.append(coordinate_row)

    return output

#parse all three arrays
u_coordinate_array = parse_coordinates(u_coordinates_raw)
l_coordinate_array = parse_coordinates(l_coordinates_raw)
f_coordinate_array = parse_coordinates(f_coordinates_raw)

def draw_cube(u_face, l_face, f_face, SCREEN):
    """
    Draws the cube given all three faces
    :param u_face: a 3x3 array of the top face
    :param l_face: a 3x3 array of the left face
    :param f_face: a 3x3 array of the right (front) face
    :param SCREEN: the pygame SCREEN to blit onto
    :return: None
    """
    faces = [ u_face, l_face, f_face ]
    coordinate_arrays = [ u_coordinate_array, l_coordinate_array, f_coordinate_array ]

    for i in range(3):
        face = faces[i]
        coordinate_array = coordinate_arrays[i]
        for row in range(3):
            for col in range(3):
                colorcode = face[row][col]
                color = colors[colorcode]

                points = []
                points.append(coordinate_array[row][col])
                points.append(coordinate_array[row][col + 1])
                points.append(coordinate_array[row + 1][col + 1])
                points.append(coordinate_array[row + 1][col])
                pygame.draw.polygon(SCREEN, color, points)


