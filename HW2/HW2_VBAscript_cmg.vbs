Sub StockDataLoop()

   Dim Total As Double
   Dim Summaryrow As Integer

   Summaryrow = 2
   
   Lastrow = Cells(Rows.Count, "A").End(xlUp).Row
   
   Range("I1").Value = "Ticker"
   Range("J1").Value = "Total Stock Volume"

   Total = Total + Cells(2, "G").Value

   For i = 2 To Lastrow

   If Cells(i, 1) = Cells(i + 1, 1) Then
       Total = Total + Cells(i, "G").Value

   Else
    Cells(Summaryrow, "I") = Cells(i - 1, 1).Value
    Total = Total + Cells(i, "G").Value
    Cells(Summaryrow, "j") = Total
    Total = 0
     Summaryrow = Summaryrow + 1
    

     End If

     Next i

End Sub
