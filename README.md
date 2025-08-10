# Quicksort Algorithm Implementation

A professional-grade implementation of the Quicksort algorithm in Python with comprehensive testing, documentation, and performance analysis.

## Features
- Clean, well-documented Quicksort implementation
- Comprehensive test suite with edge cases
- Performance benchmarking against built-in sorting
- Time and space complexity analysis
- Professional project structure

## Project Structure
```
quicksort-project/
├── src/
│   ├── __init__.py
│   ├── quicksort.py
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

# Sort a list
arr = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = quicksort(arr)
print(sorted_arr)  # [11, 12, 22, 25, 34, 64, 90]
```

## Testing
```bash
python -m pytest tests/
```

## Benchmarking
```bash
python benchmarks/performance_test.py
