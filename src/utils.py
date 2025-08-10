"""
Utility Functions for Quicksort Project
=====================================

This module provides utility functions to support the quicksort implementation,
including validation, array generation, and performance measurement tools.
"""

from typing import List, Any
import random


def is_sorted(arr: List[Any], key=None, reverse: bool = False) -> bool:
    """
    Check if a list is sorted.
    
    Args:
        arr: List to check
        key: Optional function to extract comparison key
        reverse: If True, check for descending order
    
    Returns:
        True if the list is sorted according to the specified criteria
    
    Examples:
        >>> is_sorted([1, 2, 3, 4, 5])
        True
        >>> is_sorted([5, 4, 3, 2, 1], reverse=True)
        True
        >>> is_sorted([1, 3, 2, 4, 5])
        False
    """
    if len(arr) <= 1:
        return True
    
    for i in range(1, len(arr)):
        if key is not None:
            a, b = key(arr[i-1]), key(arr[i])
        else:
            a, b = arr[i-1], arr[i]
        
        if not reverse and a > b:
            return False
        elif reverse and a < b:
            return False
    
    return True


def generate_random_array(size: int, min_val: int = 0, max_val: int = 1000, 
                         unique: bool = False) -> List[int]:
    """
    Generate a random array for testing purposes.
    
    Args:
        size: Number of elements in the array
        min_val: Minimum value for random integers
        max_val: Maximum value for random integers
        unique: If True, all elements will be unique
    
    Returns:
        List of random integers
    
    Examples:
        >>> arr = generate_random_array(10)
        >>> len(arr)
        10
        >>> all(min_val <= x <= max_val for x in arr)
        True
    """
    if unique and size > (max_val - min_val + 1):
        raise ValueError("Cannot generate unique array: range too small for size")
    
    if unique:
        return random.sample(range(min_val, max_val + 1), size)
    else:
        return [random.randint(min_val, max_val) for _ in range(size)]


def generate_sorted_array(size: int, reverse: bool = False) -> List[int]:
    """
    Generate a sorted array for testing purposes.
    
    Args:
        size: Number of elements in the array
        reverse: If True, generate descending order
    
    Returns:
        Sorted list of integers
    
    Examples:
        >>> arr = generate_sorted_array(5)
        >>> arr
        [0, 1, 2, 3, 4]
    """
    if reverse:
        return list(range(size - 1, -1, -1))
    else:
        return list(range(size))


def generate_reverse_sorted_array(size: int) -> List[int]:
    """
    Generate a reverse-sorted array for testing worst-case scenarios.
    
    Args:
        size: Number of elements in the array
    
    Returns:
        List in descending order
    
    Examples:
        >>> arr = generate_reverse_sorted_array(5)
        >>> arr
        [4, 3, 2, 1, 0]
    """
    return generate_sorted_array(size, reverse=True)


def generate_nearly_sorted_array(size: int, swaps: int = 5) -> List[int]:
    """
    Generate a nearly sorted array with some elements swapped.
    
    Args:
        size: Number of elements in the array
        swaps: Number of swaps to perform
    
    Returns:
        Nearly sorted list of integers
    
    Examples:
        >>> arr = generate_nearly_sorted_array(10)
        >>> is_sorted(arr)
        False
    """
    arr = generate_sorted_array(size)
    
    for _ in range(swaps):
        i, j = random.sample(range(size), 2)
        arr[i], arr[j] = arr[j], arr[i]
    
    return arr


def measure_memory_usage(obj: Any) -> int:
    """
    Estimate memory usage of an object in bytes.
    
    Args:
        obj: Object to measure
    
    Returns:
        Estimated memory usage in bytes
    """
    import sys
    return sys.getsizeof(obj)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
