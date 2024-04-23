# Adding the A.I. ->

import pygame
import os
import math
import sys
import neat

SCREEN_WIDTH = 1066
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

TRACK = pygame.image.load(os.path.join("assets", "track3.png"))

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join("assets", "car.png"))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (100, 330))
        # self.drive_state = 0
        self.vel_vector = pygame.math.Vector2(0, 0.8)
        self.angle = 0

        self.rotation_vel = 3
        self.direction = 0
        self.alive = True

        # Adding an empty list radars stores all the data collected by the individual radars on our car(s).
        self.radars = []
    
    def update(self):
        self.radars.clear() # We3 clear the radras every time update is called, as we want the most up-to-date data on the radars list.
        self.drive()
        self.rotate()
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.collision()

        # We call self.data()
        self.data()
    
    def drive(self):
        # if self.drive_state == 1:
        self.rect.center += self.vel_vector * 4
        # elif self.drive_state == -1:
        #     self.rect.center -= self.vel_vector * 4
    
    def rotate(self):
        if self.direction == -1:
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)
        elif self.direction == 1:
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)
        
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.08)
        self.rect = self.image.get_rect(center = self.rect.center)
    
    def radar(self, radar_angle):
        length = 0
        x = int(self.rect.centerx)
        y = int(self.rect.centery)

        while (x < 1066 and x > 0) and (y < 800 and y > 0) and (length < 100) and (not (SCREEN.get_at((x, y)) == pygame.Color(97, 184, 1, 255))) :
            length += 1
            x = int(self.rect.centerx + math.sin(math.radians(self.angle + radar_angle)) * length)
            y = int(self.rect.centery + math.cos(math.radians(self.angle + radar_angle)) * length)

        pygame.draw.line(SCREEN, (255, 255, 255), (self.rect.centerx, self.rect.centery), (x, y), 1)
        pygame.draw.circle(SCREEN, (255, 255, 0, 0), (x, y), 4)

        # A variable called dist stores he distance between the center of the car and the tip of the radars.
        dist = int(math.sqrt(math.pow(self.rect.centerx - x, 2) + math.pow(self.rect.centery - y, 2)))

        # we are also going to append the data collected by eaxh individual radar to the radars list.
        self.radars.append([radar_angle, dist])

    def collision(self):
        length = 36

        collision_point_right = [int(self.rect.centerx + math.sin(math.radians(self.angle + 20)) * length), int(self.rect.centery + math.cos(math.radians(self.angle + 20)) * length)]

        collision_point_left = [int(self.rect.centerx + math.sin(math.radians(self.angle - 20)) * length), int(self.rect.centery + math.cos(math.radians(self.angle - 20)) * length)]

        if SCREEN.get_at(collision_point_right) == pygame.Color(97, 184, 1, 255) or SCREEN.get_at(collision_point_left) == pygame.Color(128, 197, 106, 255):
            self.alive = False
            print("Dead !!!")

        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_right, 3)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_left, 3)

    def data(self) :
        input = [0, 0, 0, 0, 0] 
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        return input # this input list provides the data to train our AI.

# car = pygame.sprite.GroupSingle(Car())

def remove(index) :
    # when we train the AI, we are going to have multiple cars going around the track and this remove fn helps to remove the cars that run into the grass area. It takes index parameter as each individual car is indexed.
    cars.pop(index) # removing the car
    ge.pop(index) # removing the genome
    nets.pop(index) # removing the neural net.


def eval_genomes(genomes, config):
    # in our case, the genomes are repn by individual cars. And, this function gives excah of pur cars a fitness score, the fitness score measures how well the car runs on the track, or stays alive on it.
    global cars, ge, nets

    cars = []
    ge = []
    nets = []
    # This for loop fills each ofthe 3 lists with the appropriate number of cars.
    for genome_id, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        # initial fitness of each car is 0.
        genome.fitness = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        
        SCREEN.blit(TRACK, (0, 0))

        # Handling User Input ->
        # user_input = pygame.key.get_pressed()
        # if sum(pygame.key.get_pressed()) <= 1:
        #     car.sprite.drive_state = 0
        #     car.sprite.direction = 0

        # # Steering the car ->
        # if user_input[pygame.K_LEFT]:
        #     car.sprite.direction = -1
        # elif user_input[pygame.K_RIGHT]:
        #     car.sprite.direction = 1

        # # Driving condition ->
        # if user_input[pygame.K_UP]:
        #     car.sprite.drive_state = 1
        # elif user_input[pygame.K_DOWN]:
        #     car.sprite.drive_state = -1

        if(len(cars) == 0) :
            break

        # this for loop increments the fitness score of all the cars in the track over time.
        for i, car in enumerate(cars):
            ge[i].fitness += 1
            # removing the car running into the grass ->
            if not car.sprite.alive:
                remove(i)
        
        # this for loop determines how each individual car drives on the track.
        for i, car in enumerate(cars) : 
            # now the driving shall depend on the output of the neural network, not on the arrow keys anymore.
            output = nets[i].activate(car.sprite.data()) # thsi activation function takes in an argument: the data generated by the car's radars. The output gives us a list with 2 elements, both the elements are between -1 or 1
            if output[0] > 0.7:
                car.sprite.direction = 1 # the car turns right.
            elif output[1] > 0.7:
                car.sprite.direction = -1 # the car turns left.
            elif output[0] <= 0.7 and output[1] <= 0.7:
                car.sprite.direction = 0 # the car does not turn.

        # update the screen ->
        for car in cars:
            car.draw(SCREEN)
            car.update()
        pygame.display.update()

# eval_genomes()

# Setting up the NEAT neural network ->
def run(config_file):
    global pop # short for 'population'
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    pop = neat.Population(config) # creating the population.

    # Creating the statistics reporter. (thsi provides helpful statistics for each generation of cars that goes round the track)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    # calling the run function on the population ->
    pop.run(eval_genomes, 50) # 50 is the number of generations of cars that we want to iterate through.

# Running the entire program ->
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__) # specifying the path to the local directory
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
