#%%
# Exercise 1

# Using basic Python, write a program that receives two objects, a function and a list of numbers. 
# The function needs to return the minimum, and the maximum of the function. 
# You cannot use the built-in functions min and max.

def min_max(func, numbers):
    min_ = numbers[0]
    max_ = numbers[0]
    for number in numbers:
        result = func(number)
        if min_ is None or result < min_:
            min_ = result
        if max_ is None or result > max_:
            max_ = result
    return min_, max_

# Create a test
assert min_max(lambda x: x**2, [1, 2, 3, 4, 5]) == (1, 25)
# %%
# Exercise 2
# Create a function that sorts a list of numbers in ascending order.
# You can sort a list by swapping elements one by one until the list is sorted.

def sort_list(numbers):
    
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] > numbers[j]:
                numbers[i], numbers[j] = numbers[j], numbers[i]
    return numbers
# Create a test
assert sort_list([3, 1, 2, 4, 5]) == [1, 2, 3, 4, 5]
# %%
# Exercise 3
# In this exercise you will perform a binary search on a sorted list of numbers.
# Given a list and a number you need to return the index
# The binary search algorithm works as follows:
# 1. Find the middle element in the list.
# 2. If the middle element is the number you are looking for, return it.
# 3. If the middle element is greater than the number you are looking for, repeat the process on the left half of the list.
# 4. If the middle element is smaller than the number you are looking for, repeat the process on the right half of the list.
# 5. If the number is not in the list, return None.

def binary_search(numbers, number):
    left = 0
    right = len(numbers) - 1
    while left <= right:
        middle = (left + right) // 2
        if numbers[middle] == number:
            return middle
        elif numbers[middle] > number:
            right = middle - 1
        else:
            left = middle + 1
    return None

# Create a test
assert binary_search([1, 2, 3, 4, 5], 3) == 2
# %%
