import math
import random

def PollardRho(n):

    # no prime divisor for 1 
    if (n == 1):
        return n

    # even number means one of the divisors is 2 
    if (n % 2 == 0):
        return 2

    # we will pick from the range [2, N) 
    x = (random.randint(0, 2) % (n - 2))
    y = x

    # the constant in f(x).
    # Algorithm can be re-run with a different c
    # if it throws failure for a composite. 
    c = (random.randint(0, 1) % (n - 1))

    # Initialize candidate divisor (or result) 
    d = 1

    # until the prime factor isn't obtained.
    # If n is prime, return n 
    while (d == 1):
    
        # Tortoise Move: x(i+1) = f(x(i)) 
        x = (pow(x, 2, n) + c + n)%n

        # Hare Move: y(i+1) = f(f(y(i))) 
        y = (pow(y, 2, n) + c + n)%n
        y = (pow(y, 2, n) + c + n)%n

        # check gcd of |x-y| and n 
        d = math.gcd(abs(x - y), n)

        # retry if the algorithm fails to find prime factor
        # with chosen x and c 
        if (d == n):
            return PollardRho(n)
    
    return d

def Pollard(n):
    factors = []
    while True:
        try:
            f = PollardRho(n)
        except RecursionError:
            break
        else:
            factors.append(f)
            n = n // f
    return factors
