# Advanced Quicksort Algorithm Implementation

A comprehensive, production-ready implementation of the Quicksort algorithm in Python featuring multiple optimization strategies, advanced features, and extensive documentation.

## 🚀 Features

### Core Implementations
- **Basic Quicksort**: Clean, functional implementation with O(n log n) average complexity
- **In-place Quicksort**: Memory-efficient version that sorts arrays without additional space
- **Optimized Quicksort**: Advanced implementation with random pivot selection and tail recursion optimization
- **Advanced Quicksort**: Professional-grade implementation with multiple pivot strategies

### Advanced Features
- **Multiple Pivot Strategies**: Random, median-of-three, median-of-medians selection
- **Introsort**: Hybrid algorithm combining quicksort, heapsort, and insertion sort for guaranteed O(n log n) performance
- **Parallel Processing**: Multi-threaded implementation for large datasets
- **Visualization Tools**: Step-by-step sorting process visualization
- **Interactive CLI**: Command-line interface for demonstrations and testing

### Performance Optimizations
- **Tail Recursion Elimination**: Optimized recursive calls
- **Insertion Sort for Small Arrays**: Hybrid approach for better performance
- **Median-of-Three Pivot**: Reduces worst-case scenarios
- **Memory-Efficient**: In-place sorting options available

## 📁 Project Structure

```
quicksort-project/
├── src/
│   ├── quicksort.py              # Core quicksort implementations
│   ├── advanced_quicksort.py     # Advanced algorithms and optimizations
│   ├── utils.py                  # Utility functions
│   └── __init__.py
├── tests/
│   ├── test_quicksort.py         # Core algorithm tests
│   ├── test_advanced_quicksort.py # Advanced features tests
│   └── __init__.py
├── benchmarks/
│   ├── performance_test.py       # Performance benchmarking
│   ├── advanced_performance_test.py # Advanced benchmarking
│   └── __init__.py
├── cli.py                        # Interactive command-line interface
├── docs/
│   ├── COMPLEXITY_ANALYSIS.md    # Detailed complexity analysis
│   └── algorithm_comparison.md   # Algorithm comparison guide
├── requirements.txt              # Python dependencies
├── setup.py                      # Package installation
└── README.md                     # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install as Package
```bash
pip install -e .
```

## 🎯 Usage

### Basic Usage
```python
from src.quicksort import quicksort

# Sort a list
arr = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = quicksort(arr)
print(sorted_arr)  # [11, 12, 22, 25, 34, 64, 90]
```

### Advanced Usage
```python
from src.advanced_quicksort import AdvancedQuicksort

sorter = AdvancedQuicksort()

# Use different pivot strategies
result = sorter.sort(arr, pivot_strategy='median_of_three')

# Use introsort for guaranteed O(n log n)
result = sorter.introsort(arr)

# Use parallel processing for large arrays
result = sorter.parallel_quicksort(arr)
```

### Custom Key Functions
```python
# Sort by string length
words = ['apple', 'banana', 'cherry', 'date']
sorted_words = quicksort(words, key=len)

# Sort in descending order
sorted_desc = quicksort(arr, reverse=True)
```

## 🖥️ Command Line Interface

### Interactive Mode
```bash
python cli.py --interactive
```

### Run Specific Demos
```bash
# Sorting demonstration
python cli.py --demo "[64,34,25,12,22,11,90]"

# Visualization
python cli.py --viz "[5,2,4,6,1,3]"

# Performance comparison
python cli.py --perf "[100,50,75,25,12,88,33]"
```

## 🧪 Testing

### Run All Tests
```bash
python -m pytest tests/
```

### Run with Coverage
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test Files
```bash
python -m pytest tests/test_quicksort.py
python -m pytest tests/test_advanced_quicksort.py
```

## 📊 Benchmarking

### Basic Performance Test
```bash
python benchmarks/performance_test.py
```

### Advanced Performance Test
```bash
python benchmarks/advanced_performance_test.py
```

## 📈 Performance Comparison

| Algorithm | Best Case | Average Case | Worst Case | Memory | Stable |
|-----------|-----------|--------------|------------|--------|--------|
| Basic Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Optimized Quicksort | O(n log n) | O(n log n) | O(n log n) | O(log n) | No |
| Introsort | O(n log n) | O(n log n) | O(n log n) | O(log n) | No |
| Parallel Quicksort | O(n log n) | O(n log n/p) | O(n log n) | O(log n) | No |

*Note: p = number of processors*

## 🔧 Advanced Features

### Pivot Selection Strategies
- **Random Pivot**: Random element selection
- **Median-of-Three**: Median of first, middle, last elements
- **Median-of-Medians**: Linear-time selection algorithm
- **Adaptive Selection**: Strategy based on input characteristics

### Hybrid Algorithms
- **Introsort**: Quicksort + Heapsort + Insertion Sort
- **Parallel Processing**: Multi-threaded implementation
- **Adaptive Sorting**: Algorithm selection based on data patterns

### Visualization Tools
- **Step-by-Step Visualization**: See each sorting step
- **Performance Graphs**: Real-time performance monitoring
- **Algorithm Comparison**: Visual comparison of different approaches

## 📚 Documentation

### Detailed Documentation
- [Complexity Analysis](docs/COMPLEXITY_ANALYSIS.md) - Detailed time and space complexity analysis
- [Algorithm Comparison](docs/algorithm_comparison.md) - Side-by-side algorithm comparison
- [Usage Examples](docs/usage_examples.md) - Comprehensive usage examples

### API Documentation
- Full API documentation available in source code
- Comprehensive docstrings for all functions
- Type hints for better IDE support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## 🙏 Acknowledgments

- Inspired by classic algorithm textbooks
- Built with modern Python best practices
- Designed for both educational and production use

