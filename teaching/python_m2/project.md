---
marp: true
header: 'Project '
footer: 'Juan F. Imbet'
paginate: true
---

# Project

---
## Overview

- The latest version of the project we have been working on during the course can be installed directly using `pip`. 
```bash
pip install pybacktestchain
```

You can see the source code/ documentation in https://pypi.org/project/pybacktestchain/. 

- Your main goal is to create your own python package, which will import `pybacktestchain` to implement new functionalities. 

- All projects have to be implemented individually. 

---
## Project Basics

- Package structure from `cookiecutter` template.
- Package dependencies using `poetry`.
- Version control with `semantic-release`.
- If you need to refresh anything, refer to the slides or the following documentation https://py-pkgs.org/welcome
- Part of the requirements is to be able to have a history of the changes made to the package.
- Tests
- Proper documentation (all .md files)
- Follow the instructions in the link above to publish your package in `pypi`, do not try to publish in `test-pypi`, it is not worth it and is not reliable. 

---

## Project Requirements

- Create a new package that imports `pybacktestchain` and implements new functionalities. (You can create new functions or overwrite existing ones) E.g. 
    - Functionality with new asset classes together with their respective data structures and investment strategies. 
    - A properly developed user interface to interact with the package.
    - C-implementation of the main functions of the package.
    - A cryptocurrency implementation on the blockchain that compensates adding new blocks or profitable backtest ideas. 
    - Proper distributed computing implementation to backtest strategies in parallel.
    - Web services to backtest and collaborate with the development of investment strategies in a team. 

---
## What do I expect from you?

- Same standards as seen in class. Proper documentation, usage of version control, and code quality. Check the official style guide for python code if required https://peps.python.org/pep-0008/
- You can use LLMs to help you code, but you must understand what you are doing. I also use LLMs to code, so I will know if you understand or not the code. 
- Originality, you have enough time to develop something new and interesting.
- Having all the development process documented in the repository really supports your cv in job applications.
- If you are not sure if your idea is good or not, send me an email and visit me during office hours.
- Your grade will be based on your project having the minimum requirements and the originality/implementation of the idea. 

---
## Project Deliverables

- Github repository with the package.
- Package published in `pypi`.
- Send me an email with both links before January 17 2025 11:59 PM.
- I will provide office hours on the following dates (please send me an email in advance): 
    - Thursday Dec 12 2024 - 13:00-15:00
    - Tuesday Jan 07 2025 -  10:00-12:00