#%%
import timeit
from matplotlib import pyplot as plt
from numba import jit, njit
# Import the Cython function
from example import sum_of_squares as sum_of_squares_cython

# Define the Python version of the function
def sum_of_squares(n):
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total

@jit
def sum_of_squares_numb(n):
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total

@njit
def sum_of_squares_numb_njit(n):
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total


# Define the range of n values to test
n_values = [10**i for i in range(1, 8)]  # Testing for n = 10, 100, 1000, ..., 10 million

TRIALS = 100
# Lists to store timing results
python_times = []
cython_times = []
numba_times = []
numba_times_njit = []

# Loop over n values, time each function, and store the results
for n in n_values:
    # Time the Python function
    python_time = timeit.timeit(lambda: sum_of_squares(n), number=TRIALS)
    python_times.append(python_time / TRIALS)  # Average time per execution

    # Time the Cython function
    cython_time = timeit.timeit(lambda: sum_of_squares_cython(n), number=TRIALS)
    cython_times.append(cython_time / TRIALS)  # Average time per execution

    # Time the numba function
    numba_time = timeit.timeit(lambda: sum_of_squares_numb(n), number=TRIALS)
    numba_times.append(numba_time / TRIALS)  # Average time per execution

    # Time the numba function njit 
    numba_time_njit = timeit.timeit(lambda: sum_of_squares_numb_njit(n), number=TRIALS)
    numba_times_njit.append(numba_time_njit / TRIALS)  # Average time per execution

   
# Plot the results  
plt.figure(figsize=(10, 6))
plt.plot(n_values, python_times, label='Python', marker='o')
plt.plot(n_values, cython_times, label='Cython', marker='o')
plt.plot(n_values, numba_times, label='Numba jit', marker='o')
plt.plot(n_values, numba_times_njit, label='Numba njit', marker='o')
plt.plot(n_values, numba_times_njit_parallel, label='Numba njit parallel', marker='o')
plt.xlabel('Value of n')
plt.ylabel('Execution Time (seconds)')
plt.title('Execution Time Comparison: Python vs. Cython vs Numba')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()

# save to png 
plt.savefig('comparisons.png')

# %%
