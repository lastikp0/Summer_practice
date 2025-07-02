import random


class GeneratorParams:
    @staticmethod
    def generate(size=None):
        return [100, 0.9, 0.1, 150]


class GeneratorMatrix:
    @staticmethod
    def generate(size=3):
        return [random.randint(1, 300) for _ in range(size)]