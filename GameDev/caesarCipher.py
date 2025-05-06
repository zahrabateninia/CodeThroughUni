#!/usr/bin/env python3

# To-Do: handle capital letters, input more than 100 chars

ALPHABET_SMALL_LETTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
ALPHABET_CAPITAL_LETTERS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


def caesarCipher(text, shiftValue):
    # if shiftValue > 0 move forward, if negative move backward
    # special characters such as $, %, " "... stay the same

    if len(text) > 100:
        print("ERROR: Your sentence should be less than 100 characters!")
        return

    cipherText = ""

    if shiftValue == 0:
        return text


  
    for char in text: 
        if char in ALPHABET_SMALL_LETTERS:
            newPosition = (ALPHABET_SMALL_LETTERS.index(char) + shiftValue) % 26
            cipherText += ALPHABET_SMALL_LETTERS[newPosition]
        elif char in ALPHABET_CAPITAL_LETTERS:
            newPosition = (ALPHABET_CAPITAL_LETTERS.index(char) + shiftValue)  % 26
            cipherText += ALPHABET_CAPITAL_LETTERS[newPosition]
        else: # if it wasn't a letter
            cipherText += char

    print(cipherText)

text = input("Enter your sentence (less than 100 characters): ")
shiftValue = int(input("Enter your desired shift value as well: "))

caesarCipher(text, shiftValue)
