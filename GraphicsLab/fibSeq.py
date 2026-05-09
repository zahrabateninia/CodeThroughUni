# generate the first 5 terms of the Fibonacci sequence

n = 5  
fib_sequence = []  
a, b = 0, 1  # Starting points: first two numbers in Fibonacci (0 and 1)

for i in range(n):  
    fib_sequence.append(a)  # Add the current 'a' to the list
    a, b = b, a + b  # Update: next 'a' is current 'b', next 'b' is sum of previous a and b

print("First 5 terms of the Fibonacci sequence:", fib_sequence)
