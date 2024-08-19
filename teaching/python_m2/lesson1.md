---
marp: true
header: 'Python for Finance'
footer: 'Juan F. Imbet *Ph.D.*'
paginate: true
---

# Python for Finance

## Juan F. Imbet *Ph.D.*

### Paris Dauphine University

### M203 (M2)

---

## Prerequisites

- Basic knowledge of Python
- Numpy, Pandas
- Object Oriented Programming

---

## Roadmap

- Session 1 (03/09) Introduction, Methodology, and Tools.
- Session 2 (10/09) Project: Backtesting and Blockchain.
- Session 3 (20/09) Backtesting Library 1: Numpy and Pandas.
- Session 4 (01/10) Backtesting Library 2: Portfolio Optimization.
- Session 5 (08/10) Backtesting Library 3: Risk Management.
- Session 6 (15/10) Blockchain Library 1: Foundations
- Session 7 (22/10) Blockchain Library 2: Conecting to the Backtesting Library
- Session 8 (19/11) User Interface

---

## Evaluation

- We will develop together during the following 8 sessions a project.
- As a final evaluation, you will have to extend the project with a new feature.

---

## How to Package a Python Project

- Develop an example Python package from start to finish
- Understand key steps involved in packaging
- Use as a reference for future Python packages

---

## `cookiecutter`

- `cookiecutter` is a command-line utility that creates projects from project templates.
- It is a tool that helps you to create a new project from a template.
- It takes a directory as input and copies it to a new directory, replacing all the variables in the files with values that you provide.
- We will use a standard template for Python packages.

---

## pybacktestchain (our library)

```bash
conda install -c conda-forge cookiecutter
```

Our goal is to create a package structure that looks like this

```text
pybacktestchain
├── CHANGELOG.md               ┐
├── CONDUCT.md                 │
├── CONTRIBUTING.md            │
├── docs                       │ Package documentation
│   └── ...                    │
├── LICENSE                    │
├── README.md                  ┘
├── pyproject.toml             ┐ 
├── src                        │
│   └── pybacktestcha          │ Package source code, metadata,
│       ├── __init__.py        │ and build instructions 
│       ├── moduleA.py         │
│       └── moduleB.py         ┘
└── tests                      ┐
    └── ...                    ┘ Package tests
```

---

## Package (2)

It might be confusing to see two directories with the package’s name (the root directory pycounts/ and the subdirectory src/pycounts/, but this is how Python packages are typically set up.

```bash
cookiecutter https://github.com/py-pkgs/py-pkgs-cookiecutter.git
```

---

## Package Information

```text
author_name [Monty Python]: Juan F. Imbet
package_name [mypkg]: pybacktestchain
package_short_description []: Backtesting meets Blockchain!
package_version [0.1.0]: 
python_version [3.9]: 
Select open_source_license:
1 - MIT
2 - Apache License 2.0
3 - GNU General Public License v3.0
4 - Creative Commons Attribution 4.0
5 - BSD 3-Clause
6 - Proprietary
7 - None
Choose from 1, 2, 3, 4, 5, 6 [1]: 
Select include_github_actions:
1 - no
2 - ci
3 - ci+cd
Choose from 1, 2, 3 [1]:
```

---

## Put your package under version control (See Slides Attached)

---

## Create a Virtual Environment

```bash
conda create --name pybacktestchain python=3.9 -y
conda activate pybacktestchain
```

---

## Install the Package using `poetry`

1. `poetry` is a tool for dependency management and packaging in Python.
2. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.

```bash
pip install poetry
poetry install
```

```output
Updating dependencies
Resolving dependencies... (0.1s)

Writing lock file

Installing the current project: pybacktestchain (0.1.0)
```

---

## Adding dependencies to your package

If you want to add a new dependency to your package, you can do so by running the following command:

```bash
poetry add matplotlib
```

---

```output
Using version ^3.4.3 for matplotlib

Updating dependencies
Resolving dependencies...

Writing lock file

Package operations: 8 installs, 0 updates, 0 removals

  • Installing six (1.16.0)
  • Installing cycler (0.10.0)
  • Installing kiwisolver (1.3.1)
  • Installing numpy (1.21.1)
  • Installing pillow (8.3.1)
  • Installing pyparsing (2.4.7)
  • Installing python-dateutil (2.8.2)
  • Installing matplotlib (3.4.3)
```

---

## .toml file

```toml
[tool.poetry.dependencies]
python = "^3.9"
matplotlib = "^3.4.3"
```

We can now use our package in a Python interpreter as follows

```python
from pybacktestchain.pybacktestchain import my_function
my_function()
```
