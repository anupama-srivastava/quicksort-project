"""
Comprehensive test suite for Quicksort implementation.
"""

import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from quicksort import quicksort, quicksort_inplace, quicksort_optimized
from utils import is_sorted, generate_random_array, generate_sorted_array, \
    generate_reverse_sorted_array, generate_nearly_sorted_array


class TestQuicksort:
    """Test cases for the quicksort function."""
    
    def test_empty_list(self):
        """Test sorting empty list."""
        assert quicksort([]) == []
    
    def test_single_element(self):
        """Test sorting single element list."""
        assert quicksort([42]) == [42]
    
    def test_already_sorted(self):
        """Test sorting already sorted list."""
        arr = [1, 2, 3, 4, 5]
        result = quicksort(arr)
        assert result == [1, 2, 3, 4, 5]
        assert is_sorted(result)
    
    def test_reverse_sorted(self):
        """Test sorting reverse sorted list."""
        arr = [5, 4, 3, 2, 1]
        result = quicksort(arr)
        assert result == [1, 2, 3, 4, 5]
        assert is_sorted(result)
    
    def test_duplicates(self):
        """Test sorting list with duplicates."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        result = quicksort(arr)
        expected = [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
        assert result == expected
        assert is_sorted(result)
    
    def test_negative_numbers(self):
        """Test sorting list with negative numbers."""
        arr = [-5, 3, -1, 0, -8, 7, -2]
        result = quicksort(arr)
        expected = [-8, -5, -2, -1, 0, 3, 7]
        assert result == expected
        assert is_sorted(result)
    
    def test_floats(self):
        """Test sorting list with floating point numbers."""
        arr = [3.14, 2.71, 1.41, 1.73, 0.57]
        result = quicksort(arr)
        expected = [0.57, 1.41, 1.73, 2.71, 3.14]
        assert result == expected
        assert is_sorted(result)
    
    def test_strings(self):
        """Test sorting list of strings."""
        arr = ['banana', 'apple', 'cherry', 'date']
        result = quicksort(arr)
        expected = ['apple', 'banana', 'cherry', 'date']
        assert result == expected
        assert is_sorted(result)
    
    def test_reverse_sorting(self):
        """Test reverse sorting."""
        arr = [1, 2, 3, 4, 5]
        result = quicksort(arr, reverse=True)
        expected = [5, 4, 3, 2, 1]
        assert result == expected
        assert is_sorted(result, reverse=True)
    
    def test_key_function(self):
        """Test sorting with key function."""
        arr = ['apple', 'banana', 'cherry', 'date']
        result = quicksort(arr, key=len)
        expected = ['date', 'apple', 'banana', 'cherry']
        assert result == expected
    
    def test_large_random_array(self):
        """Test sorting large random array."""
        arr = generate_random_array(1000, -1000, 1000)
        result = quicksort(arr)
        assert is_sorted(result)
        assert len(result) == len(arr)
    
    def test_preserves_original(self):
        """Test that original array is not modified."""
        arr = [3, 1, 4, 1, 5]
        original = arr[:]
        result = quicksort(arr)
        assert arr == original
        assert result != original


class TestQuicksortInplace:
    """Test cases for the in-place quicksort function."""
    
    def test_empty_list(self):
        """Test in-place sorting empty list."""
        arr = []
        quicksort_inplace(arr)
        assert arr == []
    
    def test_single_element(self):
        """Test in-place sorting single element."""
        arr = [42]
        quicksort_inplace(arr)
        assert arr == [42]
    
    def test_sorting(self):
        """Test in-place sorting."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        quicksort_inplace(arr)
        assert arr == [1, 1, 2, 3, 4, 5, 6, 9]
        assert is_sorted(arr)
    
    def test_reverse_sorting(self):
        """Test in-place reverse sorting."""
        arr = [1, 2, 3, 4, 5]
        quicksort_inplace(arr, reverse=True)
        assert arr == [5, 4, 3, 2, 1]
        assert is_sorted(arr, reverse=True)


class TestQuicksortOptimized:
    """Test cases for the optimized quicksort function."""
    
    def test_empty_list(self):
        """Test optimized sorting empty list."""
        result = quicksort_optimized([])
        assert result == []
    
    def test_sorting(self):
        """Test optimized sorting."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        result = quicksort_optimized(arr)
        assert result == [1, 1, 2, 3, 4, 5, 6, 9]
        assert is_sorted(result)
    
    def test_large_array(self):
        """Test optimized sorting on large array."""
        arr = generate_random_array(1000)
        result = quicksort_optimized(arr)
        assert is_sorted(result)
        assert len(result) == len(arr)


class TestEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_none_values(self):
        """Test handling of None values."""
        arr = [3, None, 1, None, 2]
        with pytest.raises(TypeError):
            quicksort(arr)
    
    def test_mixed_types(self):
        """Test handling of mixed types."""
        arr = [1, 'a', 3.14, True]
        with pytest.raises(TypeError):
            quicksort(arr)
    
    def test_stability(self):
        """Test that sorting is not stable (expected for quicksort)."""
        # Create objects that compare equal but are different
        class TestObject:
            def __init__(self, value, id):
                self.value = value
                self.id = id
            
            def __lt__(self, other):
                return self.value < other.value
            
            def __eq__(self, other):
                return self.value == other.value
        
        arr = [TestObject(1, 1), TestObject(1, 2), TestObject(1, 3)]
        result = quicksort(arr)
        
        # Quicksort is not stable, so original order may not be preserved
        assert all(obj.value == 1 for obj in result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
