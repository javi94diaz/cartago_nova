import random

class Dice:

    @staticmethod
    def roll(sides):
        return random.randint(1, sides)

    @staticmethod
    def d6():
        return Dice.roll(6)
    
    @staticmethod
    def roll_many(num, sides=6):
        return [Dice.roll(sides) for _ in range(num)]