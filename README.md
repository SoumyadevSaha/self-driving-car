# Self-Driving Car
A self-driving car model made with pygame and neat library to train neural netwroks.

## Libraries and Setup:
- `pygame` is imported for creating a game.
- `os`, `math`, and `sys` are used for system-related functionalities.
- `neat` is imported for implementing the `NEAT` algorithm.

## Game Initialization:

- SCREEN_WIDTH and SCREEN_HEIGHT are set for the game window.
- TRACK image and Car class are initialized.

<hr>

### Car Class:
Represents a car sprite in the game.
Manages car movement, rotation, radar sensing, collision detection, and data collection.
Radars are lines drawn from the car in different directions to sense obstacles.
Collision is checked based on the color of pixels in the game track.
data method returns the distances from the car to obstacles sensed by radars.

### NEAT Initialization:
eval_genomes function evaluates the genomes using the NEAT algorithm.
A population of cars, genomes, and neural networks is maintained.
Fitness of each genome is updated based on car performance.

### NEAT Genome Evaluation Loop:
Event handling for quitting the game is present.
The game track is displayed.
Cars are updated and drawn on the screen.
Neural networks of cars make decisions based on radar data.
Cars are removed if they collide with obstacles or go out of bounds.

### NEAT Configuration:
NEAT configuration is set through config.txt.
Specifies parameters for genome structure, activation functions, mutation rates, and other NEAT-specific settings.
Defines the structure of neural networks and how they evolve.

### NEAT Population Initialization and Execution:
NEAT population is initialized with the provided configuration.
The population undergoes evolution and fitness evaluation through the NEAT algorithm.

<hr>

## Algorithm Used:

`NEAT` algorithm for evolving neural networks.

## Libraries Used:

- `pygame` for game development.
- `neat` for implementing the NEAT algorithm.

## Functionality:

- Simulates a game environment where cars (controlled by evolved neural networks) navigate a track.
- NEAT is employed to evolve neural networks for decision-making.
- Cars use radar sensing, collision detection, and NEAT-optimized neural networks to navigate.

## Getting Started
- Fork and Clone the repo or donload the zip 
- run the `main.py` file

## Screenshots
<img width="1066" alt="Screenshot 2024-04-23 at 12 47 19 PM" src="https://github.com/SoumyadevSaha/self-driving-car/assets/86418216/b19c73a3-975d-4465-88e7-03e9afa32454">
