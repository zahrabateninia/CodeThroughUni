#!/usr/bin/env python3

# To-Do: handle capital letters, input more than 100 chars

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def caesarCipher(text, shiftValue):
    # if shiftValue > 0 move forward, if negative move backward
    # special characters such as $, %, " "... stay the same

    cipherText = ""

    if shiftValue == 0:
        return text


    elif shiftValue < 0:
        for char in text: 
            if char in alphabet:
                newPosition = alphabet.indexOf(char) - shiftValue
                cipherText += alphabet[newPosition]
            else: # if it wasn't a letter
                cipherText += char
    else: # shiftValue is positive
        for char in text: 
            if char in alphabet:
                newPosition = alphabet.index(char) + shiftValue
                cipherText += alphabet[newPosition]
            else: # if it wasn't a letter
                cipherText += char

    print(cipherText)

text = input("Enter your sentence (less than 100 characters): ")
shiftValue = int(input("Enter your desired shift value as well: "))

caesarCipher(text, shiftValue)
