"""
Advanced performance benchmarking for Quicksort implementations.
"""

import time
import random
import statistics
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from quicksort import quicksort, quicksort_inplace, quicksort_optimized
from advanced_quicksort import AdvancedQuicksort, quicksort_advanced, quicksort_introsort, quicksort_parallel


class PerformanceBenchmark:
    """Comprehensive performance benchmarking suite."""
    
    def __init__(self):
        self.sorters = {
            'Basic Quicksort': quicksort,
            'In-place Quicksort': lambda x: quicksort_inplace(x[:]) or x[:],
            'Optimized Quicksort': quicksort_optimized,
            'Advanced Quicksort': quicksort_advanced,
            'Introsort': quicksort_introsort,
            'Parallel Quicksort': quicksort_parallel,
            'Python Built-in': sorted
        }
        
        self.results = {}
    
    def generate_test_data(self, size: int, data_type: str = 'random') -> List[int]:
        """Generate test data of specified type."""
        if data_type == 'random':
            return [random.randint(1, size * 10) for _ in range(size)]
        elif data_type == 'sorted':
            return list(range(size))
        elif data_type == 'reverse':
            return list(range(size, 0, -1))
        elif data_type == 'nearly_sorted':
            arr = list(range(size))
            # Swap 1% of elements
            for _ in range(max(1, size // 100)):
                i, j = random.sample(range(size), 2)
                arr[i], arr[j] = arr[j], arr[i]
            return arr
        elif data_type == 'duplicates':
            return [random.randint(1, size // 10) for _ in range(size)]
        else:
            return [random.randint(1, size * 10) for _ in range(size)]
    
    def benchmark_single(self, arr: List[int], algorithm_name: str, 
                        algorithm_func) -> Dict[str, Any]:
        """Benchmark a single algorithm on given data."""
        # Warm up
        for _ in range(3):
            algorithm_func(arr[:])
        
        # Actual benchmark
        times = []
        memory_usage = []
        
        for _ in range(5):
            test_arr = arr[:]
            
            # Measure time
            start_time = time.perf_counter()
            result = algorithm_func(test_arr)
            end_time = time.perf_counter()
            
            # Verify correctness
            assert result == sorted(arr), f"Algorithm {algorithm_name} failed"
            
            times.append(end_time - start_time)
        
        return {
            'mean_time': statistics.mean(times),
            'median_time': statistics.median(times),
            'std_time': statistics.stdev(times) if len(times) > 1 else 0,
            'min_time': min(times),
            'max_time': max(times)
        }
    
    def run_comprehensive_benchmark(self, sizes: List[int] = None, 
                                  data_types: List[str] = None) -> Dict[str, Any]:
        """Run comprehensive benchmark across different sizes and data types."""
        if sizes is None:
            sizes = [100, 1000, 5000, 10000, 50000]
        
        if data_types is None:
            data_types = ['random', 'sorted', 'reverse', 'nearly_sorted', 'duplicates']
        
        results = {}
        
        for size in sizes:
            results[size] = {}
            for data_type in data_types:
                print(f"Benchmarking size {size}, type {data_type}...")
                
                test_data = self.generate_test_data(size, data_type)
                results[size][data_type] = {}
                
                for algo_name, algo_func in self.sorters.items():
                    try:
                        benchmark_result = self.benchmark_single(
                            test_data, algo_name, algo_func
                        )
                        results[size][data_type][algo_name] = benchmark_result
                        print(f"  {algo_name}: {benchmark_result['mean_time']:.4f}s")
                    except Exception as e:
                        print(f"  {algo_name}: Failed - {str(e)}")
                        results[size][data_type][algo_name] = None
        
        self.results = results
        return results
    
    def create_performance_plots(self, output_dir: str = 'benchmark_results'):
        """Create performance visualization plots."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Plot 1: Performance vs Array Size
        self._plot_size_performance(output_dir)
        
        # Plot 2: Performance by Data Type
        self._plot_data_type_performance(output_dir)
        
        # Plot 3: Algorithm Comparison
        self._plot_algorithm_comparison(output_dir)
        
        # Plot 4: Speedup Analysis
        self._plot_speedup_analysis(output_dir)
    
    def _plot_size_performance(self, output_dir: str):
        """Plot performance vs array size."""
        plt.figure(figsize=(12, 8))
        
        sizes = sorted(self.results.keys())
        for algo_name in self.sorters.keys():
            times = []
            for size in sizes:
                # Use random data for this plot
                if self.results[size]['random'] and self.results[size]['random'].get(algo_name):
                    times.append(self.results[size]['random'][algo_name]['mean_time'])
                else:
                    times.append(None)
            
            # Filter out None values
            valid_times = [t for t in times if t is not None]
            valid_sizes = [s for s, t in zip(sizes, times) if t is not None]
            
            if valid_times:
                plt.plot(valid_sizes, valid_times, marker='o', label=algo_name)
        
        plt.xlabel('Array Size')
        plt.ylabel('Time (seconds)')
        plt.title('Performance vs Array Size (Random Data)')
        plt.legend()
        plt.grid(True)
        plt.xscale('log')
        plt.yscale('log')
        plt.savefig(os.path.join(output_dir, 'performance_vs_size.png'))
        plt.close()
    
    def _plot_data_type_performance(self, output_dir: str):
        """Plot performance by data type."""
        plt.figure(figsize=(15, 10))
        
        data_types = ['random', 'sorted', 'reverse', 'nearly_sorted', 'duplicates']
        algorithms = list(self.sorters.keys())
        
        # Use a representative size (e.g., 10000)
        target_size = 10000
        if target_size not in self.results:
            target_size = max(self.results.keys())
        
        data = []
        for algo in algorithms:
            row = []
            for data_type in data_types:
                if (self.results[target_size].get(data_type) and 
                    self.results[target_size][data_type].get(algo)):
                    row.append(self.results[target_size][data_type][algo]['mean_time'])
                else:
                    row.append(0)
            data.append(row)
        
        # Create heatmap
        data = np.array(data)
        plt.imshow(data, cmap='hot', interpolation='nearest', aspect='auto')
        plt.colorbar(label='Time (seconds)')
        plt.xticks(range(len(data_types)), data_types, rotation=45)
        plt.yticks(range(len(algorithms)), algorithms)
        plt.title(f'Performance by Data Type (Size: {target_size})')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'performance_by_data_type.png'))
        plt.close()
    
    def _plot_algorithm_comparison(self, output_dir: str):
        """Plot detailed algorithm comparison."""
        plt.figure(figsize=(15, 10))
        
        # Use largest size for comparison
        max_size = max(self.results.keys())
        
        algorithms = list(self.sorters.keys())
        times = []
        stds = []
        
        for algo in algorithms:
            if (self.results[max_size]['random'] and 
                self.results[max_size]['random'].get(algo)):
                times.append(self.results[max_size]['random'][algo]['mean_time'])
                stds.append(self.results[max_size]['random'][algo]['std_time'])
            else:
                times.append(0)
                stds.append(0)
        
        x_pos = np.arange(len(algorithms))
        
        plt.bar(x_pos, times, yerr=stds, capsize=5, alpha=0.7)
        plt.xlabel('Algorithm')
        plt.ylabel('Time (seconds)')
        plt.title(f'Algorithm Performance Comparison (Size: {max_size})')
        plt.xticks(x_pos, algorithms, rotation=45, ha='right')
        plt.grid(True, axis='y')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'algorithm_comparison.png'))
        plt.close()
    
    def _plot_speedup_analysis(self, output_dir: str):
        """Plot speedup analysis."""
        plt.figure(figsize=(12, 8))
        
        # Compare advanced algorithms to built-in sort
        sizes = sorted(self.results.keys())
        
        for algo_name in ['Advanced Quicksort', 'Introsort', 'Parallel Quicksort']:
            speedups = []
            for size in sizes:
                if (self.results[size]['random'] and 
                    self.results[size]['random'].get(algo_name) and
                    self.results[size]['random'].get('Python Built-in')):
                    
                    built_in_time = self.results[size]['random']['Python Built-in']['mean_time']
                    algo_time = self.results[size]['random'][algo_name]['mean_time']
                    speedups.append(built_in_time / algo_time if algo_time > 0 else 0)
                else:
                    speedups.append(0)
            
            plt.plot(sizes, speedups, marker='o', label=f'{algo_name} vs Built-in')
        
        plt.axhline(y=1, color='r', linestyle='--', label='Equal Performance')
        plt.xlabel('Array Size')
        plt.ylabel('Speedup (Built-in / Algorithm)')
        plt.title('Speedup Analysis vs Python Built-in Sort')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, 'speedup_analysis.png'))
        plt.close()
    
    def generate_report(self, output_dir: str = 'benchmark_results'):
        """Generate comprehensive benchmark report."""
        os.makedirs(output_dir, exist_ok=True)
        
        report_path = os.path.join(output_dir, 'benchmark_report.md')
        
        with open(report_path, 'w') as f:
            f.write("# Quicksort Performance Benchmark Report\n\n")
            f.write("## Executive Summary\n\n")
            f.write("This report presents comprehensive performance analysis of various Quicksort implementations.\n\n")
            
            f.write("## Test Configuration\n\n")
            f.write("- **Test Sizes**: " + ", ".join(map(str, sorted(self.results.keys()))) + "\n")
            f.write("- **Data Types**: random, sorted, reverse, nearly_sorted, duplicates\n")
            f.write("- **Iterations per test**: 5\n")
            f.write("- **Hardware**: Standard Python environment\n\n")
            
            f.write("## Results Summary\n\n")
            
            # Summary table
            f.write("| Algorithm | Best Case | Worst Case | Average |\n")
            f.write("|-----------|-----------|------------|---------|\n")
            
            for algo_name in self.sorters.keys():
                all_times = []
                for size_data in self.results.values():
                    for type_data in size_data.values():
                        if type_data and type_data.get(algo_name):
                            all_times.append(type_data[algo_name]['mean_time'])
                
                if all_times:
                    best = min(all_times)
                    worst = max(all_times)
                    avg = statistics.mean(all_times)
                    f.write(f"| {algo_name} | {best:.4f}s | {worst:.4f}s | {avg:.4f}s |\n")
            
            f.write("\n## Detailed Results\n\n")
            
            for size in sorted(self.results.keys()):
                f.write(f"### Size: {size}\n\n")
                for data_type in self.results[size].keys():
                    f.write(f"#### Data Type: {data_type}\n\n")
                    f.write("| Algorithm | Mean Time | Std Dev | Min Time | Max Time |\n")
                    f.write("|-----------|-----------|---------|----------|----------|\n")
                    
                    for algo_name, result in self.results[size][data_type].items():
                        if result:
                            f.write(f"| {algo_name} | {result['mean_time']:.4f}s | "
                                   f"{result['std_time']:.4f}s | {result['min_time']:.4f}s | "
                                   f"{result['max_time']:.4f}s |\n")
                    f.write("\n")


def main():
    """Main benchmarking function."""
    print("Starting comprehensive Quicksort benchmark...")
    
    benchmark = PerformanceBenchmark()
    
    # Run benchmarks
    results = benchmark.run_comprehensive_benchmark()
    
    # Generate plots and report
    benchmark.create_performance_plots()
    benchmark.generate_report()
    
    print("Benchmark complete! Results saved in 'benchmark_results' directory.")


if __name__ == "__main__":
    main()
