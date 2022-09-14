"""
@author Kolbe Yang
This file will display the Cube in a new Window
"""

import pygame
import cube
import sys
import cubeDrawer
from pygame.locals import *
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#Screen Dimensions
SCREENWIDTH = 600
SCREENHEIGHT = 600

#Initialize Window
pygame.init()
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption("Lil\' Cube")

#Put all images into a dictionary
images = {}
images["background"] = pygame.image.load("../images/background.PNG")
images["frame"] = pygame.image.load("../images/frame.PNG")
images["leftArrows"] = pygame.image.load("../images/leftArrows.PNG")
images["rightArrows"] = pygame.image.load("../images/rightArrows.PNG")
images["shadow"] = pygame.image.load("../images/shadow.PNG")
images["upArrows"] = pygame.image.load("../images/upArrows.PNG")
images["instructions"] = pygame.image.load("../images/instructions.png")

#Initialize the cube object
lilCube = cube.Cube()

def build_image(SCREEN, cube):
    """
    Draws the background and cube
    :param SCREEN: the screen to blit onto
    :param cube: the cube object to display
    :return: None
    """
    #Put background on
    SCREEN.blit(images["background"], [0,0])

    #Use the draw_cube method to display the faces
    #pass in each of the faces to the cubeDrawer method
    cubeDrawer.draw_cube(
        cube.get_face_for_display(0),
        cube.get_face_for_display(5),
        cube.get_face_for_display(1),
        SCREEN
    )

    #display the Frame and Shadow for the cube
    SCREEN.blit(images["frame"], [0,0])
    SCREEN.blit(images["shadow"], [0,0])

#Define the regions for mouse hovering
u_region = Polygon([(177, 228),(300, 152),(433, 230),(300, 299)])
l_region = Polygon([ (177,228),(300,299),(303, 449),(173, 379) ])
f_region = Polygon([ (300,299),(433, 230),(432, 374),(303, 449) ])

def mouse_selection(SCREEN, coordinates):
    """
    Determines if the mouse is hovering over any of the three faces
    Returns a character corresponding to the face the mouse is hovering over, None otherwise
    :param SCREEN: the screen to blit on to
    :param coordinates: the coordinates of the mouse
    :return: a character, or None
    """
    mouse_pos = Point(coordinates)
    if u_region.contains(mouse_pos):
        SCREEN.blit(images["upArrows"], [0,0])
        return "U"
    elif l_region.contains(mouse_pos):
        SCREEN.blit(images["leftArrows"],[0,0])
        return "L"
    elif f_region.contains(mouse_pos):
        SCREEN.blit(images["rightArrows"], [0,0])
        return "F"
    return None

class Button():
    """
    A class for buttons
    """
    def __init__(self, rect):
        """
        Initialize the button
        :param rect: the rect where the button is
        """
        #the buttons Rect object
        self.rect = rect
        #whether the button was clicked last frame
        self.old_value = False

    def update(self,mousepos, mouseclick):
        """
        Update the button based on the mouse position
        and whether the mouse is down
        Returns true iff the button is down this frame but was up last frame
        :param mousepos: the position of the mouse
        :param mouseclick: whether the button is down
        :return: whether this button is clicked this frame
        """
        condition = self.rect.collidepoint(mousepos) and mouseclick
        if self.old_value == False and condition:
            self.old_value = condition
            return(True)
        else:
            self.old_value = condition
            return(False)

    def isHovering(self, mousepos):
        """
        Returns whether the mouse is hovering over this button's region
        :param mousepos: the current mouse position
        :return: whether this button is being hovered on
        """
        return self.rect.collidepoint(mousepos)

#Initialize Button dictionary with button objects
buttons = {}
buttons["help"] = Button(pygame.Rect(38, 38, 31, 31))
buttons["scramble"] = Button(pygame.Rect(76, 38, 31, 31))
buttons["reset"] = Button(pygame.Rect(131, 38, 31, 31))

#Initialize Vars to keep track of mouse clicks and key presses
previously_down = False
currently_down = False
previous_keystate = {K_RIGHT:0, K_LEFT:0, K_UP:0, K_DOWN:0}

#Initial moves on the cube
lilCube.parse_move_notation("R")
lilCube.x_rotation(-1)
lilCube.y_rotation(-1)

#Main loop
while True:
    #Get the current mouse position
    mouse_pos = pygame.mouse.get_pos()
    #Check to see if the app should quit
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        currently_down = event.type == MOUSEBUTTONDOWN

    #Click is true if the mouse is down but was up last frame
    click = False
    if (currently_down) and not(previously_down):
        click = True
    previously_down = currently_down

    keystate = pygame.key.get_pressed()

    #lilCube.parse_move_notation(input())

    build_image(SCREEN, lilCube)
    face_selected = mouse_selection(SCREEN, mouse_pos)
    if keystate[K_RIGHT] and not previous_keystate[K_RIGHT]:
        if face_selected:
            lilCube.parse_move_notation(face_selected + "")
        else:
            lilCube.y_rotation(1)
    elif keystate[K_LEFT] and not previous_keystate[K_LEFT]:
        if face_selected:
            lilCube.parse_move_notation(face_selected + "\'")
        else:
            lilCube.y_rotation(-1)
    elif keystate[K_UP] and not previous_keystate[K_UP]:
        lilCube.x_rotation(1)
    elif keystate[K_DOWN] and not previous_keystate[K_DOWN]:
        lilCube.x_rotation(-1)

    #update the previous keystates for next frame
    previous_keystate[K_RIGHT] = keystate[K_RIGHT]
    previous_keystate[K_LEFT] = keystate[K_LEFT]
    previous_keystate[K_UP] = keystate[K_UP]
    previous_keystate[K_DOWN] = keystate[K_DOWN]

    for key in buttons.keys():
        button = buttons[key]

        if key == "help" and button.isHovering(mouse_pos):
            SCREEN.blit(images["instructions"], [0, 0])

        if button.update(mouse_pos, currently_down):
            if key == "scramble":
                lilCube.scramble()
            elif key == "reset":
                lilCube = cube.Cube()


    pygame.display.update()