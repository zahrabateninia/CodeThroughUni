# Generate two random floats, multiply them, and compute their GCD
import random
import math

a = random.uniform(1, 100)
b = random.uniform(1, 100)

product = a * b

a_int = int(a)
b_int = int(b)

gcd_value = math.gcd(a_int, b_int)

print(f"Random float A: {a}")
print(f"Random float B: {b}")
print(f"Product: {product}")
print(f"GCD of integer parts ({a_int}, {b_int}): {gcd_value}")
