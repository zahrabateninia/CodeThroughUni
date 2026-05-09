# Define a recursive function for factorial
# Recursive case: n! = n * (n-1)!
def factorial(n):
    if n < 0:  
        raise ValueError("Factorial is only defined for non-negative integers.")
    if n == 0 or n == 1:  # Base case
        return 1
    else:  # Recursive case
        return n * factorial(n - 1)  # Multiply n by factorial of (n-1)


while True:  
    try:
        n = int(input("Enter a non-negative integer to compute factorial: "))  # Prompt for n
        if n >= 0:
            break  
        else:
            print("Please enter a non-negative integer.")
    except ValueError:  #
        print("Invalid input. Please enter an integer.")

result = factorial(n)
print(f"The factorial of {n} is {result}")
