# SmartScheduler Algorithm Documentation

This directory contains various scheduling algorithms implemented for the SmartScheduler application. Each algorithm takes a different approach to solve the class scheduling problem.

## Algorithm Overview

### 1. Simple Genetic Algorithm (`simple_genetic.py`)

A basic genetic algorithm implementation that evolves a population of schedules over generations:

- **Population Size**: 30 schedules
- **Generations**: 50
- **Mutation Rate**: 0.2
- **Crossover Rate**: 0.7
- **Selection Method**: Roulette wheel selection
- **Fitness Factors**: Teacher conflicts, section conflicts, teacher-subject suitability

The algorithm randomly generates initial schedules, then iteratively improves them through selection, crossover, and mutation operations. Best individuals are preserved through elitism.

### 2. Multi-Objective Genetic Algorithm (`moga_algo.py`)

An advanced genetic algorithm with multiple optimization objectives and adaptive parameters:

- **Population Size**: 100 schedules
- **Generations**: 200
- **Initial Mutation Rate**: 0.2 (adaptive)
- **Crossover Rate**: 0.9
- **Elitism Count**: 5
- **Selection Method**: Tournament selection
- **Fitness Factors**: Teacher conflicts, section conflicts, teacher load balance, teacher-subject suitability
- **Early Stopping**: After 20 generations without improvement

Features parallel processing for fitness calculations and targeted mutation based on conflict types. Incorporates early stopping when a perfect solution is found.

### 3. Ant Colony Optimization (`ant_colony.py`)

Inspired by ant behavior, this algorithm uses pheromone trails to guide the search:

- **Ants**: 20
- **Iterations**: 50
- **Evaporation Rate**: 0.5
- **Pheromone Importance (α)**: 1.0
- **Heuristic Importance (β)**: 2.0
- **Pheromone Deposit Factor (Q)**: 100.0

Ants construct solutions incrementally, depositing pheromones on promising schedule components. The pheromone trails guide future ants toward better solutions while allowing exploration.

### 4. Hill Climbing (`hill_climbing.py`)

A local search algorithm that iteratively improves a single solution:

- **Max Iterations**: 1000
- **Max Neighbors**: 100 per iteration
- **No Improvement Limit**: 50 iterations
  
The algorithm starts with a random schedule and repeatedly explores neighboring solutions by making small modifications. It accepts changes only when they improve the solution.

## Common Features

All algorithms:
1. Load necessary data from the database (teachers, sections, subjects)
2. Consider teacher-subject suitability when making assignments
3. Minimize conflicts (teachers teaching multiple classes simultaneously, sections having multiple subjects at once)
4. Return metrics about the generated schedule's quality
5. Save the optimized schedule to the database

## Usage

Each algorithm is exposed through a function that can be called from route handlers:

```python
# For the Simple Genetic Algorithm
from scripts.simple_genetic import create_simple_genetic_schedule

# For the Multi-Objective Genetic Algorithm 
from scripts.moga_schedule import create_moga_schedule

# For the Ant Colony Optimization
from scripts.ant_colony import create_ant_colony_schedule

# For the Hill Climbing algorithm
from scripts.hill_climbing import create_hill_climbing_schedule
```

All these functions take the same parameters:
- `session`: Database session
- `Section`: Section model class
- `Subject`: Subject model class
- `Teacher`: Teacher model class
- `Schedule`: Schedule model class

And return a tuple containing:
- Number of schedules created
- Metrics dictionary with quality indicators
- Execution time
