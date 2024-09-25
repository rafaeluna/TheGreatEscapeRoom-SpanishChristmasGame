import math
from typing import Tuple

def find_squarest_factors(n: int) -> Tuple[int, int]:
    """
    Find the squarest factors of a number
    (the pair of numbers closer to each other that multiplied yield n)
    """

    # Initialize variables to store the best factor pair
    best_factors = (1, n)
    min_difference = n - 1  # Start with the largest possible difference

    # Loop through potential factors up to the square root of n
    for i in range(1, math.isqrt(n) + 1):
        if n % i == 0:  # i is a factor
            corresponding_factor = n // i
            difference = abs(i - corresponding_factor)

            # If this pair is closer to a square form, update best_factors
            if difference < min_difference:
                min_difference = difference
                best_factors = (i, corresponding_factor)

    # Ensure the bigger number comes first
    if best_factors[1] > best_factors[0]:
        best_factors = (best_factors[1], best_factors[0])

    return best_factors
