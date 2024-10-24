import math
import random
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
    for i in range(1, isqrt(n) + 1):
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

def random_red() -> tuple:
    """Generate a random shade of red."""
    return (random.uniform(0.7, 1), random.uniform(0, 0.2), random.uniform(0, 0.2), 1)

def random_green() -> tuple:
    """Generate a random shade of green."""
    return (random.uniform(0, 0.2), random.uniform(0.7, 1), random.uniform(0, 0.2), 1)

def get_random_christmas_color() -> tuple:
    """Randomly choose a color: red, green, or light gray."""
    color_choice = random.choice(["red", "green"])
    if color_choice == "red":
        return (0.7, 0, 0)
    return (0, 0.39215686, 0)

def isqrt(n: int) -> int:
    """Calculate the integer square root of a non-negative integer n."""
    if n < 0:
        raise ValueError("isqrt() argument must be non-negative")
    if n == 0:
        return 0

    # Use binary search to find the integer square root
    left, right = 1, n
    while left <= right:
        mid = (left + right) // 2
        if mid * mid <= n < (mid + 1) * (mid + 1):
            return mid
        elif mid * mid < n:
            left = mid + 1
        else:
            right = mid - 1
