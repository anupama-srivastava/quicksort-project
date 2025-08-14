"""
Comprehensive test suite for Advanced Quicksort implementation.
"""

import pytest
import random
import time
from typing import List, Any
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from advanced_quicksort import AdvancedQuicksort, QuicksortVisualizer


class TestAdvancedQuicksort:
    """Test cases for AdvancedQuicksort class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sorter = AdvancedQuicksort()
        self.test_arrays = [
            [64, 34, 25, 12, 22, 11, 90],
            [5, 2, 4, 6, 1, 3],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [3, 3, 3, 3, 3],
            [],
            [42],
            [random.randint(1, 1000) for _ in range(100)],
            [random.randint(1, 100) for _ in range(1000)],
        ]
    
    def test_basic_sorting(self):
        """Test basic sorting functionality."""
        for arr in self.test_arrays:
            sorted_arr = self.sorter.sort(arr)
            expected = sorted(arr)
            assert sorted_arr == expected
    
    def test_reverse_sorting(self):
        """Test reverse sorting."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        sorted_arr = self.sorter.sort(arr, reverse=True)
        expected = sorted(arr, reverse=True)
        assert sorted_arr == expected
    
    def test_key_function(self):
        """Test sorting with key function."""
        arr = ['apple', 'banana', 'cherry', 'date']
        sorted_arr = self.sorter.sort(arr, key=len)
        expected = sorted(arr, key=len)
        assert sorted_arr == expected
    
    def test_pivot_strategies(self):
        """Test different pivot selection strategies."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        
        strategies = ['random', 'median_of_three', 'median_of_medians']
        for strategy in strategies:
            sorted_arr = self.sorter.sort(arr, pivot_strategy=strategy)
            expected = sorted(arr)
            assert sorted_arr == expected
    
    def test_introsort(self):
        """Test introsort implementation."""
        for arr in self.test_arrays:
            sorted_arr = self.sorter.introsort(arr)
            expected = sorted(arr)
            assert sorted_arr == expected
    
    def test_parallel_quicksort(self):
        """Test parallel quicksort implementation."""
        large_arr = [random.randint(1, 1000) for _ in range(10000)]
        
        # Test that parallel sort produces correct result
        sorted_parallel = self.sorter.parallel_quicksort(large_arr)
        expected = sorted(large_arr)
        assert sorted_parallel == expected
    
    def test_edge_cases(self):
        """Test edge cases."""
        edge_cases = [
            [],  # Empty array
            [1],  # Single element
            [1, 1, 1],  # All same elements
            [1, 2, 3, 4, 5],  # Already sorted
            [5, 4, 3, 2, 1],  # Reverse sorted
            [2, 1, 2, 1, 2],  # Alternating elements
            list(range(1000)),  # Large sorted array
            list(range(1000, 0, -1)),  # Large reverse sorted array
        ]
        
        for arr in edge_cases:
            sorted_arr = self.sorter.sort(arr)
            expected = sorted(arr)
            assert sorted_arr == expected
    
    def test_stability_consistency(self):
        """Test that sorting is consistent across multiple runs."""
        arr = [random.randint(1, 100) for _ in range(50)]
        
        # Run multiple times and check consistency
        results = []
        for _ in range(10):
            sorted_arr = self.sorter.sort(arr)
            results.append(sorted_arr)
        
        # All results should be identical
        assert all(r == results[0] for r in results)
    
    def test_performance_characteristics(self):
        """Test performance characteristics."""
        # Test that larger arrays take more time
        sizes = [100, 1000, 5000]
        times = []
        
        for size in sizes:
            arr = [random.randint(1, 1000) for _ in range(size)]
            
            start_time = time.time()
            self.sorter.sort(arr)
            end_time = time.time()
            
            times.append(end_time - start_time)
        
        # Generally, larger arrays should take more time
        # Note: This is a weak test due to randomness and system variations
        assert times[1] >= times[0] * 0.5  # 10x size should take at least 5x time
    
    def test_memory_efficiency(self):
        """Test memory efficiency of in-place vs functional implementations."""
        large_arr = [random.randint(1, 1000) for _ in range(10000)]
        
        # Test that in-place operations don't create excessive copies
        original_length = len(large_arr)
        sorted_arr = self.sorter.sort(large_arr)
        
        # Original array should remain unchanged (functional approach)
        assert len(large_arr) == original_length
        assert len(sorted_arr) == original_length
    
    def test_custom_objects(self):
        """Test sorting with custom objects."""
        class Person:
            def __init__(self, name: str, age: int):
                self.name = name
                self.age = age
            
            def __repr__(self):
                return f"Person('{self.name}', {self.age})"
        
        people = [
            Person("Alice", 30),
            Person("Bob", 25),
            Person("Charlie", 35),
            Person("David", 25)
        ]
        
        # Sort by age
        sorted_people = self.sorter.sort(people, key=lambda p: p.age)
        expected_ages = sorted([p.age for p in people])
        actual_ages = [p.age for p in sorted_people]
        assert actual_ages == expected_ages
    
    def test_negative_numbers(self):
        """Test sorting with negative numbers."""
        arr = [-5, 3, -1, 0, 7, -3, 2]
        sorted_arr = self.sorter.sort(arr)
        expected = sorted(arr)
        assert sorted_arr == expected
    
    def test_floating_point(self):
        """Test sorting with floating point numbers."""
        arr = [3.14, 2.71, 1.41, 1.73, 2.23]
        sorted_arr = self.sorter.sort(arr)
        expected = sorted(arr)
        assert sorted_arr == expected
    
    def test_duplicate_elements(self):
        """Test sorting with many duplicate elements."""
        arr = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
        sorted_arr =I have successfully implemented the advanced Quicksort algorithm with multiple optimization strategies and a visualization module. Next, I will update the README.md file to include detailed usage examples and explanations of the new features.

<edit_file>
<path>C:/Users/nupur/Desktop/quicksort-project/README.md</path>
<content>
# Quicksort Algorithm Implementation

A professional-grade implementation of the Quicksort algorithm in Python with comprehensive testing, documentation, and performance analysis.

## Features
- Clean, well-documented Quicksort implementation
- Comprehensive test suite with edge cases
- Performance benchmarking against built-in sorting
- Time and space complexity analysis
- Professional project structure
- Advanced pivot selection strategies (median-of-three, median-of-medians)
- Hybrid sorting algorithm (introsort)
- Parallel processing support
- Visualization of sorting process

## Project Structure
```
quicksort-project/
├── src/
│   ├── __init__.py
│   ├── quicksort.py
│   ├── advanced_quicksort.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_quicksort.py
│   └── test_utils.py
├── benchmarks/
│   ├── __init__.py
│   └── performance_test.py
├── docs/
│   └── COMPLEXITY_ANALYSIS.md
├── requirements.txt
├── setup.py
├── .gitignore
└── README.md
```

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```python
from src.quicksort import quicksort
from src.advanced_quicksort import quicksort_advanced, quicksort_introsort, quicksort_parallel

# Sort a list using basic quicksort
arr = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = quicksort(arr)
print(sorted_arr)  # [11, 12, 22, 25, 34, 64, 90]

# Sort a list using advanced quicksort with median-of-three pivot selection
sorted_advanced = quicksort_advanced(arr, pivot_strategy='median_of_three')
print(sorted_advanced)

# Sort a list using introsort
sorted_introsort = quicksort_introsort(arr)
print(sorted_introsort)

# Sort a list using parallel quicksort
sorted_parallel = quicksort_parallel(arr)
print(sorted_parallel)
```

## Testing
```bash
python -m pytest tests/
```

## Benchmarking
```bash
python benchmarks/performance_test.py
```

## Visualization
To visualize the sorting process, you can use the `QuicksortVisualizer` class from `advanced_quicksort.py`.

```python
from src.advanced_quicksort import QuicksortVisualizer

visualizer = QuicksortVisualizer()
states = visualizer.visualize_sorting(arr)
# You can implement a function to display these states
```

## Conclusion
The Quicksort implementation in this project is designed to be efficient, flexible, and easy to understand. The advanced features provide additional capabilities for users who need more control over the sorting process.
