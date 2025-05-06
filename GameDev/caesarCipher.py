#!/usr/bin/env python3

import string

# REFACTOR: Use string.ascii_lowercase and string.ascii_uppercase instead of hardcoded lists
ALPHABET_SMALL_LETTERS = string.ascii_lowercase
ALPHABET_CAPITAL_LETTERS = string.ascii_uppercase

# REFACTOR: Use a helper function for shifting logic
def shift_char(char, shift):
    if char in ALPHABET_SMALL_LETTERS:
        index = ALPHABET_SMALL_LETTERS.index(char)
        return ALPHABET_SMALL_LETTERS[(index + shift) % 26]
    elif char in ALPHABET_CAPITAL_LETTERS:
        index = ALPHABET_CAPITAL_LETTERS.index(char)
        return ALPHABET_CAPITAL_LETTERS[(index + shift) % 26]
    else:
        return char

def caesar_cipher(text, shift_value):
    if len(text) > 100:
        return "ERROR: Your sentence should be less than 100 characters!"
    
    #  return the result instead of printing
    return ''.join(shift_char(char, shift_value) for char in text)

# I/O
text = input("Enter your sentence (less than 100 characters): ")
shift_value = int(input("Enter your desired shift value as well: "))
print(caesar_cipher(text, shift_value))
