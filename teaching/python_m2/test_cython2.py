#%%
from numba import jit
import numba
import numpy as np

import random
# Serial version
@jit(nopython=True)
def monte_carlo_pi_serial(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

@jit(nopython=True, parallel=True)
def monte_carlo_pi_parallel(nsamples):
    acc = 0
    for i in numba.prange(nsamples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

%timeit monte_carlo_pi_serial(int(4e8))
%timeit monte_carlo_pi_parallel(int(4e8))