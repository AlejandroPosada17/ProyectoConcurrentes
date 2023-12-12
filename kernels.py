
import numpy as np

class Kernels:
    def __init__(self):
        self.class1 = np.array([[0, 0, 0, 0, 0],
                                      [0, 0, 1, 0, 0],
                                      [0, 0, -1, 0, 0],
                                      [0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0]])

        self.class2 = np.array([[0, 0, 0, 0, 0],
                                   [0, 0, 1, 0, 0],
                                   [0, 0, -2, 0, 0],
                                   [0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0]])