import unittest
from car_simulation import *

class TestCarSimulation(unittest.TestCase):

    def test_rotation(self):
        car = Car("A", 0, 0, 'N')
        car.rotate('L')
        self.assertEqual(car.direction, 'W')
        car.rotate('R')
        self.assertEqual(car.direction, 'N')

    def test_forward_movement(self):
        car = Car("A", 1, 1, 'N')
        new_x, new_y = car.get_next_position()
        car.move(new_x, new_y)
        self.assertEqual((car.x, car.y), (1, 2))

    def test_boundary_block(self):
        car = Car("A", 0, 0, 'S')
        new_x, new_y = car.get_next_position()
        field = Field(10, 10)
        if field.is_valid_position(new_x, new_y):
            car.move(new_x, new_y)
        self.assertEqual((car.x, car.y), (0, 0))

    def test_sample_path(self):
        car = Car("A", 1, 2, 'N')
        commands = 'FFRFFFRRLF'
        field = Field(10, 10)
        for command in commands:
            if command in ['L', 'R']:
                car.rotate(command)
            elif command == 'F':
                new_x, new_y = car.get_next_position()
                if field.is_valid_position(new_x, new_y):
                    car.move(new_x, new_y)
        self.assertEqual((car.x, car.y, car.direction), (4, 3, 'S'))

    def test_initial_collision(self):
        field = Field(10, 10)
        car1 = Car("A", 5, 5, 'N')
        car2 = Car("B", 5, 5, 'S')
        field.add_car(car1)
        field.add_car(car2)
        collisions = field.get_collisions()
        self.assertTrue(collisions)
        self.assertEqual(collisions[0][0], ['A', 'B'])
        self.assertEqual(collisions[0][1], (5, 5))

    def test_no_collision(self):
        field = Field(10, 10)
        car1 = Car("A", 0, 0, 'N')
        car2 = Car("B", 1, 0, 'N')
        field.add_car(car1)
        field.add_car(car2)
        commands = {
            "A": "F",
            "B": "F"
        }
        field.process_commands(commands)
        collisions = field.get_collisions()
        self.assertEqual(collisions, [])
        
    def test_single_car_movement(self):
        width, height = 10, 10
        field = Field(width, height)

        car = Car("A", 1, 2, 'N')
        field.add_car(car)
 
        commands = "FFRFFFRRLF"
 
        for command in commands:
            if command in ['L', 'R']:
                car.rotate(command)
            elif command == 'F':
                new_x, new_y = car.get_next_position()
                if field.is_valid_position(new_x, new_y):
                    car.move(new_x, new_y)

        self.assertEqual((car.x, car.y, car.direction), (4, 3, 'S'))

    def test_collision_AB(self):
        width, height = 10, 10
        field = Field(width, height)
 
        car_a = Car("A", 1, 2, 'N')
        car_b = Car("B", 7, 8, 'W')
 
        field.add_car(car_a)
        field.add_car(car_b)
 
        commands = {
            "A": "FFRFFFFRRL",
            "B": "FFLFFFFFFF"
        }
 
        field.process_commands(commands)
        collisions = field.get_collisions()
 
        self.assertTrue(collisions)
        expected_car_names = ['A', 'B']
        expected_position = (5, 4)
        expected_step = 7

        actual_car_names, actual_position, actual_step = collisions[0]
        self.assertEqual(actual_car_names, expected_car_names)
        self.assertEqual(actual_position, expected_position)
        self.assertEqual(actual_step, expected_step)


if __name__ == "__main__":
    unittest.main()
