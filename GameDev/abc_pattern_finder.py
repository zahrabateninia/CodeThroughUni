#!/usr/bin/env python3
''''
Write a program that reads a string composed of English alphabet letters from the input, and prints all the substrings that match the following pattern:

For a given number n >=1

abbbbb...bc
(where there are n b's between a and c)

Each match must be printed on a separate line.
'''


import re

def main():
    print("Enter multiple lines of text (each up to 100 characters). End with a line containing just 0.")

    pattern = re.compile(r'ab{1,}c')  # Matches 'a' followed by 1 or more 'b's and ending with 'c'
    matches = []

    while True:
        line = input().strip() # remove leading and trailing whitespaces

        if line == '0':
            break

        if len(line) > 100:
            print("Line skipped: exceeds 100 characters.")
            continue

        found = pattern.findall(line)
        matches.extend(found)

    for match in matches:
        print(match)

if __name__ == "__main__":
    main()
