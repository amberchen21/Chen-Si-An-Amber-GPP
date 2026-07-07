import sys

class Car:
    '''
    Represents an autonomous car on a grid.
    Stores the car's name, position, facing direction, and movement history.
    '''
    DIRECTION_MAP = {
        'N': {'L': 'W', 'R': 'E', 'move': (0, 1)},
        'E': {'L': 'N', 'R': 'S', 'move': (1, 0)},
        'S': {'L': 'E', 'R': 'W', 'move': (0, -1)},
        'W': {'L': 'S', 'R': 'N', 'move': (-1, 0)}
    }

    def __init__(self, name, x, y, direction):
        self.name = name
        self.x = x
        self.y = y
        self.direction = direction
        self.history = [(x, y)]  # Track position at each step

    def rotate(self, command):
        # Rotate car 90 degrees to left or right based on command ('L' or 'R')
        if command in ['L', 'R']:
            self.direction = self.DIRECTION_MAP[self.direction][command]
    
    def get_next_position(self):
        # Compute car’s next position based on its current direction
        dx, dy = self.DIRECTION_MAP[self.direction]['move']
        return self.x + dx, self.y + dy
    
    def move(self, new_x, new_y):
        # Move car to new coordinates
        self.x = new_x
        self.y = new_y
        self.history.append((new_x, new_y))
    
    def get_current_position(self):
        # Return car’s current (x, y) position
        return (self.x, self.y)
    
    def __str__(self):
        # Return string representation of car’s position and direction
        return f"{self.x} {self.y} {self.direction}"


class Field:
    '''
    Represents the simulation grid and manages multiple cars.
    Handles collision detection and movement execution.
    '''
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cars = {} # Dictionary of {car_name: Car object}
        self.collisions = [] # List of (car_names, position, step_number)
        
    def add_car(self, car):
        # Add a car to field. If another car is already at same position, record an initial collision.

        # Check for initial collision before adding the car
        colliding_cars = []
        for existing_car in self.cars.values():
            if existing_car.get_current_position() == car.get_current_position():
                colliding_cars.append(existing_car.name)
        
        if colliding_cars:
            # Include new car in collision list
            colliding_cars.append(car.name)
            self.collisions.append((sorted(colliding_cars), 
                                  car.get_current_position(), 
                                  1)) # Initial collision counted at step 1
        self.cars[car.name] = car

    def is_valid_position(self, x, y):
        # Check if a position is within field boundaries
        return 0 <= x < self.width and 0 <= y < self.height
    
    def process_commands(self, commands_dict):
        # Execute all cars' commands step-by-step.
        # Detect and record collisions if multiple cars attempt to move to same position

        # If we already have initial collisions, return immediately
        if self.collisions:
            return
        
        max_steps = max(len(commands) for commands in commands_dict.values())
        
        for step in range(max_steps):
            current_step = step + 1 
            # Track planned moves to detect same-step collisions
            planned_positions = {}
            
            # First phase: plan all moves
            for name, car in self.cars.items():
                commands = commands_dict[name]
                if step < len(commands):
                    command = commands[step]
                    
                    if command == 'F':
                        new_x, new_y = car.get_next_position()
                        if self.is_valid_position(new_x, new_y):
                            # Record planned position for collision detection
                            if (new_x, new_y) not in planned_positions:
                                planned_positions[(new_x, new_y)] = []
                            planned_positions[(new_x, new_y)].append((name, current_step))
                    else:
                        car.rotate(command)
            
            # Second phase: execute moves and check for collisions 
            for pos, cars in planned_positions.items():
                if len(cars) > 1:
                    # Collision detected - get all involved cars
                    car_names = sorted([car[0] for car in cars])
                    step_num = cars[0][1]  # All have same step number
                    
                    # Check if we already have a collision at this step
                    existing_collision = next(
                        (c for c in self.collisions 
                         if c[2] == step_num and set(car_names).issubset(set(c[0]))),
                        None
                    )
                    
                    if not existing_collision:
                        self.collisions.append((car_names, pos, step_num))
                    
                    # Don't return here to find all collisions in this step
                    # Just prevent the moves from happening
                    continue
                
                # No collision, so proceed to excute the move
                name, _ = cars[0]
                self.cars[name].move(pos[0], pos[1])
    
    def get_collisions(self):
        # Return list of detected collisions
        return self.collisions


def parse_input_part1(input_lines):
    # Parse input for single car collision
    width, height = map(int, input_lines[0].strip().split())
    x, y, direction = input_lines[1].strip().split()
    commands = input_lines[2].strip()
    return width, height, x, y, direction, commands


def parse_input_part2(input_lines):
    # Parse input for multiple car collision
    lines = [line.strip() for line in input_lines if line.strip()]
    width, height = map(int, lines[0].split())
    
    cars = {}
    commands = {}
    i = 1
    while i < len(lines):
        name = lines[i]
        x, y, direction = lines[i+1].split()
        cmd = lines[i+2]
        cars[name] = (int(x), int(y), direction)
        commands[name] = cmd
        i += 3
    
    return width, height, cars, commands


def part1_simulation(input_lines):
    # Run simulation for a single car and return its final state
    width, height, x, y, direction, commands = parse_input_part1(input_lines)
    field = Field(width, height)
    car = Car("A", int(x), int(y), direction) # Arbitrarily name it as Car A
    field.add_car(car)
    
    # Process commands one by one
    for command in commands:
        if command == 'F':
            new_x, new_y = car.get_next_position()
            if field.is_valid_position(new_x, new_y):
                car.move(new_x, new_y)
        else:
            car.rotate(command)
    
    return str(car)


def part2_simulation(input_lines):
    # Run simulation for multiple cars and return the first collision (if any)
    width, height, cars, commands = parse_input_part2(input_lines)
    field = Field(width, height)
    
    for name, (x, y, direction) in cars.items():
        car = Car(name, x, y, direction)
        field.add_car(car)
    
    field.process_commands(commands)
    collisions = field.get_collisions()
    
    if collisions:
        # Return first collision
        car_names, pos, step = collisions[0]
        return f"{' '.join(car_names)}\n{pos[0]} {pos[1]}\n{step}"
    else:
        return "no collision"


if __name__ == "__main__":
    # Read input lines from stdin
    input_lines = [line.strip() for line in sys.stdin if line.strip()]
    
    # Automatically determine Part 1 or Part 2 input format
    if len(input_lines) == 3 and not input_lines[1][0].isalpha():
        # Part 1 input
        result = part1_simulation(input_lines)
        print(result)
    else:
        # Part 2 input
        result = part2_simulation(input_lines)
        print(result)
