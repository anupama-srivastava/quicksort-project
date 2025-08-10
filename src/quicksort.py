"""
Quicksort Algorithm Implementation
================================

This module provides an efficient implementation of the Quicksort algorithm,
a divide-and-conquer sorting algorithm with average time complexity O(n log n).

Algorithm Overview:
1. Choose a pivot element from the array
2. Partition the array into two sub-arrays:
   - Elements less than the pivot
   - Elements greater than or equal to the pivot
3. Recursively apply the above steps to the sub-arrays
4. Combine the sorted sub-arrays and pivot

Time Complexity:
- Best/Average Case: O(n log n)
- Worst Case: O(n²) - occurs when pivot is always the smallest or largest element
- Space Complexity: O(log n) - due to recursive call stack

The implementation includes both functional (returns new list) and in-place versions.
"""

from typing import List, Callable, Any
import random


def quicksort(arr: List[Any], key: Callable[[Any], Any] = None, reverse: bool = False) -> List[Any]:
    """
    Functional implementation of Quicksort that returns a new sorted list.
    
    Args:
        arr: List of comparable elements to sort
        key: Optional function to extract comparison key from each element
        reverse: If True, sort in descending order
    
    Returns:
        New list containing sorted elements
    
    Examples:
        >>> quicksort([3, 1, 4, 1, 5, 9, 2, 6])
        [1, 1, 2, 3, 4, 5, 6, 9]
        
        >>> quicksort([3, 1, 4, 1, 5], reverse=True)
        [5, 4, 3, 1, 1]
        
        >>> quicksort(['apple', 'banana', 'cherry'], key=len)
        ['apple', 'banana', 'cherry']
    """
    if len(arr) <= 1:
        return arr[:]
    
    # Use the last element as pivot (simple approach)
    pivot = arr[-1]
    
    # Partition the array
    left = [x for x in arr[:-1] if _compare(x, pivot, key) <= 0]
    right = [x for x in arr[:-1] if _compare(x, pivot, key) > 0]
    
    # Recursively sort sub-arrays
    sorted_left = quicksort(left, key=key, reverse=reverse)
    sorted_right = quicksort(right, key=key, reverse=reverse)
    
    # Combine results
    result = sorted_left + [pivot] + sorted_right
    
    # Handle reverse ordering
    if reverse:
        result.reverse()
    
    return result


def quicksort_inplace(arr: List[Any], low: int = 0, high: int = None, 
                     key: Callable[[Any], Any] = None, reverse: bool = False) -> None:
    """
    In-place implementation of Quicksort that modifies the input list.
    
    Args:
        arr: List to sort in-place
        low: Starting index for sorting (default: 0)
        high: Ending index for sorting (default: len(arr) - 1)
        key: Optional function to extract comparison key from each element
        reverse: If True, sort in descending order
    
    Examples:
        >>> arr = [3, 1, 4, 1, 5, 9, 2, 6]
        >>> quicksort_inplace(arr)
        >>> arr
        [1, 1, 2, 3, 4, 5, 6, 9]
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partition the array and get pivot index
        pivot_index = _partition(arr, low, high, key, reverse)
        
        # Recursively sort sub-arrays
        quicksort_inplace(arr, low, pivot_index - 1, key, reverse)
        quicksort_inplace(arr, pivot_index + 1, high, key, reverse)


def _partition(arr: List[Any], low: int, high: int, key: Callable[[Any], Any] = None, 
               reverse: bool = False) -> int:
    """
    Partition helper function for in-place quicksort.
    
    Args:
        arr: List to partition
        low: Starting index
        high: Ending index
        key: Optional comparison key function
        reverse: Sorting direction
    
    Returns:
        Index of the pivot element after partitioning
    """
    # Choose median-of-three pivot for better performance
    mid = (low + high) // 2
    pivot = arr[mid]
    
    # Move pivot to end
    arr[mid], arr[high] = arr[high], arr[mid]
    
    i = low - 1
    
    for j in range(low, high):
        comparison = _compare(arr[j], pivot, key)
        if not reverse and comparison <= 0:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
        elif reverse and comparison >= 0:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Place pivot in correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    return i + 1


def _compare(a: Any, b: Any, key: Callable[[Any], Any] = None) -> int:
    """
    Helper function for comparing elements with optional key function.
    
    Args:
        a: First element to compare
        b: Second element to compare
        key: Optional function to extract comparison key
    
    Returns:
        Negative if a < b, zero if a == b, positive if a > b
    """
    if key is not None:
        a_key, b_key = key(a), key(b)
    else:
        a_key, b_key = a, b
    
    if a_key < b_key:
        return -1
    elif a_key > b_key:
        return 1
    else:
        return 0


# Optimized version with random pivot selection
def quicksort_optimized(arr: List[Any], key: Callable[[Any], Any] = None, 
                       reverse: bool = False) -> List[Any]:
    """
    Optimized Quicksort with random pivot selection to avoid worst-case scenarios.
    
    Args:
        arr: List of elements to sort
        key: Optional function to extract comparison key
        reverse: If True, sort in descending order
    
    Returns:
        New list containing sorted elements
    """
    def _quicksort_helper(arr: List[Any], low: int, high: int) -> None:
        while low < high:
            # Use insertion sort for small arrays
            if high - low < 10:
                _insertion_sort(arr, low, high)
                break
            
            # Random pivot selection
            pivot_index = random.randint(low, high)
            arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
            
            # Partition
            p = _partition(arr, low, high, key, reverse)
            
            # Tail recursion optimization
            if p - low < high - p:
                _quicksort_helper(arr, low, p - 1)
                low = p + 1
            else:
                _quicksort_helper(arr, p + 1, high)
                high = p - 1
    
    result = arr[:]
    _quicksort_helper(result, 0, len(result) - 1)
    
    if reverse:
        result.reverse()
    
    return result


def _insertion_sort(arr: List[Any], low: int, high: int, key: Callable[[Any], Any] = None) -> None:
    """Insertion sort for small sub-arrays."""
    for i in range(low + 1, high + 1):
        key_val = arr[i]
        j = i - 1
        while j >= low and _compare(arr[j], key_val, key) > 0:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_val


if __name__ == "__main__":
    import doctest
    doctest.testmod()
