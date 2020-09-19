import numpy as np
import math
import scipy.linalg as la
import pygame

# COLORS
GREEN=(0,255,0)

class Pendulum:
    def __init__(self, screen, bob_position=np.pi, bob_radius=20, bob_color=GREEN, rod_position=0, rod_length=100, rod_color=GREEN):
        '''
        Creates and Updates a Cartesian rod_position
        Creates and Updates a Polar bob_position
        '''
        # Characteristics of Bob
        self.screen = screen
        self.bob_position = bob_position # Theta
        self.bob_radius = bob_radius
        self.bob_color = bob_color

        # Characteristics of Rod
        self.rod_position = rod_position
        self.rod_length = rod_length
        self.rod_color = rod_color

    def update_pos(self, theta, cart_position, cart_size ):
        '''
        Updates
        Polar Coordinates for the Bob

        Updates
        Cartesian Coordinates for the Rod 
        '''

        cart_center = ( cart_position[0]+(0.5)*cart_size[0], cart_position[1]+(.5)*cart_size[1] )


        x = cart_center[0] - self.rod_length*math.sin(theta)
        y = cart_center[1] + self.rod_length*math.cos(theta)

        self.bob_position = ( int(x), int(y) )

        pygame.draw.line( self.screen, self.rod_color, cart_center, self.bob_position, 10)
        pygame.draw.circle( self.screen, self.bob_color, self.bob_position, self.bob_radius, 0)


class Cart:
    def __init__(self, screen, cart_position, cart_size, color):
        '''
        Creates and updates the cartesian coordinate system

        '''

        self._rectangle = pygame.Rect( cart_position, cart_size )
        self.cart_size = cart_size
        self.cart_position = cart_position
        #self.cart_center = (cart_position[0]+int(cart_size[1]/2), cart_position[1]-int(cart_size[1]/2))
        self.screen = screen
        self.color = color

    def update_pos(self, x, y ):
        '''
            Cartesian Movement in X and Y
            
                and
            
            Drawing Step All In One
        '''
        x_position = x
        # With Respect to Origin on Lower Left Side of Scren
        #y_position = (self.screen.get_height()-self.cart_size[1]) - y
        y_position = (self.screen.get_height()) - y

        # Update Cart Position
        self.cart_position = ( x_position, y_position )
        #self.cart_center = (self.cart_position[0]+int(self.cart_size[1]/2), self.cart_position[1]-int(self.cart_size[1]/2))

        self.rectangle = pygame.Rect( self.cart_position, self.cart_size )
        pygame.draw.rect( self.screen, self.color, self.rectangle )
