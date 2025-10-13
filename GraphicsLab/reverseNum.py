# reverse a four-digit number

while True:  
    try:
        num = int(input("Enter a four-digit number (1000-9999): "))  
        if 1000 <= num <= 9999:  # Check if it's exactly four digits
            break  # Valid input, exit loop
        else:
            print("Invalid input. Please enter a number between 1000 and 9999.")
    except ValueError:  # Handle non-integer inputs
        print("Invalid input. Please enter an integer.")

# Convert the number to a string to easily reverse digits
num_str = str(num)  

# Reverse the string using slicing
reversed_str = num_str[::-1]  

reversed_num = int(reversed_str)  
print(f"The reverse of {num} is {reversed_num}")
