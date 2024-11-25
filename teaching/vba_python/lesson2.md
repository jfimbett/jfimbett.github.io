---
marp: true
header: 'VBA and Python'
footer: 'Juan F. Imbet *Ph.D.*'
paginate: true
---

# Programming 1: VBA and Python

## Exercises to practice the basics of programming

---

# Exercise 1: Temperature conversion (30 minutes)

Write a program that converts from any of the following temperature units to any of the others: Celsius, Fahrenheit, and Kelvin. The program should ask the user for the temperature and the unit of the temperature, and then ask the user for the unit to which the temperature should be converted. The program should then display the converted temperature. You can interact with the user using the `InputBox` function or directly in the excel sheet.

---

## Some formulas 

- Celsius to Fahrenheit: $F = \frac{9}{5}C + 32$
- Celsius to Kelvin: $K = C + 273.15$

---

# Exercise 2: Prime numbers (30 minutes)

- You are going to replicate the Sieve of Eratosthenes algorithm in VBA. Here is the pseudocode:

```
Input: an integer n > 1

Let A be an array of Boolean values, indexed by integers 2 to n,
initially all set to true.

for i = 2, 3, 4, ..., not exceeding √n:
    if A[i] is true:
        for j = i^2, i^2+i, i^2+2i, i^2+3i, ..., not exceeding n:
            A[j] := false

Output: all i such that A[i] is true

```

