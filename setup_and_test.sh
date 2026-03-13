#!/bin/bash
# Setup script to install dependencies and run tests for clean_data.py

set -e  # Exit on error

echo "=========================================="
echo "Setting up test environment"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "clean_data.py" ]; then
    echo "Error: clean_data.py not found. Please run this script from the project root."
    exit 1
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
python3 -m pip install --user pytest pytest-cov pandas numpy

# Verify installation
echo ""
echo "Verifying pytest installation..."
python3 -c "import pytest; print(f'pytest {pytest.__version__} installed')" || {
    echo "Error: pytest installation failed"
    exit 1
}

echo ""
echo "=========================================="
echo "Running tests"
echo "=========================================="

# Run tests with coverage
python3 -m pytest tests/test_clean_data.py -v --cov=clean_data --cov-report=term-missing --cov-report=html

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo ""
echo "Coverage report generated in htmlcov/index.html"
echo "Open it in a browser to see detailed coverage information."
echo ""
echo "To run tests again:"
echo "  pytest tests/test_clean_data.py -v"
echo ""
echo "To run with coverage:"
echo "  pytest tests/test_clean_data.py --cov=clean_data --cov-report=html"
