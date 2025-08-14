"""
Advanced Quicksort Algorithm Implementation
==========================================

This module provides advanced implementations of the Quicksort algorithm including:
- Multiple pivot selection strategies
- Hybrid algorithms (introsort)
- Parallel processing capabilities
- Advanced optimization techniques

Author: Advanced Algorithm Implementation
Version: 2.0.0
"""

import math
import random
import statistics
from typing import List, Callable, Any, Tuple, Optional
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedQuicksort:
    """
    Advanced Quicksort implementation with multiple optimization strategies.
    
    This class provides various quicksort variants including:
    - Median-of-three pivot selection
    - Median-of-medians pivot selection
    - Introsort (hybrid of quicksort, heapsort, and insertion sort)
    - Parallel processing support
    """
    
    def __init__(self, threshold: int = 10, max_depth: int = None):
        """
        Initialize AdvancedQuicksort with optimization parameters.
        
        Args:
            threshold: Size threshold for switching to insertion sort
            max_depth: Maximum recursion depth before switching to heapsort
        """
        self.threshold = threshold
        self.max_depth = max_depth or 2 * math.floor(math.log2(1000))  # Default based on array size
        
    def sort(self, arr: List[Any], 
             pivot_strategy: str = 'median_of_three',
             parallel: bool = False,
             key: Callable[[Any], Any] = None,
             reverse: bool = False) -> List[Any]:
        """
        Main sorting method with configurable strategies.
        
        Args:
            arr: List to sort
            pivot_strategy: 'random', 'median_of_three', 'median_of_medians', 'introsort'
            parallel: Enable parallel processing for large arrays
            key: Key function for custom sorting
            reverse: Sort in descending order
            
        Returns:
            Sorted list
        """
        if not arr:
            return arr
            
        if pivot_strategy == 'introsort':
            return self.introsort(arr[:], key=key, reverse=reverse)
        elif parallel and len(arr) > 10000:
            return self.parallel_quicksort(arr[:], key=key, reverse=reverse)
        else:
            return self._quicksort_recursive(arr[:], 0, len(arr) - 1, 
                                           pivot_strategy, key, reverse)
    
    def _quicksort_recursive(self, arr: List[Any], low: int, high: int,
                           pivot_strategy: str, key: Callable, reverse: bool) -> List[Any]:
        """Internal recursive quicksort implementation."""
        if low < high:
            # Use insertion sort for small arrays
            if high - low < self.threshold:
                self._insertion_sort_range(arr, low, high, key, reverse)
                return arr
                
            # Select pivot based on strategy
            pivot_index = self._select_pivot(arr, low, high, pivot_strategy)
            arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
            
            # Partition
            p = self._partition(arr, low, high, key, reverse)
            
            # Recursively sort sub-arrays
            self._quicksort_recursive(arr, low, p - 1, pivot_strategy, key, reverse)
            self._quicksort_recursive(arr, p + 1, high, pivot_strategy, key, reverse)
            
        return arr
    
    def _select_pivot(self, arr: List[Any], low: int, high: int, 
                     strategy: str) -> int:
        """Select pivot based on specified strategy."""
        if strategy == 'random':
            return random.randint(low, high)
        elif strategy == 'median_of_three':
            return self._median_of_three(arr, low, high)
        elif strategy == 'median_of_medians':
            return self._median_of_medians(arr, low, high)
        else:
            return high  # Default to last element
    
    def _median_of_three(self, arr: List[Any], low: int, high: int) -> int:
        """Select median of first, middle, and last elements as pivot."""
        mid = (low + high) // 2
        
        # Compare three elements
        a, b, c = arr[low], arr[mid], arr[high]
        
        if a <= b <= c or c <= b <= a:
            return mid
        elif b <= a <= c or c <= a <= b:
            return low
        else:
            return high
    
    def _median_of_medians(self, arr: List[Any], low: int, high: int) -> int:
        """Select pivot using median-of-medians algorithm (linear time selection)."""
        if high - low < 5:
            # Use insertion sort for small arrays
            temp = arr[low:high+1]
            temp.sort(key=lambda x: x)
            median_val = temp[len(temp)//2]
            return arr.index(median_val, low, high+1)
        
        # Divide into groups of 5
        medians = []
        for i in range(low, high+1, 5):
            group_end = min(i+5, high+1)
            group = arr[i:group_end]
            group.sort(key=lambda x: x)
            median_idx = i + len(group)//2
            medians.append(arr[median_idx])
        
        # Find median of medians
        median_of_medians = statistics.median(medians)
        
        # Find index of median_of_medians in original array
        for i in range(low, high+1):
            if arr[i] == median_of_medians:
                return i
        
        return (low + high) // 2
    
    def _partition(self, arr: List[Any], low: int, high: int, 
                   key: Callable, reverse: bool) -> int:
        """Partition array around pivot."""
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            comparison = self._compare_elements(arr[j], pivot, key)
            if not reverse and comparison <= 0:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
            elif reverse and comparison >= 0:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def _compare_elements(self, a: Any, b: Any, key: Callable = None) -> int:
        """Compare two elements with optional key function."""
        if key is not None:
            a_key, b_key = key(a), key(b)
        else:
            a_key, b_key = a, b
            
        if a_key < b_key:
            return -1
        elif a_key > b_key:
            return 1
        return 0
    
    def _insertion_sort_range(self, arr: List[Any], low: int, high: int,
                            key: Callable, reverse: bool) -> None:
        """Insertion sort for small ranges."""
        for i in range(low + 1, high + 1):
            key_val = arr[i]
            j = i - 1
            while j >= low:
                comparison = self._compare_elements(arr[j], key_val, key)
                if not reverse and comparison > 0:
                    arr[j + 1] = arr[j]
                    j -= 1
                elif reverse and comparison < 0:
                    arr[j + 1] = arr[j]
                    j -= 1
                else:
                    break
            arr[j + 1] = key_val
    
    def introsort(self, arr: List[Any], key: Callable = None, reverse: bool = False) -> List[Any]:
        """
        Introsort implementation - hybrid of quicksort, heapsort, and insertion sort.
        
        Introsort starts with quicksort and switches to heapsort when the recursion
        depth exceeds a threshold, ensuring O(n log n) worst-case performance while
        maintaining quicksort's average-case efficiency.
        """
        def _introsort_helper(arr: List[Any], low: int, high: int, depth_limit: int) -> None:
            while high - low > self.threshold:
                if depth_limit == 0:
                    # Switch to heapsort
                    self._heapsort_range(arr, low, high, key, reverse)
                    return
                
                # Use quicksort
                pivot_index = self._median_of_three(arr, low, high)
                arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
                
                p = self._partition(arr, low, high, key, reverse)
                
                # Recurse on smaller partition first (tail recursion optimization)
                if p - low < high - p:
                    _introsort_helper(arr, low, p - 1, depth_limit - 1)
                    low = p + 1
                else:
                    _introsort_helper(arr, p + 1, high, depth_limit - 1)
                    high = p - 1
            
            # Use insertion sort for small arrays
            self._insertion_sort_range(arr, low, high, key, reverse)
        
        result = arr[:]
        max_depth = 2 * math.floor(math.log2(len(result))) if result else 0
        _introsort_helper(result, 0, len(result) - 1, max_depth)
        return result
    
    def _heapsort_range(self, arr: List[Any], low: int, high: int,
                       key: Callable = None, reverse: bool = False) -> None:
        """Heapsort implementation for range [low, high]."""
        def heapify(arr: List[Any], n: int, i: int) -> None:
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n and self._compare_elements(arr[left], arr[largest], key) > 0:
                largest = left
                
            if right < n and self._compare_elements(arr[right], arr[largest], key) > 0:
                largest = right
                
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)
        
        n = high - low + 1
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr[low:high+1], n, i)
        
        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            arr[low], arr[low + i] = arr[low + i], arr[low]
            heapify(arr[low:high+1], i, 0)
    
    def parallel_quicksort(self, arr: List[Any], key: Callable = None,
                          reverse: bool = False, min_parallel_size: int = 10000) -> List[Any]:
        """
        Parallel quicksort implementation using ThreadPoolExecutor.
        
        Args:
            arr: List to sort
            key: Key function for custom sorting
            reverse: Sort in descending order
            min_parallel_size: Minimum array size to use parallel processing
            
        Returns:
            Sorted list
        """
        def _parallel_sort(arr: List[Any], low: int, high: int, depth: int) -> None:
            if low >= high:
                return
                
            # Use sequential sort for small arrays
            if high - low < min_parallel_size or depth <= 0:
                self._quicksort_recursive(arr, low, high, 'median_of_three', key, reverse)
                return
            
            # Partition
            pivot_index = self._median_of_three(arr, low, high)
            arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
            p = self._partition(arr, low, high, key, reverse)
            
            # Parallel processing for sub-arrays
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = []
                
                if p - low > min_parallel_size // 2:
                    futures.append(executor.submit(_parallel_sort, arr, low, p - 1, depth - 1))
                else:
                    _parallel_sort(arr, low, p - 1, depth - 1)
                
                if high - p > min_parallel_size // 2:
                    futures.append(executor.submit(_parallel_sort, arr, p + 1, high, depth - 1))
                else:
                    _parallel_sort(arr, p + 1, high, depth - 1)
                
                # Wait for parallel tasks to complete
                for future in as_completed(futures):
                    future.result()
        
        result = arr[:]
        max_depth = math.floor(math.log2(len(result))) if result else 0
        _parallel_sort(result, 0, len(result) - 1, max_depth)
        return result


class QuicksortVisualizer:
    """
    Visualization utilities for the quicksort algorithm.
    """
    
    @staticmethod
    def visualize_sorting(arr: List[Any], algorithm: str = 'median_of_three',
                         delay: float = 0.1) -> List[List[Any]]:
        """
        Generate step-by-step visualization of the sorting process.
        
        Args:
            arr: Array to visualize sorting for
            algorithm: Which algorithm to use
            delay: Delay between steps (for animation)
            
        Returns:
            List of array states during sorting
        """
        states = []
        sorter = AdvancedQuicksort()
        
        def _visualize_quicksort(arr: List[Any], low: int, high: int) -> None:
            if low < high:
                states.append(arr[:])  # Capture current state
                
                # Partition
                pivot_index = sorter._median_of_three(arr, low, high)
                arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
                p = sorter._partition(arr, low, high, None, False)
                
                states.append(arr[:])  # After partitioning
                
                # Recursively sort sub-arrays
                _visualize_quicksort(arr, low, p - 1)
                _visualize_quicksort(arr, p + 1, high)
        
        working_arr = arr[:]
        _visualize_quicksort(working_arr, 0, len(working_arr) - 1)
        states.append(working_arr[:])  # Final state
        
        return states


# Convenience functions for easy usage
def quicksort_advanced(arr: List[Any], **kwargs) -> List[Any]:
    """Convenience function for advanced quicksort."""
    sorter = AdvancedQuicksort()
    return sorter.sort(arr, **kwargs)


def quicksort_introsort(arr: List[Any], **kwargs) -> List[Any]:
    """Convenience function for introsort."""
    sorter = AdvancedQuicksort()
    return sorter.introsort(arr, **kwargs)


def quicksort_parallel(arr: List[Any], **kwargs) -> List[Any]:
    """Convenience function for parallel quicksort."""
    sorter = AdvancedQuicksort()
    return sorter.parallel_quicksort(arr, **kwargs)


if __name__ == "__main__":
    # Example usage and testing
    test_arrays = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 4, 6, 1, 3],
        [1, 2, 3, 4, 5],  # Already sorted
        [5, 4, 3, 2, 1],  # Reverse sorted
        [3, 3, 3, 3, 3],  # All same elements
        [],
        [42],
        [random.randint(1, 1000) for _ in range(100)]
    ]
    
    sorter = AdvancedQuicksort()
    
    for arr in test_arrays:
        print(f"Original: {arr}")
        
        # Test different strategies
        sorted_random = sorter.sort(arr, pivot_strategy='random')
        sorted_median = sorter.sort(arr, pivot_strategy='median_of_three')
        sorted_introsort = sorter.introsort(arr)
        
        print(f"Random pivot: {sorted_random}")
        print(f"Median-of-three: {sorted_median}")
        print(f"Introsort: {sorted_introsort}")
        print("-" * 50)
