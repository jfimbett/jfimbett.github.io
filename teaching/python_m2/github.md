---
marp: true
header: 'Github'
footer: 'Juan F. Imbet *Ph.D.*'
paginate: true
---

# A handbook for Github
## Juan F. Imbet *Ph.D.*
### Paris Dauphine University

---
# GitHub

Github is a cloud-based platform to store and share code. 

- Showcase your work. 
- Track and manage changes. 
- Review and collaborate.

# Git

Git is a version control system. It is useful when you and other people are working on the same project.

---
# Requirements 

-  [Create an account on GitHub](https://docs.github.com/en/get-started/using-github/connecting-to-github)
- [Install Git on your computer](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- [Connect to GitHub](https://docs.github.com/en/get-started/using-github/connecting-to-github)
- [Install the GitHub CLI](https://github.com/cli/cli) 

---
# Command Line Interface

```bash
git --version 
git config --global user.name "Juan Imbett"
git config user.name
git config --global user.email "jfimbett@gmail.com"
git config --global user.email
```

```output
git version 2.44.0.windows.1
Juan Imbett
jfimbett@gmail.com
```

```bash
gh auth login
```

---
# Step 3: Create a Local Repository

```bash
cd 
mkdir hello-world
cd hello-world
git init # creates .git folder
```

# Step 4: Add Files to the Repository

```bash
git add .
git commit -m "First commit"
```

---
# Step 5: Create a Remote Repository

```bash
gh repo create hello-world --public --source=.
```

```output
✓ Created repository jfimbett/hello-world on GitHub
  https://github.com/jfimbett/hello-world
✓ Added remote https://github.com/jfimbett/hello-world.git
```

---
# Step 6: Push the Local Repository to GitHub

You can use the git remote add command to match a remote URL with a name. For example, you'd type the following in the command line:

`git remote add origin <REMOTE_URL>`

This associates the name `origin` with the `REMOTE_URL`.

You can use the command `git remote set-url` to change a remote's URL.

```bash
git remote add origin https://github.com/jfimbett/hello-world.git
```

---
# Step 7: Push the Local Repository to GitHub

```bash

git push -u origin master
```
Where `origin` is the name of the remote repository and `master` is the name of the branch (more on this later).