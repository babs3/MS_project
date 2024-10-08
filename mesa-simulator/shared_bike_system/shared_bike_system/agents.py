import mesa

from .random_walk import RandomWalker


class Bike(RandomWalker):
    """
    A bike that is driven by a person.

    The init is the same as the RandomWalker.
    """

    battery_level = 100

    def __init__(self, model, moore, battery_level=100):
        super().__init__(model, moore=moore)
        self.battery_level = battery_level

    def step(self):
        """
        A model step. Move, ... .
        """

        # a bike can only move if it has battery
        if self.battery_level >= 1:
            self.random_move()
            self.battery_level -= 1
            
