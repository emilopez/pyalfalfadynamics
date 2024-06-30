import numpy as np

def fisher(x, c1, c2):
    return 0.5 + 0.5*np.tanh(c1*x - c2)

def landau(x, c1, c2):
    return np.sqrt(0.5 + 0.5*np.tanh(c1*x - c2))

def gompertz(x, c1, c2):
    return np.exp(-c1*np.exp(-c2*x))
