"""
Performance benchmarking for Quicksort implementation.
"""

import time
import random
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from quicksort import quicksort, quicksort_optimized
from utils import generate_random_array, generate_sorted_array, generate_reverse_sorted_array


def measure_sorting_time(sort_func, arr: List[int]) -> float:
    """
    Measure the time taken to sort an array.
    
    Args:
        sort_func: Sorting function to test
        arr: Array to sort
    
    Returns:
        Time taken in seconds
    """
    start_time = time.perf_counter()
    sort_func(arr)
    end_time = time.perf_counter()
    return end_time - start_time


def benchmark_sorting_algorithms():
    """Benchmark different sorting algorithms against each other."""
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    algorithms = {
        'Quicksort': quicksort,
        'Quicksort Optimized': quicksort_optimized,
        'Python Built-in': sorted
    }
    
    results = {name: [] for name in algorithms.keys()}
    
    print("Benchmarking sorting algorithms...")
    print("-" * 60)
    print(f"{'Size':<10} {'Quicksort':<15} {'Optimized':<15} {'Built-in':<15}")
    print("-" * 60)
    
    for size in sizes:
        times = {}
        
        # Test with random arrays
        arr = generate_random_array(size, -1000, 1000)
        
        for name, algorithm in algorithms.items():
            if name == 'Python Built-in':
                test_arr = arr.copy()
                time_taken = measure_sorting_time(algorithm, test_arr)
            else:
                time_taken = measure_sorting_time(algorithm, arr)
            
            times[name] = time_taken
            results[name].append(time_taken)
        
        print(f"{size:<10} {times['Quicksort']:<15.6f} "
              f"{times['Quicksort Optimized']:<15.6f} {times['Python Built-in']:<15.6f}")
    
    return sizes, results


def benchmark_worst_case():
    """Benchmark worst-case scenarios."""
    sizes = [100, 500, 1000, 2000, 5000]
    
    print("\nBenchmarking worst-case scenarios...")
    print("-" * 50)
    print(f"{'Size':<10} {'Random':<15} {'Sorted':<15} {'Reverse':<15}")
    print("-" * 50)
    
    for size in sizes:
        # Random array
        random_arr = generate_random_array(size, -1000, 1000)
        random_time = measure_sorting_time(quicksort, random_arr)
        
        # Already sorted array
        sorted_arr = generate_sorted_array(size)
        sorted_time = measure_sorting_time(quicksort, sorted_arr)
        
        # Reverse sorted array
        reverse_arr = generate_reverse_sorted_array(size)
        reverse_time = measure_sorting_time(quicksort, reverse_arr)
        
        print(f"{size:<10} {random_time:<15.6f} {sorted_time:<15.6f} {reverse_time:<15.6f}")


def plot_performance_results(sizes: List[int], results: dict):
    """Plot performance comparison charts."""
    plt.figure(figsize=(12, 8))
    
    # Plot 1: Performance comparison
    plt.subplot(2, 2, 1)
    for name, times in results.items():
        plt.plot(sizes, times, marker='o', label=name)
    
    plt.xlabel('Array Size')
    plt.ylabel('Time (seconds)')
    plt.title('Sorting Algorithm Performance Comparison')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Log-log plot
    plt.subplot(2, 2, 2)
    for name, times in results.items():
        plt.loglog(sizes, times, marker='o', label=name)
    
    plt.xlabel('Array Size (log scale)')
    plt.ylabel('Time (log scale)')
    plt.title('Log-Log Performance Plot')
    plt.legend()
    plt.grid(True)
    
    # Plot 3: Relative performance
    plt.subplot(2, 2, 3)
    built_in_times = results['Python Built-in']
    for name, times in results.items():
        if name != 'Python Built-in':
            relative = [t/b for t, b in zip(times, built_in_times)]
            plt.plot(sizes, relative, marker='o', label=f'{name} vs Built-in')
    
    plt.xlabel('Array Size')
    plt.ylabel('Relative Time (vs Built-in)')
    plt.title('Relative Performance Comparison')
    plt.legend()
    plt.grid(True)
    
    # Plot 4: Theoretical vs Actual
    plt.subplot(2, 2, 4)
    theoretical = [n * np.log(n) for n in sizes]
    actual = results['Quicksort']
    
    # Normalize both to compare shapes
    theoretical_norm = [t/theoretical[-1] for t in theoretical]
    actual_norm = [a/actual[-1] for a in actual]
    
    plt.plot(sizes, theoretical_norm, 'r--', label='Theoretical O(n log n)')
    plt.plot(sizes, actual_norm, 'b-', label='Actual Performance')
    
    plt.xlabel('Array Size')
    plt.ylabel('Normalized Time')
    plt.title('Theoretical vs Actual Performance')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('benchmark_results.png', dpi=300, bbox_inches='tight')
    plt.show()


def memory_usage_analysis():
    """Analyze memory usage patterns."""
    sizes = [100, 1000, 5000, 10000]
    
    print("\nMemory Usage Analysis...")
    print("-" * 40)
    print(f"{'Size':<10} {'Memory (MB)':<15}")
    print("-" * 40)
    
    for size in sizes:
        arr = generate_random_array(size)
        
        # Measure memory before sorting
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024
        
        # Sort the array
        quicksort(arr)
        
        memory_after = process.memory_info().rss / 1024 / 1024
        
        print(f"{size:<10} {memory_after - memory_before:<15.2f}")


def run_comprehensive_benchmark():
    """Run all benchmarks and generate reports."""
    print("=" * 60)
    print("QUICKSORT PERFORMANCE BENCHMARK")
    print("=" * 60)
    
    # Basic performance benchmark
    sizes, results = benchmark_sorting_algorithms()
    
    # Worst-case scenarios
    benchmark_worst_case()
    
    # Memory analysis
    try:
        memory_usage_analysis()
    except ImportError:
        print("\nMemory analysis skipped (psutil not available)")
    
    # Generate plots
    try:
        plot_performance_results(sizes, results)
        print("\nPerformance plots saved as 'benchmark_results.png'")
    except ImportError:
        print("\nPlotting skipped (matplotlib not available)")
    
    print("\nBenchmark completed!")


if __name__ == "__main__":
    run_comprehensive_benchmark()
