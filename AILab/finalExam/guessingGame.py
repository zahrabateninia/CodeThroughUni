# Task 3: Number guessing game

import random

secret_number = random.randint(1, 100)

print("Welcome to the number guessing game!")
print("I am thinking of a number between 1 and 100.")

while True:
    guess = int(input("Enter your guess: "))

    if guess < secret_number:
        print("Too low! Try again.")
    elif guess > secret_number:
        print("Too high! Try again.")
    else:
        print("Correct! You guessed the number.")
        break
