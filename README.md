# GPP 2027 - Take Home Coding Assignment

# Auto Driving Car Simulation

## Overview

This is an Auto Driving Car Simulation that models one or more autonomous vehicles moving across a grid-based field. The application supports:

- **Single Car Simulation**: Move a car according to a set of commands, within a defined grid, and determine its final position and direction.
- **Multi-Car Simulation**: Simultaneously move multiple cars (2 or more) with individual command sequences, and detect if any collision occurs when cars attempt to move to the same location at the same step.

The simulation ensures boundary enforcement and accurate handling of movement and orientation.

---

## Design and Assumptions

### Design

- **Car Class**: Handles the car's state, including its position, direction, and movement logic. Includes methods to rotate left or right and move forward, with a built-in direction mapping (`N`, `E`, `S`, `W`).

- **Field Class**: Manages the grid and all car instances. It validates movements within grid boundaries and detects collisions—either at the initial positions or during simulation.

- **Simulation Functions**:
  - `part1_simulation()`: Executes movement for a single car and returns its final position and direction.
  - `part2_simulation()`: Simulates multiple cars step-by-step, checking for collisions, and returns the first collision point and step, or returns "no collision".

### Assumptions

- The grid is defined by width and height, with `(0, 0)` as the bottom-left corner.
- Cars cannot move beyond the grid boundaries. Such moves are ignored.
- If multiple cars attempt to move to the same cell in the same step, a collision is detected and recorded.
- Input is expected in a specific format:
  - Part 1: 3 lines (grid size, car position, commands)
  - Part 2: grid size followed by blocks of car name, position, and commands.

---

## Requirements 

- **Python**: Version 3.12.4 (Tested with Python 3.12.4)
- **Operating System**: Works on Windows, macOS, or Linux. Tested on macOS 12.3.1.
- **Dependencies**: No external libraries required. Uses only Python standard library (`unittest`, `sys`).

---

## How to Run

1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/amberchen21/Chen-Si-An-Amber-GPP.git
   cd Chen-Si-An-Amber-GPP
2. **Run the Application**: 
   ```bash
   python3 car_simulation.py
   python3 car_simulation.py < input.txt
   ```
3. **Test the Application**: 
   ```bash
   python3 test_car_simulation.py
   ```
