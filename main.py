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
        self.rect = self.image.get_rect(center = (752, 500))
        self.vel_vector = pygame.math.Vector2(0, 0.8)
        self.angle = 0

        self.rotation_vel = 3
        self.direction = 0
        self.alive = True
        self.radars = []
    
    def update(self):
        self.radars.clear() 
        self.drive()
        self.rotate()
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.collision()
        self.data()
    
    def drive(self):
        self.rect.center += self.vel_vector * 4
    
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

        dist = int(math.sqrt(math.pow(self.rect.centerx - x, 2) + math.pow(self.rect.centery - y, 2)))
        self.radars.append([radar_angle, dist])

    def collision(self):
        length = 32

        collision_point_right = [int(self.rect.centerx + math.sin(math.radians(self.angle + 30)) * length), int(self.rect.centery + math.cos(math.radians(self.angle + 30)) * length)]

        collision_point_left = [int(self.rect.centerx + math.sin(math.radians(self.angle - 30)) * length), int(self.rect.centery + math.cos(math.radians(self.angle - 30)) * length)]

        if SCREEN.get_at(collision_point_right) == pygame.Color(97, 184, 1, 255) or SCREEN.get_at(collision_point_left) == pygame.Color(128, 197, 106, 255):
            self.alive = False
            print("Dead !!!")

        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_right, 4)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_left, 4)

    def data(self) :
        input = [0, 0, 0, 0, 0] 
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        return input

def remove(index) :
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)


def eval_genomes(genomes, config):
    global cars, ge, nets

    cars = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        
        SCREEN.blit(TRACK, (0, 0))
        if(len(cars) == 0) :
            break

        for i, car in enumerate(cars):
            ge[i].fitness += 1
            if not car.sprite.alive:
                remove(i)

        for i, car in enumerate(cars) : 
            output = nets[i].activate(car.sprite.data())
            if output[0] > 0.7:
                car.sprite.direction = 1
            elif output[1] > 0.7:
                car.sprite.direction = -1
            elif output[0] <= 0.7 and output[1] <= 0.7:
                car.sprite.direction = 0

        for car in cars:
            car.draw(SCREEN)
            car.update()
        pygame.display.update()

def run(config_file):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.run(eval_genomes, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__) 
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
