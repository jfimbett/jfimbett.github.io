---
marp: true
header: 'Python for Finance'
footer: 'Juan F. Imbet *Ph.D.*'
paginate: true
---

# Python: An Introduction
## Session 2

---
# File I/O

File I/O is used to read and write files. It is useful for storing data. File I/O is done using the `open` function. The `open` function has two arguments: a filename, and a mode. The mode is used to specify how the file should be opened. The mode can be `r` for reading, `w` for writing, `a` for appending, `r` for reading and writing, `b` for binary, and `+` for updating. The default mode is `r`.

```python
# Writing to a file
with open('file.txt', 'w') as f:
    f.write('Hello World')

# Reading from a file
with open('file.txt', 'r') as f:
    print(f.read())
```

---
# File I/O - Don't s

When dealing with files always use the `with` statement. This ensures that the file is closed properly. If you don't use the `with` statement, then you have to close the file manually.

```python
# Do not do this
f = open('file.txt', 'w')
f.write('Hello World')
f.close()
```

---
# Decorators

Decorators are used to modify the behavior of a function. They allow the program to modify the behavior of a function without changing the function itself. Decorators are done using the `@` symbol. The `@` symbol is used to specify a decorator. The decorator is a function that takes a function as an argument, and returns a function. The decorator can be used to modify the behavior of the function.

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        # Do something before
        func(*args, **kwargs)
        # Do something after
    return wrapper
```

---
# Useful decorators

Timing a function
```python
import time
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} took {end - start} seconds')
    return wrapper

@timer
def add(x, y):
    return x + y

add(1, 2)
```
```output
add took 0.0 seconds
```
---
# Useful decorators

Logging a function
```python
import logging
logging.basicConfig(level=logging.INFO)

def logger(func):
    def wrapper(*args, **kwargs):
        logging.info(f'Running {func.__name__} with args {args} and kwargs {kwargs}')
        func(*args, **kwargs)
    return wrapper
```

---
# Timeit

Timeit is used to time a function using the `timeit` module. 

```python
import timeit
timeit.timeit('1 + 1') # input has to be string
%timeit 1 + 1 # Computes the average and s.d. of different runs.
```

```output
0.01200000000000001
8.52 ns ± 0.00658 ns per loop (mean ± std. dev. of 7 runs, 100,000,000 loops each)
```

---
# Type hints

Type hints are used to specify the type of a variable. They allow the program to specify the type of a variable without changing the variable itself. Type hints are done using the `:` symbol. The `:` symbol is used to specify a type hint. Hints are not enforced by the interpreter, but they are useful for documentation and debugging.

```python

def add(x: int, y: int) -> int:
    z: int = x + y
    return z

add(1, 2)
add(1.0, 2) # No error
```

---
# Docstrings

Docstrings are used to document a function using the `"""` string. Try always to document your functions. Docstrings are useful for documentation and debugging. Use the following format for your docstrings. Most IDE will automatically show the docstring when you hover over a function and even help you to write it.

```python
def add(x: int, y: int) -> int:
    """Add two numbers

    Args:
        x (int): First number
        y (int): Second number

    Returns:
        int: Sum of x and y
    """
    z: int = x + y
    return z
```
Docstrings can be accessed using the function `help`.

---
# Machine Epsilon

Machine epsilon is the smallest number that can be added to 1.0 and still be different from 1.0. It is useful for determining the precision of a floating point number. Machine epsilon is done using the `sys` module. The `sys` module has many built-in functions, and it can also be customized to suit your needs.

```python
import sys
sys.float_info.epsilon # 2.220446049250313e-16
1.0 + sys.float_info.epsilon == 1.0 # False
1.0 + sys.float_info.epsilon/2 == 1.0 # True
```

---
# Week 2  NumPy, Matplotlib, Pandas.

---
# Community developed libraries

---

![Numpy](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/NumPy_logo.svg/1200px-NumPy_logo.svg.png)

---
# Numpy

Numpy is a library for scientific computing. It is useful for working with arrays and matrices. Most of its code is written in C, so it is very fast. Numpy is used in many scientific computing applications, including machine learning and deep learning. Numpy is imported using the `import` keyword. Numpy is usually imported using the alias `np`.

```python
import numpy as np
```

---
# Numpy arrays

Numpy arrays are used to store multiple items in a single variable. They can be created using the `np.array` function. Numpy arrays are similar to lists, but they are faster and more efficient. Numpy arrays can be created from lists, tuples, and other arrays.

```python
x = np.array([1, 2, 3])
```

```output
array([1, 2, 3])
```

---
# Numpy arrays are faster than lists

```python
x = list(range(1000000))
y = np.array(x)
%timeit sum(x) 
%timeit np.sum(y)
```

```output
4.92 ms ± 9.35 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
130 µs ± 75.3 ns per loop (mean ± std. dev. of 7 runs, 10,000 loops each)
```

---
# Why are numpy arrays faster than lists?

NumPy arrays are faster than lists because they are stored efficiently in memory, allowing for faster data access and manipulation. They also support vectorized operations, which are optimized and implemented in lower-level languages like C, making them much faster than equivalent Python loops. Additionally, NumPy takes advantage of CPU caching, optimized algorithms, and specialized functions, resulting in faster computations compared to pure Python list operations.

---
# Use numpy for linear algebra

Most common functions

```python
X = np.array([[1, 2, 3], [4, 5, 6]])
Y = np.array([[1, 2], [3, 4], [5, 6]])
x = np.array([1, 2, 3])

X.T # transpose
X@Y # matrix multiplication
X*X # element-wise multiplication
np.dot(X, Y) # matrix multiplication
np.matmul(X, Y) # matrix multiplication
np.vdot(x, x) # dot product
np.inner(x, x) # dot product
np.outer(x, x) # outer product
np.linalg.norm(x) # norm
np.linalg.det(X@Y) # determinant
np.linalg.inv(X@Y) # inverse
np.linalg.eig(X@Y) # eigenvalues and eigenvectors
np.linalg.svd(X@Y) # singular value decomposition


```

---
# Numpy types

Numpy allows to store data in different types. This is useful when you want to save memory, or when you want to perform operations on different types of data. Data types include int32, int64, float32, float64, bool, and object. The default data type is float64.

```python
x = np.array([1, 2, 3], dtype=np.int8)
x.dtype # dtype('int8')
``` 

---


![Matplotlib](https://matplotlib.org/stable/_static/images/logo2.svg)

---
# Matplotlib

Matplotlib is a library for plotting data. It is useful for visualizing data. Matplotlib is imported using the `import` keyword. Matplotlib is usually imported using the alias `plt`.

```python
import matplotlib.pyplot as plt
# or
from matplotlib import pyplot as plt
```

---
# Matplotlib - Most common plots

* Line plot - `plt.plot`
* Scatter plot - `plt.scatter`
* Bar plot - `plt.bar`
* Histogram - `plt.hist`
* Box plot - `plt.boxplot`
* Pie chart - `plt.pie`

Matplotlib is a very powerful library. Graphs can be customized in many ways, and a complete guide would be too long. 

---
# Customizing plots

* `plt.title` - Set the title of the plot
* `plt.xlabel` - Set the label for the x-axis
* `plt.ylabel` - Set the label for the y-axis
* `plt.rotate` - Rotate the x-axis labels
* `plt.legend` - Show the legend
* `plt.show` - Show the plot

Check out the examples [here](https://matplotlib.org/stable/gallery/index.html)


---

![Pandas](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/1200px-Pandas_logo.svg.png)

---
# Pandas

Pandas is a library for data analysis. Probably the most used library in data science. Pandas is imported using the `import` keyword. Pandas is usually imported using the alias `pd`.

```python
import pandas as pd
```

Dataframes are the main data structure in Pandas. They are used to store tabular data. They can be created using the `pd.DataFrame` function. Dataframes can be created from lists, tuples, dictionaries, and other dataframes. It is common to name dataframes `df`.

```python
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
```

```output
   a  b
0  1  4
1  2  5
2  3  6
```

---
# Pandas - Load data from a file

Pandas can load data from CSV files, JSON files, Excel files, parquet files, and SQL databases.

```python
df = pd.read_csv('file.csv')
df = pd.read_json('file.json')
df = pd.read_excel('file.xlsx')
df = pd.read_sql('SELECT * FROM table', connection)
df = pd.read_parquet('file.parquet')
```

---
# Pandas - miscellaneous

Pandas can load data from a URL.

```python
df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
```

Pandas and NumPy are closely related. Pandas is built on top of NumPy, and it uses NumPy arrays to store data. Pandas can convert dataframes to NumPy arrays using the `to_numpy` method.

```python
df.to_numpy()
```

---
# Dataframe indexing

Dataframes can be indexed using the `iloc` and `loc` methods. The `iloc` method is used to index dataframes by position. The `loc` method is used to index dataframes by label. Dataframes can also be indexed using the `[]` operator. The `[]` operator is used to index dataframes by label.

Using `iloc`
```python
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
df.iloc[0] # First row
df.iloc[0, 0] # First element of first row
df.iloc[:, 0] # First column
df.iloc[0:2] # First two rows
df.iloc[0:2, 0:2] # First two rows and columns
df.iloc[[0, 2]] # First and third row
df.iloc[[0, 2], [0, 2]] # First and third row and column
df.iloc[lambda x: x.index % 2 == 0] # Even rows
df.iloc[lambda x: x.index % 2 == 0, lambda x: x.columns % 2 == 0] # Even rows and columns
```

---
# Dataframe indexing

Using `loc`

```python
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
df.loc[0] # First row
df.loc[0, 'a'] # First element of first row
df.loc[:, 'a'] # First column
df.loc[0:2] # First two rows
df.loc[0:2, 'a':'b'] # First two rows and columns
df.loc[[0, 2]] # First and third row
df.loc[[0, 2], ['a', 'b']] # First and third row and column
df.loc[lambda x: x.index % 2 == 0] # Even rows
df.loc[lambda x: x.index % 2 == 0, lambda x: x.columns % 2 == 0] # Even rows and columns
```

---
# Data operations

Dataframes can be modified using the `assign` method. The `assign` method is used to modify dataframes by adding new columns. Dataframes can also be modified using the `[]` operator. The `[]` operator is used to modify dataframes by adding new columns.

```python
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
df['c'] = df.a + df.b # Add a new column
df['c'] = df['a'] + df['b'] # Add a new column
```

Columns can be accessed using the `[]` operator. The `[]` operator is used to access columns by label. Columns can also be accessed using the `.` operator. The `.` operator is used to access columns by label. The `.` operator cannot be used to describe a column that does not exist, and cannot be used to describe a column with a reserved name. E.g. `df.dtype` is not a valid column.

---
# Inplace vs not inplace

Dataframes can be modified inplace or not inplace. The `inplace` parameter is used to specify whether or not the dataframe should be modified inplace. The `inplace` parameter has two possible values: `True` and `False`. For efficiency reasons, it is recommended to not modify dataframes inplace.

```python
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
df.rename(columns={'a': 'A'}, inplace=True) # Modify inplace
df = df.rename(columns={'a': 'A'}) # Modify not inplace
```

---
## The `groupby` operation produces a `DataFrameGroupBy` object

```python
df = pd.DataFrame({'group': ['A', 'A', 'B', 'B'], 'value': [1, 2, 3, 4]})
df.groupby('group')

```
    
```output
<pandas.core.groupby.generic.DataFrameGroupBy object at 0x7f8e1c0b5d90>
 ```

 ---
 ## `apply` and custom functions

    The `apply` method is used to apply a function to a dataframe. The `apply` method has two arguments: a function, and an axis. The function is applied to each row or column of the dataframe. The axis is used to specify whether the function should be applied to each row or column. The axis can be `0` for rows, or `1` for columns. The default axis is `0`.
    
```python
df = pd.DataFrame({'group': ['A', 'A', 'B', 'B'], 'value': [1, 2, 3, 4]})
df.groupby('group').apply(lambda x: x.value.sum())
# or
df.groupby('group')['value'].apply(lambda x: x.sum())
# or
df.groupby('group').value.sum()
```

```output
group
A    3
B    7
```

---
# Week 3
# Parallel programming - Polars and Dask
---

# Parallel programming

Breaking down larger problems into smaller, independen, that can be executed simultaneously.

---

# Fundamentals of Parallel Computer Architecture

* **Multi-core computing**: A multi-core processor has multiple processing cores on a single chip, which can execute instructions in parallel. 

* **Symmetric multiprocessing (SMP)**: In SMP, two or more similar processors controlled by a single OS have equal access to a shared main memory and all common resources. 

* **Distributed computing**: In this architecture, system components on different networked computers coordinate their actions through communication, often using HTTP or message queues. 

* **Massively parallel computing**: This involves using a large number of computers or processors to execute computations in parallel. 


---

![Polars](https://devio2022-media.developers.io/wp-content/uploads/2023/02/eyecatch-polars-1-960x504.png)

# Short Introduction to Polars

---
# Polars

Polars is a library for parallel data processing. It is useful for working with large datasets. Polars is imported using the `import` keyword. Polars is usually imported using the alias `pl`.

```python
import polars as pl
```

How is it coded? Polars is written in Rust, a low-level programming language. Rust is similar to C++, but it is safer and more efficient. Rust is used to write high-performance applications, including web browsers and operating systems.

---
# Polars - Dataframes

Dataframes are the main data structure in Polars. They are used to store tabular data. They can be created using the `pl.DataFrame` function. Dataframes can be created from lists, tuples, dictionaries, and other dataframes. It is common to name dataframes `df`.

```python
df = pl.DataFrame({'a': [1], 'b': [4]})
```

```output
shape: (3, 2)
┌─────┬─────┐
│ a   ┆ b   │
│ --- ┆ --- │
│ i64 ┆ i64 │
╞═════╪═════╡
│ 1   ┆ 4   │
╞═════╪═════╡
```

---
# Polars - Lazy evaluation

Polars uses lazy evaluation to improve performance. This means that operations are not executed until they are needed. This is useful for working with large datasets, because it allows the program to only load the data that is needed. Lazy evaluation is done using the `lazy` method. The `lazy` method has one argument: a function. The function is applied to the dataframe, and the result is returned.

```python
df = pl.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
df.lazy()
```

---
# Polars - General Instructions

Some instructions are similar to Pandas, however some other operations have a different syntax to connect to the Rust API. 

## Creating dataframes
    
```python  
df = pl.read_csv('file.csv')
df = pl.read_parquet('file.parquet')
```

---
# Polars - Expressions

Expressions can be performed in sequence, this improves readability. You can use the `\` character to split code, or use parenthesis (**recommended**).

* Use `filter` to mask observations. 
* Use `pl.col` to select a column.
* Use methos inside `pl` to perform operations on columns. E.g. `pl.col('a').sum()`.

Example of Polars code
```python
df = (df 
    .filter(pl.col('a') > 0)
    .select(pl.col('a'), pl.col('b'))
    .groupby(pl.col('a'))
    .agg([pl.col('b').sum().alias('sum_b')])
)
```

---
# Subset Observations - rows
Filter: Extract rows that meet logical criteria.
```python
df.flter(pl.col("random") > 0.5)
df.flter(
(pl.col("groups")  "B")
& (pl.col("random") > 0.5) 
)
```

Sample 
```python
# Randomly select fraction of rows.
df.sample(frac=0.5)
# Randomly select n rows.
df.sample(n=2)
```

---
# Subset Observations - rows

```python
Select rst and last rows
# Select frst n rows
df.head(n=2)
# Select last n rows.
df.tail(n=2)
```

---
# Make New Columns

```python
df.with_columns(
    [
    (pl.col("a") * 2).alias("a_doubled"),
    (pl.col("b") + pl.col("a")).alias("a_plus_b"),
    (pl.col("c") / 2).alias("c_halved"),
    ]
)
```



---
# Week 4
# Object Oriented Programming

---
# Object Oriented Programming

Object Oriented Programming is a programming paradigm that uses objects and classes. It is useful for creating reusable code, and it can also be used to create complex programs. Object Oriented Programming is done using the `class` keyword. Classes are used to create objects, which are instances of a class. Objects can have attributes and methods. Attributes are variables that belong to an object, and methods are functions that belong to an object.

```python
class Asset:
    pass
```

---
# Constructor

A constructor is a special method that is used to initialize an object. It is useful for creating objects with default values. Constructors are done using the `__init__` method. The `__init__` method has two arguments: `self` and `args`. The `self` argument is used to refer to the object itself, and the `args` argument is used to pass arguments to the constructor. The `__init__` method is called when an object is created.

```python
class Asset:
    def __init__(self, name, price):
        self.name = name
        self.price = price

asset = Asset('Bitcoin', 50000)
```

---
# Attributes

Attributes are variables that belong to an object. They are useful for storing information about an object. Attributes can be accessed using the `.` operator. Attributes can also be accessed using the `getattr` function. Attributes can be set using the `=` operator. Attributes can also be set using the `setattr` function. Attributes can be deleted using the `del` operator. Attributes can also be deleted using the `delattr` function.

```python
asset.name # Get attribute
asset.price = 60000 # Set attribute
asset.type = 'Cryptocurrency' # Set attribute not defined in constructor
```

---
# Methods

Methods are functions that belong to an object. Methods can be called using the `()` operator. Since they are functions they are defined using the `def` keyword and always contain the `self` argument first.

```python
class Asset:
    ...

    def double_price(self):
        return self.price*2

```

---
# Dunders (Magic methods)

Dunders are special methods that are used to avoid operator overloading. They are useful for creating objects that behave like built-in objects. Dunders are done using the `__` keyword. For example, the `+` operator can be used to add two numbers, but it can also be used to add two strings. 

```python
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

v1 = Vector2D(1, 2)
v2 = Vector2D(3, 4)
v3 = v1 + v2
```

---
# Dunders (Magic methods)
Non-exhaustive list of dunders

```python
__init__ # Constructor
__str__ # String representation
__add__ # Addition + 
__sub__ # Subtraction -
__mul__ # Multiplication *
__truediv__ # Division /
__floordiv__ # Floor division //
__mod__ # Modulo %
__pow__ # Exponentiation **
__lt__ # Less than <
__le__ # Less than or equal to <=
__eq__ # Equal to ==
__ne__ # Not equal to !=
__gt__ # Greater than >
__ge__ # Greater than or equal to >=
```

---

# Example: Portfolio Class

A portfolio consists of a list of assets. Each asset has a name (identifier) as well as a history of prices. 

```python
class Asset:

    self.mu = np.nan # Expected return
    self.sigma = np.nan # Volatility

    def __init__(self, name: str, price_history: pd.DataFrame):
        self.name = name
        self.price_history = price_history
        self.compute_mu()
        self.compute_sigma()

    def compute_mu(self):
        self.mu = self.price_history.pct_change().mean()
    
    def compute_sigma(self):
        self.sigma = self.price_history.pct_change().std()

```

---
# Example: Portfolio Class

```python
class Portfolio:

    self.mu = np.nan # Expected return
    self.sigma = np.nan # Volatility

    def __init__(self, assets: List[Asset], weights: List[float]):
        self.assets = assets
        self.weights = weights
        self.compute_mu()
        self.compute_sigma()

    def compute_mu(self):
        self.mu = np.sum([asset.mu * weight for asset, weight in zip(self.assets, self.weights)])
    
    def compute_sigma(self):
        # Covariance matrix
        cov = np.cov([asset.price_history.pct_change().dropna() for asset in self.assets])
        # Weighted covariance matrix
        cov = np.diag(self.weights) @ cov @ np.diag(self.weights)
        # Portfolio volatility
        self.sigma = np.sqrt(np.diag(cov).sum())

```
        
---
# Algorithm Analysis

---
# What is an algorithm

An algorithm is a set of instructions that are used to solve a problem. 

**Example**
Find the maximum value in a list of numbers. 

1. Set the maximum value to the first value in the list.
2. For each value in the list, if the value is greater than the maximum value, then set the maximum value to that value.
3. Return the maximum value after looking at all values in the list.

---
# How can we compare algorithms?

* **Time complexity** - How long does it take to run the algorithm?
* **Space complexity** - How much memory does the algorithm use?
* **Correctness** - Does the algorithm solve the problem, or does it approximate the solution?

---
# Big O Notation

One way to compare algorithms is by understanding its behavior as the size of the problem increases. Big O notation is used to describe the time complexity of an algorithm. 

We say an algorithm has a time complexity $O(f(n))$ if the number of operations is bounded by $Cf(n)$ for some constant $C$ and for all $n$ greater than some constant $n_0$.

$$
O(f(n)) = \{g(n) : \exists C > 0, \exists n_0 > 0, \forall n > n_0, 0 \leq g(n) \leq Cf(n)\}
$$

They normally considered the amount of stpes that the algorithm has to perform in the worst case scenario. E.g. sorting a list that is in reverse order.

---
# Examples of Big O Notation

* $O(1)$ - Constant time, and algorithm that always takes the same amount of time to run. E.g. accessing an element in an array.

```python
a = range(1000000)
%timeit a[0] # O(1)
%timeit a[500000] # O(1)
```
Differences are due to CPU caching, practically they are the same.

```output
66.8 ns ± 0.124 ns per loop (mean ± std. dev. of 7 runs, 10,000,000 loops each)
86.2 ns ± 0.192 ns per loop (mean ± std. dev. of 7 runs, 10,000,000 loops each)
```
        
---
# Examples of Big O Notation

* $O(n)$ - Linear time, an algorithm that takes $n$ steps to run. E.g. find the maximum value in a list of numbers.

```python
import random
random.seed(0)
a = [random.random() for _ in range(1000)]
%timeit max(a) # O(n)
a = [random.random() for _ in range(1000000)]
%timeit max(a) # O(n)
```
Second examples takes 1000 times longer.
$1 ms = 1000 \mu s$
```output
12.1 µs ± 4.11 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
12 ms ± 10.8 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

---
# Examples of Big O Notation

* $O(n^2)$ - Quadratic time, an algorithm that takes $n^2$ steps to run. Sort a list of numbers using bubble sort.

```python

import random
random.seed(0)
a = [random.random() for _ in range(1000)]
%timeit bubble_sort(a) # O(n^2)
a = [random.random() for _ in range(10000)]
%timeit bubble_sort(a) # O(n^2)
```
Increasing the size ten times increases the time by 100 times.

```output
37 ms ± 107 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
4.09 s ± 24.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

$$
\frac{4.09 s}{37 ms} = 110.54
$$

---
# Appendix: Bubble Sort

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

--- 
# Polynomial time 

When an algorithm has a time complexity of $O(n^k)$ for some constant $k$, we say it has polynomial time. Polynomial time algorithms are considered efficient.

**Example** NumPy's matrix inversion is approximately $O(n^{3})$. This means that increasing the size of the matrix by 10 times increases the time by 1000 times.

**DO NOT RUN IN A SLOW COMPUTER**

```python
import numpy as np
import random
random.seed(0)
a = np.random.rand(1000, 1000)
%timeit np.linalg.inv(a) # O(n^3)
a = np.random.rand(100000, 100000)
%timeit np.linalg.inv(a) # O(n^3)
```


---
# Logarithmic time

When an algorithm has a time complexity of $O(\log n)$, we say it has logarithmic time. Logarithmic time algorithms are considered efficient.

**Example** Binary search is a search algorithm that finds the position of a target value within a sorted array. Increasing the size by 1000 barely changes the time.

```python
a = range(1000000)
%timeit binary_search(a, 500000) # O(log n)
a = range(1000000000)
%timeit binary_search(a, 500000) # O(log n)
```

```output
5.18 µs ± 9.36 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
7.79 µs ± 72 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
```

---
# Appendix: Binary Search

```python
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] < target:
            low = mid + 1
        elif arr[mid] > target:
            high = mid - 1
        else:
            return mid
    return -1
```

---
# Exponential time

When an algorithm has a time complexity of $O(2^n)$, we say it has exponential time. Exponential time algorithms are considered inefficient.

**Example** The Power Set problem involves finding all possible subsets of a given set, including the empty set and the set itself. For a set with n elements, the number of subsets is $2^n$, which grows exponentially with the size of the set. An extra element almost doubles the time.

```python
s = range(5)
%timeit generate_power_set(s) # O(2^n)
s = range(6)
%timeit generate_power_set(s) # O(2^n)
```

```output
6.05 µs ± 18.8 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
10.7 µs ± 20.2 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
```


---
# Appendix: Compute the Power Set

```python
def generate_power_set(s):
    if len(s) == 0:
        return [[]]  # Base case: empty set has one subset, which is the empty set
    
    subsets = []
    first_element = s[0]
    remaining_elements = s[1:]
    
    # Recursive call to generate subsets without the first element
    subsets_without_first = generate_power_set(remaining_elements)
    
    # Combine subsets without the first element with subsets including the first element
    for subset in subsets_without_first:
        subsets.append(subset)  # Add subset without the first element
        subsets.append([first_element] + subset)  # Add subset including the first element
    
    return subsets
```

---
# Factorial time

When an algorithm has a time complexity of $O(n!)$, we say it has factorial time. Factorial time algorithms are considered inefficient.

One example of an algorithm with a time complexity of $O(n!)$ is the brute-force solution for the permutation problem. The permutation problem involves finding all possible permutations of a given set of elements.

```python
s = list(range(5))
%timeit generate_permutations(s) # O(n!)
s = list(range(6))
%timeit generate_permutations(s) # O(n!)
```

```output
137 µs ± 291 ns per loop (mean ± std. dev. of 7 runs, 10,000 loops each)
822 µs ± 587 ns per loop (mean ± std. dev. of 7 runs, 1,000 loops each)
```

$822/137 = 6$


---
# Appendix: Compute the Permutations

```python
def generate_permutations(elements):
    permutations = []
    generate_permutations_recursive(elements, [], permutations)
    return permutations

def generate_permutations_recursive(elements, current_permutation, permutations):
    if len(elements) == 0:
        permutations.append(current_permutation)
    else:
        for i in range(len(elements)):
            remaining_elements = elements[:i] + elements[i+1:]
            new_permutation = current_permutation + [elements[i]]
            generate_permutations_recursive(remaining_elements, new_permutation, permutations)
```

---
# Numerical Optimization

---
# Preliminaries

Consider the following optimization problem
$$
\min_{x \in \mathbb{R}^n} f(x)
$$
where $f: \mathbb{R}^n \to \mathbb{R}$ is a function. The function $f$ is called the objective function. The set $\mathbb{R}^n$ is called the feasible set. The vector $x$ is called the decision variable. The vector $x^*$ is called the optimal solution. The scalar $f(x^*)$ is called the optimal value. The optimization problem is called a minimization problem. A maximization problem is defined similarly.

---
# Convex optimization

A convex optimization problem is an optimization problem where the objective function is convex, and the feasible set is convex. A convex function is a function where the line segment between any two points on the graph of the function lies above the graph. A convex set is a set where the line segment between any two points in the set lies in the set. Convex optimization problems are easy to solve because they have a unique global minimum.

---
# Solving convex optimization problems

Convex optimization problems can be solved using the gradient descent algorithm. The gradient descent algorithm is an iterative algorithm that starts at a random point and moves in the direction of the negative gradient until it reaches a local minimum. The gradient descent algorithm is guaranteed to converge to a local minimum if the objective function is convex and the feasible set is convex. The gradient descent algorithm is guaranteed to converge to the global minimum if the objective function is convex and the feasible set is convex and compact.

---
# Gradient descent

$$
x_{k+1} = x_k - \alpha_k \nabla f(x_k)
$$
where $x_k$ is the current point, $x_{k+1}$ is the next point, $\alpha_k$ is the step size, and $\nabla f(x_k)$ is the gradient of the objective function at the current point. The step size is a hyperparameter that controls how fast the algorithm moves towards the minimum. The step size can be constant or variable. The step size is constant if it does not change during the algorithm. The step size is variable if it changes during the algorithm. The step size can be chosen using more advanced methods such as line search or backtracking line search.

---
# Quick gradient descent example in Python

```python
import numpy as np

f = lambda x: x**2
df = lambda x: 2*x

x = 10
alpha = 0.1
tol = 1e-6
max_iter = 1000

while True:
    x_new = x - alpha*df(x)
    if np.abs(x_new - x) < tol:
        break
    x = x_new
```

---
# Optimization in Python: SciPy

![SciPy](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/SCIPY_2.svg/500px-SCIPY_2.svg.png)




---

$$
\min_{x \in \mathbb{R}^2} f(x) = x_1^2 + x_2^2
$$

```python
import numpy as np
from scipy.optimize import minimize
f = lambda x: x[0]**2 + x[1]**2
x0 = np.array([10, 10])
res = minimize(f, x0)
print(res)
```
```output
      fun: 9.714371410949269e-13
 hess_inv: array([[ 0.75000002, -0.24999998],
       [-0.24999998,  0.75000002]])
      jac: array([-1.37896909e-06, -1.37896909e-06])
  message: 'Optimization terminated successfully.'
     nfev: 12
      nit: 2
     njev: 4
   status: 0
  success: True
        x: array([-6.96935126e-07, -6.96935126e-07])
```

---
# Performance, how fast is SciPy?

```python
import numpy as np
def my_minimize(f, x0, alpha = 0.1, tol = 1e-6, max_iter = 1000):
    df = lambda x: (f(x + tol) - f(x - tol))/(2*tol)
    x = x0
    for _ in range(max_iter):
        x_new = x - alpha*df(x)
        if np.max(np.abs(x_new - x)) < tol:
            break
        x = x_new
    return x
```

---
# Profiling, knowing the derivative accelerates convergence

```python
import numpy as np
from scipy.optimize import minimize
f = lambda x: x**2
x0 = 10
%timeit minimize(f, x0, tol=1e-6, options={'maxiter': 1000})
%timeit my_minimize(f, x0, tol=1e-6, alpha=0.1, max_iter=1000)
```

```output
588 µs ± 1.32 µs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)
358 µs ± 1.08 µs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)
```

---
# Scipy when the Jacobian is known

```python
import numpy as np
from scipy.optimize import minimize
f = lambda x: x[0]**2 + x[1]**2
df = lambda x: np.array([2*x[0], 2*x[1]])
x0 = np.array([10, 10])
res = minimize(f, x0, jac=df)
print(res)
```

```output
 fun: 1.5777218104420236e-30
 hess_inv: array([[ 0.75, -0.25],
       [-0.25,  0.75]])
      jac: array([-1.77635684e-15, -1.77635684e-15])
  message: 'Optimization terminated successfully.'
     nfev: 4
      nit: 2
     njev: 4
   status: 0
  success: True
        x: array([-8.8817842e-16, -8.8817842e-16])
```

---
# Numerical Differentiation

Computing the derivative of a function numerically is useful when the derivative is not known analytically. The derivative of a function $f: \mathbb{R}^n \to \mathbb{R}$ at a point $x \in \mathbb{R}^n$ is defined as

$$
\nabla f(x) = \left[\frac{\partial f}{\partial x_1}(x), \frac{\partial f}{\partial x_2}(x), \dots, \frac{\partial f}{\partial x_n}(x)\right]
$$

where $\frac{\partial f}{\partial x_i}(x)$ is the partial derivative of $f$ with respect to $x_i$ at $x$. The partial derivative of $f$ with respect to $x_i$ at $x$ is defined as

$$
\frac{\partial f}{\partial x_i}(x) = \lim_{h \to 0} \frac{f(x + he_i) - f(x)}{h}
$$

where $e_i$ is the $i$-th standard basis vector. The partial derivative of $f$ with respect to $x_i$ at $x$ is the slope of the tangent line of $f$ at $x$ in the direction of $e_i$.

---
# Numerical Differentiation

The partial derivative of $f$ with respect to $x_i$ at $x$ can be approximated using the forward difference formula

$$
\frac{\partial f}{\partial x_i}(x) \approx \frac{f(x + he_i) - f(x)}{h}
$$

where $h$ is a small number. It can also be approximated using the backward difference formula

$$
\frac{\partial f}{\partial x_i}(x) \approx \frac{f(x) - f(x - he_i)}{h}
$$
 It can also be approximated using the central difference formula

$$
\frac{\partial f}{\partial x_i}(x) \approx \frac{f(x + he_i) - f(x - he_i)}{2h}
$$

where $h$ is a small number. The central difference formula is more accurate than the forward difference formula and the backward difference formula.

---
# Numerical Differentiation, higher order derivatives

The second partial derivative of $f$ with respect to $x_i$ and $x_j$ at $x$ is defined as

$$
\frac{\partial^2 f}{\partial x_i \partial x_j}(x) = \lim_{h \to 0} \frac{\frac{\partial f}{\partial x_i}(x + he_j) - \frac{\partial f}{\partial x_i}(x)}{h}
$$

where $\frac{\partial f}{\partial x_i}(x + he_j)$ is the partial derivative of $f$ with respect to $x_i$ at $x + he_j$. The second partial derivative of $f$ with respect to $x_i$ and $x_j$ at $x$ can be approximated using the central difference formula

---
# Numerical Differentiation, higher order derivatives

Replacing the partial derivative of $f$ with respect to $x_i$ at $x$ with the central difference formula gives

$$
\frac{\partial^2 f}{\partial x_i \partial x_j}(x) \approx \frac{\frac{f(x + he_i + he_j) - f(x + he_j)}{h} - \frac{f(x + he_i) - f(x)}{h}}{h}
$$
arranging terms
$$
\frac{\partial^2 f}{\partial x_i \partial x_j}(x) \approx \frac{f(x + he_i + he_j) - f(x + he_i) - f(x + he_j) + f(x)}{h^2}
$$

---
# Differentiation in Python

```python
import numpy as np
def df(f, h=1e-6):
    return lambda x: (f(x + h) - f(x - h))/(2*h)
```

Differentiation plays a key role in training and tuning machine learning models. Even LLM uses differentiation to compute the optimal weights.

---
# Non-convex optimization

A non-convex optimization problem is an optimization problem where the objective function is non-convex, or the feasible set is non-convex. Non-convex optimization problems are difficult to solve because they have multiple local minima. The gradient descent algorithm is not guaranteed to converge to the global minimum if the objective function is non-convex or the feasible set is non-convex.

---
# Non-convex optimization

![Non-convex optimization](https://upload.wikimedia.org/wikipedia/commons/e/e3/Non-Convex_Objective_Function.gif?20181130000341)

How to solve non-convex optimization problems? Escape local minima using random restarts. 

---
# Heuristics and metaheuristics

A heuristic is a technique that is used to solve a problem. A metaheuristic is a heuristic that is used to solve a class of problems. 

Simplest metaheuristic: **random local search**. Start at a random point and move in a random direction until a local minimum is reached. Repeat the process multiple times and keep the best solution.

---
# Coding a random local search in Python

```python
import numpy as np
def random_local_search(f, x0, alpha = 0.1, tol = 1e-6, max_iter = 1000):
    x = x0
    for _ in range(max_iter):
        x_new = x - alpha*np.random.randn(*x.shape)
        if np.max(np.abs(x_new - x)) < tol:
            break
        x = x_new
    return x
```

---
# Calling C code from Python

```python
import ctypes
lib = ctypes.CDLL('./lib.so')
lib.add.argtypes = (ctypes.c_int, ctypes.c_int)
lib.add.restype = ctypes.c_int
lib.add(1, 2)
```

```output
3
```

---
# Web scraping

---
# Web scraping: Basics of HTML

HTML is a markup language that is used to create web pages. HTML is used to describe the structure of a web page. HTML is done using tags. Tags are used to describe the structure of a web page. Tags are enclosed in angle brackets. Tags can be nested inside other tags. Tags can have attributes. Attributes are used to describe the properties of a tag. 

---
# Web scraping: Basics of HTML

```html
<!DOCTYPE html>
<html>
    <head>
        <title>Page Title</title>
    </head>
    <body>
        <h1>My First Heading</h1>
        <p>My first paragraph.</p>
    </body>
</html>

```

---
# Web scraping: CSS 
 CSS is done using selectors. Selectors can be used to select elements by tag name, class, or id. 

```css
/* Select all elements */
* {
    color: red;
}
/* Select all h1 elements */
h1 {
    color: red;
}
/* Select all elements with class="example" */
.example {
    color: red;
}
/* Select the element with id="example" */
#example {
    color: red;
}
```

---
# HTTP Requests

HTTP is a protocol that is used to send and receive data over the internet. HTTP is done using requests. Requests are sent to a server. Requests have a method and a URL. The method is used to specify the type of request. The URL is used to specify the location of the resource. The server responds with a response. The response has a status code and a body. The status code is used to specify the status of the request. The body is used to specify the data that was sent.

---
# GET, POST, PUT, DELETE

* **GET** - Requests data from a specified resource
* **POST** - Submits data to be processed to a specified resource
* **PUT** - Updates a specified resource
* **DELETE** - Deletes a specified resource

---
# Example: GET request

```python
import requests
url = 'https://www.google.com'
response = requests.get(url)
print(response.status_code)
print(response.text)
```

```output
200
<!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="es-419">
<head>...
```

---
# Example Post request

```python
import requests
url = 'https://httpbin.org/post'
data = {'key1': 'value1', 'key2': 'value2'}
response = requests.post(url, data=data)
print(response.status_code)
print(response.text)
```

```output
200
{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "key1": "value1", 
    "key2": "value2"
  }, 
...
}
```

---
# Put and Delete requests

```python
import requests
url = 'https://httpbin.org/put'
data = {'key1': 'value1', 'key2': 'value2'}
response = requests.put(url, data=data)
print(response.status_code)
print(response.text)
```

```python
import requests
url = 'https://httpbin.org/delete'
response = requests.delete(url)
print(response.status_code)
print(response.text)
```

---
# Good practice

Check the status code before parsing the response.

```python
import requests
url = 'https://www.google.com'
response = requests.get(url)
if response.status_code == 200:
    print(response.text)
else:
    raise Exception(f"Error: {response.status_code}")
```

---
# Headers

Not all websites allow you to communicate with them through a browserless environment. Some websites require you to specify a user agent. A user agent is a string that is used to identify the browser and operating system that is being used. A user agent can be specified using the headers argument.

```python
import requests

url = 'http://sec.gov'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
response = requests.get(url, headers=headers)
print(response.status_code)
```

---
# Signing in

Some websites require you to sign in before you can access the data. You can sign in using the requests library. You can use the session object to keep track of the cookies. You can use the cookies argument to specify the cookies that you want to send.

---

```python
import requests

# some website that requires username and password
url = 'http://httpbin.org/basic-auth/user/passwd'

# create session object
session = requests.Session(
# sign in
session.auth = ('user', 'passwd')
# send request
response = session.get(url)
# print response
print(response.status_code)
print(response.text)
```

```output
200
{
  "authenticated": true, 
  "user": "user"
}
```

---
# Ok, so we get all the HTML, now what?

We need to parse the HTML to extract the data that we want. We can use the BeautifulSoup library to parse the HTML. 

```python
import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.google.com'
response = requests.get(url)
soup = bs(response.text, 'html.parser')
print(soup.prettify())
```
---
# HTML as a tree
```output
<div id="guser" width="100%">
    <nobr>
     <span class="gbi" id="gbn">
     </span>
     <span class="gbf" id="gbf">
     </span>
     <span id="gbe">
     </span>
     <a class="gb4" href="http://www.google.com.co/history/optout?hl=es-419">
      ...
```

---
# My take on how to traverse the tree

Use the `find_all` method, and specify the tag name, class, or id. 

```python
soup = bs(response.text, 'html.parser')
soup.find_all('a')
soup.find_all('a', class_='gb4')
soup.find_all('a', id='gb_70')
```

Recall that `find_all` always returns a list, even if there is only one element.




