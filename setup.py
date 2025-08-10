"""
Setup configuration for Quicksort Algorithm Implementation.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quicksort-algorithm",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Professional-grade Quicksort algorithm implementation in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quicksort-project",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "quicksort-benchmark=benchmarks.performance_test:run_comprehensive_benchmark",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
