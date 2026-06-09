# Task 1: Read a 5-digit number, print its reverse, and check if it is a palindrome

num = input("Enter a 5-digit number: ")

reversed_num = num[::-1]

print("Reversed number:", reversed_num)

if num == reversed_num:
    print("The number is a palindrome (mirror number).")
else:
    print("The number is not a palindrome.")
