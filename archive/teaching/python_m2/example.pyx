# example.pyx
def sum_of_squares(int n):
    cdef long long total = 0
    cdef int i
    for i in range(1, n + 1):
        total += i * i
    return total
