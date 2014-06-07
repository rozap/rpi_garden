from collections import deque
from math import floor

class Window(object):

    def __init__(self, size = 50):
        self.window = deque([], size)

    def add(self, value):
        self.window.append(value)

    def average(self):
        c = list(self.window)
        return float(sum(c)) / float(len(c))


    def moving_average(self, alpha = 0):
        c = list(self.window)
        num = 0.0
        denom = 0.0
        for i, val in enumerate(c):
            num += ((1 - alpha) ** i) * float(val)
            denom += ((1 - alpha) ** i)
        return num / denom

    def median(self):
        c = sorted(list(self.window))
        if len(c) == 0:
            return 0
        pivot = int(floor(len(c) / 2.0))
        return c[pivot: (pivot+1)][0]
