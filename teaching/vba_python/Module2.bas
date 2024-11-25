Function all_prime_numbers_until_N(N As Integer) As Variant
    Dim primes() As Boolean
    Dim i As Integer, j As Integer
    Dim primeNumbers() As Integer
    Dim primeCount As Integer
    
    ' Step 1: Initialize the boolean array
    ReDim primes(2 To N)
    For i = 2 To N
        primes(i) = True ' Assume all numbers are prime initially
    Next i
    
    ' Step 2: Implement the Sieve of Eratosthenes
    For i = 2 To Sqr(N)
        If primes(i) = True Then
            For j = i * i To N Step i
                primes(j) = False ' Mark multiples of i as non-prime
            Next j
        End If
    Next i
    
    ' Step 3: Count prime numbers
    primeCount = 0
    For i = 2 To N
        If primes(i) = True Then
            primeCount = primeCount + 1
        End If
    Next i
    
    ' Step 4: Store prime numbers in an array
    ReDim primeNumbers(1 To primeCount)
    primeCount = 0
    For i = 2 To N
        If primes(i) = True Then
            primeCount = primeCount + 1
            primeNumbers(primeCount) = i
        End If
    Next i
    
    ' Return the prime numbers as an array
    all_prime_numbers_until_N = Application.Transpose(primeNumbers)
End Function

