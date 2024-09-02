Attribute VB_Name = "Module2"
Sub VariableTypesExamplesToTable()

    ' Boolean - True or False
    Dim isComplete As Boolean
    isComplete = True

    ' Byte - Integer from 0 to 255
    Dim byteValue As Byte
    byteValue = 255

    ' Integer - Integer from -32,768 to 32,767
    Dim smallNumber As Integer
    smallNumber = 12345

    ' Long - Integer from -2,147,483,648 to 2,147,483,647
    Dim largeNumber As Long
    largeNumber = 1234567890

    ' Single - Single-precision floating-point (approximately -3.4E38 to 3.4E38)
    Dim singlePrecisionNumber As Single
    singlePrecisionNumber = 1234.56

    ' Double - Double-precision floating-point (approximately -1.7E308 to 1.7E308)
    Dim doublePrecisionNumber As Double
    doublePrecisionNumber = 1234567.89

    ' Currency - Fixed-point with 4 decimal places (approximately -922,337,203,685,477.5808 to 922,337,203,685,477.5807)
    Dim currencyValue As Currency
    currencyValue = 12345.6789

    ' Decimal - Floating-point number (exact values, used for financial calculations)
    Dim decimalValue As Variant
    decimalValue = CDec(12345678.1234)
    
    ' Date - Date and time
    Dim currentDate As Date
    currentDate = Now

    ' String - Text
    Dim name As String
    name = "John Doe"

    ' Variant - Can hold any type of data, default data type if not specified
    Dim unknownType As Variant
    unknownType = "Can hold any type"
    
    ' Object - Can refer to any object
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
    ws.Name = "Variable Types"

    ' Range - Special type for referring to Excel ranges
    Dim rng As Range
    Set rng = ws.Range("A1:A10")

    ' Array - A collection of variables of the same type
    Dim numbersArray(1 To 5) As Integer
    numbersArray(1) = 10
    numbersArray(2) = 20
    numbersArray(3) = 30
    numbersArray(4) = 40
    numbersArray(5) = 50

    ' Object - Example with a custom object
    Dim dict As Object
    Set dict = CreateObject("Scripting.Dictionary")
    dict.Add "Key1", "Value1"
    
    ' Preparing headers for the table
    ws.Cells(1, 1).Value = "Variable Type"
    ws.Cells(1, 2).Value = "Variable Name"
    ws.Cells(1, 3).Value = "Value"
    
    ' Filling in the table with data
    ws.Cells(2, 1).Value = "Boolean"
    ws.Cells(2, 2).Value = "isComplete"
    ws.Cells(2, 3).Value = isComplete

    ws.Cells(3, 1).Value = "Byte"
    ws.Cells(3, 2).Value = "byteValue"
    ws.Cells(3, 3).Value = byteValue

    ws.Cells(4, 1).Value = "Integer"
    ws.Cells(4, 2).Value = "smallNumber"
    ws.Cells(4, 3).Value = smallNumber

    ws.Cells(5, 1).Value = "Long"
    ws.Cells(5, 2).Value = "largeNumber"
    ws.Cells(5, 3).Value = largeNumber

    ws.Cells(6, 1).Value = "Single"
    ws.Cells(6, 2).Value = "singlePrecisionNumber"
    ws.Cells(6, 3).Value = singlePrecisionNumber

    ws.Cells(7, 1).Value = "Double"
    ws.Cells(7, 2).Value = "doublePrecisionNumber"
    ws.Cells(7, 3).Value = doublePrecisionNumber

    ws.Cells(8, 1).Value = "Currency"
    ws.Cells(8, 2).Value = "currencyValue"
    ws.Cells(8, 3).Value = currencyValue

    ws.Cells(9, 1).Value = "Decimal"
    ws.Cells(9, 2).Value = "decimalValue"
    ws.Cells(9, 3).Value = decimalValue

    ws.Cells(10, 1).Value = "Date"
    ws.Cells(10, 2).Value = "currentDate"
    ws.Cells(10, 3).Value = currentDate

    ws.Cells(11, 1).Value = "String"
    ws.Cells(11, 2).Value = "name"
    ws.Cells(11, 3).Value = name

    ws.Cells(12, 1).Value = "Variant"
    ws.Cells(12, 2).Value = "unknownType"
    ws.Cells(12, 3).Value = unknownType

    ws.Cells(13, 1).Value = "Array (Element 1)"
    ws.Cells(13, 2).Value = "numbersArray(1)"
    ws.Cells(13, 3).Value = numbersArray(1)
    
    ws.Cells(14, 1).Value = "Object (Dictionary)"
    ws.Cells(14, 2).Value = "dict(""Key1"")"
    ws.Cells(14, 3).Value = dict("Key1")
    
    ' Formatting the table
    With ws.Range("A1:C14")
        .Font.Bold = True
        .Borders.LineStyle = xlContinuous
        .Columns.AutoFit
    End With

End Sub

Sub SimpleMessages()
    MsgBox "This is a simple message box"
    MsgBox "This is a simple message box with a title", vbInformation, "Title"
    MsgBox "This is a simple message box with a title and a Yes/No button", vbYesNo, "Title"
End Sub

Sub SimpleMessagesUserClick()
    Dim response As VbMsgBoxResult
    response = MsgBox("Do you want to continue?", vbYesNo, "Continue?")
    If response = vbYes Then
        MsgBox "You clicked Yes"
    Else
        MsgBox "You clicked No"
    End If
End Sub

Sub RetrieveInformation()
    Dim name As String
    name = InputBox("What is your name?", "Name")
    MsgBox "Hello, " & name
End Sub

Sub RetrieveInformationFromCell()
    Dim value As Variant
    value = ThisWorkbook.Sheets("Sheet1").Range("A1").Value
    MsgBox "The value in cell A1 is " & value
End Sub

Sub WriteToCell()
    ThisWorkbook.Sheets("Sheet1").Range("A1").Value = "Hello, world!"
End Sub

Sub WriteArrayToRange()
    Dim values As Variant
    values = Array("One", "Two", "Three", "Four", "Five")
    ThisWorkbook.Sheets("Sheet1").Range("A1:A5").Value = Application.Transpose(values)
End Sub

Sub UseExcelFunction()
    ' Initialize an array with values
    Dim valuesArray As Variant
    valuesArray = Array(1, 2, 3, 4, 5)
    
    ' Loop through the range and assign the array values to the cells
    Dim i As Integer
    For i = 1 To 5
        ThisWorkbook.Sheets("Sheet1").Cells(i, 1).Value = valuesArray(i - 1)
    Next i
    
    ' Calculate the sum of the range
    Dim result As Variant
    result = Application.WorksheetFunction.Sum(ThisWorkbook.Sheets("Sheet1").Range("A1:A5"))
    
    ' Display the result in a message box
    MsgBox "The sum of the values in A1:A5 is " & result
End Sub

Sub IfStatement()
    Dim value As Integer
    value = 10
    
    If value > 5 Then
        MsgBox "The value is greater than 5"
    End If
End Sub

Sub IfElseStatement()
    Dim value As Integer
    value = 3
    
    If value > 5 Then
        MsgBox "The value is greater than 5"
    Else
        MsgBox "The value is less than or equal to 5"
    End If
End Sub

Sub ElseIfStatement()
    Dim value As Integer
    value = 5
    
    If value > 5 Then
        MsgBox "The value is greater than 5"
    ElseIf value < 5 Then
        MsgBox "The value is less than 5"
    Else
        MsgBox "The value is equal to 5"
    End If
End Sub

Sub ForLoop()
    Dim N As Integer
    N = 10

    Dim myArray() As Integer
    ReDim myArray(N)
    Dim i As Integer
    For i = 0 To N - 1
        myArray(i) = i  + 1
    Next i

    Dim sum As Integer
    sum = 0
    For i = 0 To N -1
        sum = sum + myArray(i)
    Next i

    MsgBox "The sum of the numbers from 1 to " & N & " is " & sum

End Sub

Function AddNumbers(x As Double, y As Double) As Double
    AddNumbers = x + y
End Function
