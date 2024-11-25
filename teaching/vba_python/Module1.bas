Attribute VB_Name = "Module1"
Sub temperature_converter()
    Dim original_temp As Single
    Dim converted_temp As Single
    Dim original_units As String
    Dim converted_units As String
    
    original_temp = ThisWorkbook.Sheets("Sheet1").Range("B2").Value
    original_units = ThisWorkbook.Sheets("Sheet1").Range("C2").Value
    converted_units = ThisWorkbook.Sheets("Sheet1").Range("C3").Value
    
    'trim units and make them uppercase
    original_units = UCase(Trim(original_units))
    converted_units = UCase(Trim(converted_units))

    ' We only accept symbols K, C, or F
    ' Check that the original units are valid

    If original_units <> "K" And original_units <> "C" And original_units <> "F" Then
        MsgBox "Invalid original units. Please use K, C, or F."
        Exit Sub
    End If

    ' Check that the converted units are valid
    ' Kelvin cannot be negative 

    if original_units = "K" And original_temp < 0 Then
        MsgBox "Kelvin cannot be negative."
        Exit Sub
    End If

    ' Always convert to Kelvin first

    If original_units = "C" Then
        converted_temp = original_temp + 273.15
    ElseIf original_units = "F" Then
        converted_temp = (original_temp - 32) * 5 / 9 + 273.15
    Else
        converted_temp = original_temp
    End If

    ' Convert from Kelvin to the desired units

    If converted_units = "C" Then
        converted_temp = converted_temp - 273.15
    ElseIf converted_units = "F" Then
        converted_temp = (converted_temp - 273.15) * 9 / 5 + 32
    End If

    ThisWorkbook.Sheets("Sheet1").Range("B3").Value = converted_temp

End Sub

