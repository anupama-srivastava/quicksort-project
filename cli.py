#!/usr/bin/env python3
"""
Interactive CLI for Quicksort Algorithm Demonstration.

This module provides a command-line interface for:
- Testing different quicksort implementations
- Visualizing the sorting process
- Benchmarking performance
- Educational demonstrations
"""

import argparse
import sys
import os
import json
import time
from typing import List, Any, Optional

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from quicksort import quicksort, quicksort_inplace, quicksort_optimized
from advanced_quicksort import AdvancedQuicksort, QuicksortVisualizer


class QuicksortCLI:
    """Interactive CLI for Quicksort demonstrations."""
    
    def __init__(self):
        self.sorter = AdvancedQuicksort()
        self.visualizer = QuicksortVisualizer()
    
    def parse_array_input(self, input_str: str) -> List[int]:
        """Parse array input from string."""
        try:
            # Handle different input formats
            if input_str.startswith('[') and input_str.endswith(']'):
                # JSON-like format
                return json.loads(input_str)
            elif ',' in input_str:
                # Comma-separated
                return [int(x.strip()) for x in input_str.split(',')]
            else:
                # Space-separated
                return [int(x) for x in input_str.split()]
        except ValueError as e:
            raise ValueError(f"Invalid input format: {e}")
    
    def display_array(self, arr: List[Any], title: str = "Array"):
        """Display array in a formatted way."""
        print(f"\n{title}:")
        print(f"  Length: {len(arr)}")
        print(f"  Elements: {arr}")
        if arr:
            print(f"  Min: {min(arr)}, Max: {max(arr)}")
    
    def run_sorting_demo(self, arr: List[int], algorithm: str = 'all'):
        """Run sorting demonstration."""
        algorithms = {
            'basic': ('Basic Quicksort', quicksort),
            'inplace': ('In-place Quicksort', lambda x: quicksort_inplace(x[:]) or x[:]),
            'optimized': ('Optimized Quicksort', quicksort_optimized),
            'advanced': ('Advanced Quicksort', self.sorter.sort),
            'introsort': ('Introsort', self.sorter.introsort),
            'parallel': ('Parallel Quicksort', self.sorter.parallel_quicksort),
        }
        
        if algorithm == 'all':
            selected_algorithms = algorithms.items()
        else:
            selected_algorithms = [(algorithm, algorithms[algorithm])]
        
        print("\n" + "="*60)
        print("SORTING DEMONSTRATION")
        print("="*60)
        
        for algo_key, (name, func) in selected_algorithms:
            print(f"\n{name}:")
            start_time = time.time()
            sorted_arr = func(arr[:])
            end_time = time.time()
            
            print(f"  Original: {arr}")
            print(f"  Sorted:   {sorted_arr}")
            print(f"  Time:     {(end_time - start_time)*1000:.2f} ms")
            print(f"  Correct:  {sorted_arr == sorted(arr)}")
    
    def run_visualization_demo(self, arr: List[int]):
        """Run visualization demonstration."""
        print("\n" + "="*60)
        print("VISUALIZATION DEMONSTRATION")
        print("="*60)
        
        print("Generating step-by-step visualization...")
        states = self.visualizer.visualize_sorting(arr)
        
        print(f"\nTotal steps: {len(states)}")
        
        # Display first few and last few steps
        display_steps = min(10, len(states))
        for i, state in enumerate(states[:display_steps]):
            print(f"Step {i+1}: {state}")
        
        if len(states) > display_steps * 2:
            print("...")
            for i, state in enumerate(states[-display_steps:]):
                print(f"Step {len(states) - display_steps + i + 1}: {state}")
    
    def run_performance_test(self, arr: List[int], iterations: int = 5):
        """Run performance comparison."""
        algorithms = {
            'Basic Quicksort': quicksort,
            'In-place Quicksort': lambda x: quicksort_inplace(x[:]) or x[:],
            'Optimized Quicksort': quicksort_optimized,
            'Advanced Quicksort': self.sorter.sort,
            'Introsort': self.sorter.introsort,
            'Parallel Quicksort': self.sorter.parallel_quicksort,
            'Python Built-in': sorted,
        }
        
        print("\n" + "="*60)
        print("PERFORMANCE COMPARISON")
        print("="*60)
        
        results = {}
        
        for name, func in algorithms.items():
            times = []
            for _ in range(iterations):
                start_time = time.perf_counter()
                result = func(arr[:])
                end_time = time.perf_counter()
                
                # Verify correctness
                assert result == sorted(arr), f"{name} produced incorrect result"
                times.append(end_time - start_time)
            
            results[name] = {
                'mean': statistics.mean(times),
                'median': statistics.median(times),
                'min': min(times),
                'max': max(times),
                'std': statistics.stdev(times) if len(times) > 1 else 0
            }
        
        # Display results
        print(f"\nArray size: {len(arr)}")
        print(f"Iterations: {iterations}")
        print("\nResults (sorted by mean time):")
        print("-" * 80)
        print(f"{'Algorithm':<20} {'Mean (ms)':<12} {'Median (ms)':<12} {'Min (ms)':<12} {'Max (ms)':<12}")
        print("-" * 80)
        
        sorted_results = sorted(results.items(), key=lambda x: x[1]['mean'])
        for name, stats in sorted_results:
            print(f"{name:<20} {stats['mean']*1000:<12.2f} "
                  f"{stats['median']*1000:<12.2f} {stats['min']*1000:<12.2f} "
                  f"{stats['max']*1000:<12.2f}")
    
    def interactive_mode(self):
        """Run interactive mode."""
        print("\n" + "="*60)
        print("QUICKSORT INTERACTIVE MODE")
        print("="*60)
        print("Welcome to the Quicksort Interactive Demonstration!")
        print("\nAvailable commands:")
        print("  demo <array>     - Run sorting demonstration")
        print("  viz <array>      - Run visualization demonstration")
        print("  perf <array>     - Run performance comparison")
        print("  help             - Show this help")
        print("  quit             - Exit the program")
        print("\nArray formats:")
        print("  [1,2,3,4,5]      - JSON format")
        print("  1,2,3,4,5        - Comma-separated")
        print("  1 2 3 4 5        - Space-separated")
        
        while True:
            try:
                user_input = input("\nquicksort> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.interactive_mode()
                    continue
                
                # Parse command
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    print("Error: Please provide an array")
                    continue
                
                command, array_str = parts
                
                try:
                    arr = self.parse_array_input(array_str)
                    
                    if command == 'demo':
                        self.run_sorting_demo(arr)
                    elif command == 'viz':
                        self.run_visualization_demo(arr)
                    elif command == 'perf':
                        self.run_performance_test(arr)
                    else:
                        print(f"Error: Unknown command '{command}'. Type 'help' for available commands.")
                
                except ValueError as e:
                    print(f"Error: {e}")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description='Quicksort Algorithm Demonstration')
    parser.add_argument('--demo', metavar='ARRAY', help='Run sorting demonstration')
    parser.add_argument('--viz', metavar='ARRAY', help='Run visualization demonstration')
    parser.add_argument('--perf', metavar='ARRAY', help='Run performance comparison')
    parser.add_argument('--iterations', type=int, default=5, 
                       help='Number of iterations for performance tests')
    parser.add_argument('--interactive', action='store_true', 
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    cli = QuicksortCLI()
    
    if args.interactive:
        cli.interactive_mode()
    elif args.demo:
        try:
            arr = cli.parse_array_input(args.demo)
            cli.run_sorting_demo(arr)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.viz:
        try:
            arr = cli.parse_array_input(args.viz)
            cli.run_visualization_demo(arr)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.perf:
        try:
            arr = cli.parse_array_input(args.perf)
            cli.run_performance_test(arr, args.iterations)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Default to interactive mode
        cli.interactive_mode()


if __name__ == "__main__":
    main()
