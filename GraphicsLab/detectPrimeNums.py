# Program to detect prime numbers from 0 to 100

# A prime number is greater than 1 and has no positive divisors other than 1 and itself
def is_prime(num):
    if num <= 1:  
        return False
    for i in range(2, int(num**0.5) + 1):  # Check divisors up to sqrt(num) for efficiency
        if num % i == 0:  # If divisible by any number, it's not prime
            return False
    return True  # If no divisors found, it's prime

primes = []  
for number in range(101):  
    if is_prime(number):
        primes.append(number)  

print("Prime numbers from 0 to 100:", primes)
