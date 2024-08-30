---
marp: true
header: 'VBA and Python'
footer: 'Juan F. Imbet *Ph.D.*'
paginate: true
---

# Programming 1: VBA and Python
## Juan F. Imbet *Ph.D.*
### Paris Dauphine University
### M203 (M1) 

---
## Visual Basic for Applications (VBA)

- VBA is a programming language that is used to automate tasks in Microsoft Office applications.
- VBA is a subset of Visual Basic (VB), focusing on **macros** and **automation**.
- You can use VBA inside of Outlook, Word, Excel, Access, and PowerPoint.
- We will focus on Excel VBA as it is the most common use case.
- Although some other languages are becoming more and more popular, VBA is still widely used in the industry, and this is unlikely to change in the near future.

---
## What happens in the back?

- Code written in VBA is **compiled** to Microsoft P-Code (Pseudo Code), a proprietary intermediate language.
---

## Characteristics of VBA

- **General Purpose**
- **Interpreted**
- **Event-Driven**
- **Object-Oriented**
- **High Level**

---
## General Purpose

- VBA is a general-purpose programming language, meaning that it can be used to solve a wide range of problems. It is only limited by the use of Office applications.

* Automated Financial Models and Dashbords. 
* Custom ERP Systems
* Interactive Games
* In 2003 a flight simulator was created in Excel using VBA.

---

## Interpreted

- VBA is an interpreted language, meaning that the code is executed line by line. This is different from compiled languages like C++ or Java, where the code is compiled into machine code before execution.

---
## Event-Driven

- VBA is an event-driven language, meaning that code is executed in response to events. For example, you can write code that is executed when a user clicks a button or opens a workbook.


## Object-Oriented

- VBA is an object-oriented language, meaning that it uses objects to represent data and functionality. Objects can be manipulated using methods and properties.

---
## High Level

- VBA is a high-level language, meaning that it is closer to human language than machine language. This makes it easier to read and write code (more on this when we talk about Python).

---

# SETTING UP YOUR ENVIRONMENT

---

## You need

- Microsoft Excel
- [VS Code](https://code.visualstudio.com/download) (we will not use the standard VBA editor)
- VBA extension for VS Code
- [Python](https://www.anaconda.com/download/) (Anaconda Distribution)
- [`xlwings`](https://docs.xlwings.org/en/stable/installation.html) library for Python that allows you to interact with Excel.

---

## Install `xlwings`

```bash
pip install xlwings
pip install watchgod
```

Open an excel file and save it as a macro-enabled workbook, call it `hello_world.xlsm`.


---

## VBA in VS Code

- Excel files are really zip files with a different extension.

- Enable Trust Access to the VBA Project Object Model:

    * Open Excel.
    * Go to File > Options.
    * In the Excel Options window, select Trust Center on the left.
    * Click on the Trust Center Settings button.
    * In the Trust Center, select Macro Settings.
    * Check the box that says Trust access to the VBA project object model.
    * Click OK to close the Trust Center and then OK to close the Excel Options.

- Click on the View tab and then click on the Macros button, create a new macro called `my_first_macro()`. 

---

## `xlwings`

- Directly in vs code, open a prompt and type 
```bash
xlwings vba edit -f hello_world.xlsm
```
```output
xlwings version: 0.29.1

This will affect the following workbook/folder:

* hello_world.xlsm
* C:\Users\jfimb\Dropbox\jfimbett.github.io\teaching\vba_python

Proceed? [Y/n] y
NOTE: Deleting a VBA module here will also delete it in the VBA editor!
Watching for changes in hello_world.xlsm (silent mode)...(Hit Ctrl-C to stop)
```

---
- Do not close excel, keep the macro editor open.
- In the file explorer you should see a file called Module1.bas
- Edit the file and write the following code:

```vba
Attribute VB_Name = "Module1"
Sub my_first_macro()
' Display a message box
    MsgBox "Hello, world!"
End Sub
```
- The first line does not appear in the VBA Editor, but VS Code identifies it. 
- You still need to run the macro from the Excel file.

---

## Data Types in VBA

- Default Type: Variant
- Explicit Types: Null, Integer, Long, Single, Double, Currency, Date, String, Boolean, Object. 

- Variables store a specific type of information. 
```vba
Dim variable_name [As type]
```
During the course, the notation `[]` will be used to indicate that a part of the code is optional.

- Variables are implicit by default (Variant).

---

## Scope and lifetime: where and when variables can be used

- Local, Module, Global, Static

* **Local**: only within the procedure (Sub or Function) where it is declared.
* **Module**: within the module where it is declared.
* **Global**: within the entire project.
* **Static**: retains its value between calls to the procedure.

---

## `Dim`, `Static`, `ReDim` and `Global`

- `Dim`: declares a variable, 
```vba
Dim x 
```
- `Static`: retains its value between calls to the procedure.
```vba
Static x 
```
- `ReDim`: changes the size of an array.
```vba
ReDim x(1 to 10)
```
- `Global`: declares a variable that can be used in any module.
```vba
Global x
```

---

## Arrays

- Syntax:
```vba
Dim my_array(size_of_array) [As type of elements]
Dim my_array(1 to 10) As Integer
```
- Often we declare empty arrays and then fill them with values.
```vba
Dim my_array(5)
my_array(0) = 1
begin_idx = LBound(my_array)
end_idx = UBound(my_array)
ReDim Preserve my_array(1 to 10)
ReDim my_array(10)
```
- The initial index of an array is 0 by default.


