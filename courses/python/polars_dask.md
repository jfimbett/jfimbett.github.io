---
marp: true
header: 'Python for Finance'
footer: 'Juan F. Imbet *Ph.D.*'
paginate: true
---


# Parallel programming - Polars and Dask

---

## Parallel programming

Breaking down larger problems into smaller, independen, that can be executed simultaneously.

---

## Fundamentals of Parallel Computer Architecture

* **Multi-core computing**: A multi-core processor has multiple processing cores on a single chip, which can execute instructions in parallel.

* **Symmetric multiprocessing (SMP)**: In SMP, two or more similar processors controlled by a single OS have equal access to a shared main memory and all common resources.

* **Distributed computing**: In this architecture, system components on different networked computers coordinate their actions through communication, often using HTTP or message queues.

* **Massively parallel computing**: This involves using a large number of computers or processors to execute computations in parallel.

---

![Polars](https://devio2022-media.developers.io/wp-content/uploads/2023/02/eyecatch-polars-1-960x504.png)

## Short Introduction to Polars

---

## Polars

Polars is a library for parallel data processing. It is useful for working with large datasets. Polars is imported using the `import` keyword. Polars is usually imported using the alias `pl`.

```python
import polars as pl
```

How is it coded? Polars is written in Rust, a low-level programming language. Rust is similar to C++, but it is safer and more efficient. Rust is used to write high-performance applications, including web browsers and operating systems.

---

## Polars - Dataframes

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

## Polars - Lazy evaluation

Polars uses lazy evaluation to improve performance. This means that operations are not executed until they are needed. This is useful for working with large datasets, because it allows the program to only load the data that is needed. Lazy evaluation is done using the `lazy` method. The `lazy` method has one argument: a function. The function is applied to the dataframe, and the result is returned.

```python
df = pl.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
df.lazy()
```

---

## Polars - General Instructions

Some instructions are similar to Pandas, however some other operations have a different syntax to connect to the Rust API.

## Creating dataframes

```python  
df = pl.read_csv('file.csv')
df = pl.read_parquet('file.parquet')
```

---

## Polars - Expressions

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

## Subset Observations - rows

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

## Subset Observations - rows (2)

```python
Select rst and last rows
# Select frst n rows
df.head(n=2)
# Select last n rows.
df.tail(n=2)
```

---

## Make New Columns

```python
df.with_columns(
    [
    (pl.col("a") * 2).alias("a_doubled"),
    (pl.col("b") + pl.col("a")).alias("a_plus_b"),
    (pl.col("c") / 2).alias("c_halved"),
    ]
)
```
