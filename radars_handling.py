# Handling the radars to check the distance between the car and the edge of the track ->

import pygame
import os
import math
import sys
import neat

# the purpose of the radars is to measure the distance between the car and the edge of the track, and finally provide us with the data that will be used as an input tothe neural network.

SCREEN_WIDTH = 1066
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

TRACK = pygame.image.load(os.path.join("assets", "track3.png"))

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join("assets", "car.png"))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (752, 600))
        self.drive_state = 0
        self.vel_vector = pygame.math.Vector2(0, 0.8)
        self.angle = 0
        # for steering
        self.rotation_vel = 3
        self.direction = 0
        # for collision status
        self.alive = True
    
    def update(self):
        self.drive()
        self.rotate()
        # Creating the radar (We shall create 5 different radars for the 5 different angles) ->
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        # To check for collsions ->
        self.collision()
    
    def drive(self):
        if self.drive_state == 1:
            self.rect.center += self.vel_vector * 4
        elif self.drive_state == -1:
            self.rect.center -= self.vel_vector * 4
    
    def rotate(self):
        if self.direction == -1:
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)
        elif self.direction == 1:
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)
        
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.08)
        self.rect = self.image.get_rect(center = self.rect.center)
    
    # Creating the radars fn ->
    def radar(self, radar_angle):
        length = 0 # It is going to be responsible for the length of the radar.
        # The radars are going to start at the center of the car and are going to get longer as they reach theend of the track.
        x = int(self.rect.centerx)
        y = int(self.rect.centery)

        # While loop responsible for extending the radar until it hits a grassy area ->
        while (x < 1066 and x > 0) and (y < 800 and y > 0) and (length < 100) and (not (SCREEN.get_at((x, y)) == pygame.Color(97, 184, 1, 255))) :
            length += 1
            # calculate the end-point of our radar ->
            x = int(self.rect.centerx + math.sin(math.radians(self.angle + radar_angle)) * length)
            y = int(self.rect.centery + math.cos(math.radians(self.angle + radar_angle)) * length)
        
        # drawing the radar to visualize the distance ->
        pygame.draw.line(SCREEN, (255, 255, 255), (self.rect.centerx, self.rect.centery), (x, y), 1)
        pygame.draw.circle(SCREEN, (255, 255, 0, 0), (x, y), 4)

    # Our collision function ->
    def collision(self):
        length = 36 # distance between the center of the car and the collision point.

        # Creating 2 collision points, 1st one located at the right head-light of the car and the 2nd one at the left headlight.
        collision_point_right = [int(self.rect.centerx + math.sin(math.radians(self.angle + 20)) * length), int(self.rect.centery + math.cos(math.radians(self.angle + 20)) * length)]

        collision_point_left = [int(self.rect.centerx + math.sin(math.radians(self.angle - 20)) * length), int(self.rect.centery + math.cos(math.radians(self.angle - 20)) * length)]

        # Dying on collision ->
        if SCREEN.get_at(collision_point_right) == pygame.Color(97, 184, 1, 255) or SCREEN.get_at(collision_point_left) == pygame.Color(128, 197, 106, 255):
            self.alive = False
            print("Dead !!!")

        # Drawing Collision points ->
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_right, 3)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_left, 3)

# Container holding a single sprite image ->
car = pygame.sprite.GroupSingle(Car())
# Main Loop ->
def eval_genomes():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        
        SCREEN.blit(TRACK, (0, 0))

        # Handling User Input ->
        user_input = pygame.key.get_pressed()
        if sum(pygame.key.get_pressed()) <= 1:
            car.sprite.drive_state = 0
            car.sprite.direction = 0

        # Steering the car ->
        if user_input[pygame.K_LEFT]:
            car.sprite.direction = -1
        elif user_input[pygame.K_RIGHT]:
            car.sprite.direction = 1

        # Driving condition ->
        if user_input[pygame.K_UP]:
            car.sprite.drive_state = 1
        elif user_input[pygame.K_DOWN]:
            car.sprite.drive_state = -1

        car.draw(SCREEN)
        car.update()
        pygame.display.update()

eval_genomes()
