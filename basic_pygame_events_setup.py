# Drawing the car, the track and handling steering events ->

import pygame
import os
import math
import sys
import neat

SCREEN_WIDTH = 980
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

TRACK = pygame.image.load(os.path.join("assets", "track1.png"))

# Creating sprite classes for games is useful in 2D games.
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join("assets", "car1.png"))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (370, 640))
        self.drive_state = 0
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotation_vel = 3
        self.direction = 0 # This is -1 when we turn left, and 1 when its is right, else 0.
    
    def update(self):
        self.drive()
        self.rotate()
    
    def drive(self):
        if self.drive_state == 1:
            self.rect.center += self.vel_vector * 4
        elif self.drive_state == -1:
            self.rect.center -= self.vel_vector * 4
    
    def rotate(self):
        if self.direction == 1: # For right
            self.angle -= self.rotation_vel
            # We also need to change the velocity vector.
            self.vel_vector.rotate_ip(self.rotation_vel)
        elif self.direction == -1: # For left
            self.angle += self.rotation_vel
            # We also need to change the velocity vector.
            self.vel_vector.rotate_ip(-self.rotation_vel)
        
        # Fitting the car image into the road of the track.
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.08)
        # Get the reactangle of the car image.
        self.rect = self.image.get_rect(center = self.rect.center)

# Container holding a single sprite image ->
car = pygame.sprite.GroupSingle(Car())

# Main Loop ->
def eval_genomes():
    # The main loop is going to help us evaluate the fitness of all the cars in the track, which helps us to determine what cars are used by the algorithm to learn the driving mechanic.

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        
        SCREEN.blit(TRACK, (0, 0))

        # Handling User Input ->
        user_input = pygame.key.get_pressed() # user_input contains the key that was most recently pressed on the key board.
        if sum(pygame.key.get_pressed()) <= 1: # When no keys are pressed, the drive_state is set to False.
            car.sprite.drive_state = 0
            # Value of the direction is 0.
            car.sprite.direction = 0

        # Steering the car ->
        if user_input[pygame.K_LEFT]:
            car.sprite.direction = -1
        elif user_input[pygame.K_RIGHT]:
            car.sprite.direction = 1

        # Driving condition ->
        if user_input[pygame.K_UP]:
            # Drive state is true when the user presses the up key.
            car.sprite.drive_state = 1
        elif user_input[pygame.K_DOWN]:
            car.sprite.drive_state = -1

        # Update the screen ->
        car.draw(SCREEN)
        car.update()
        pygame.display.update()

# Calling the main loop ->
eval_genomes()
