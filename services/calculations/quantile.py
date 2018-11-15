import numpy as np


def sixty_percent_quantile(cell):
    return np.quantile(cell, 0.6)
