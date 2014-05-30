from collections import deque
from math import floor

def Window(object):


    def __init__(self, size = 20):
        self.window = deque([], size)

    def add(self, value):
        self.window.append(value)

    def average(self):
        c = list(self.window)
        return float(sum(c)) / float(len(c))

    def median(self):
        c = sorted(list(self.window))
        if len(c) == 0:
            return 0
        pivot = floor(len(c) / 2.0)
        return c[pivot: (pivot+1)][0]