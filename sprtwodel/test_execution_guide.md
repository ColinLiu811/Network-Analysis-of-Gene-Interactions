# Test Execution Guide

## Quick Start

To run the tests for `clean_data.py`, follow these steps:

### Option 1: Using the Setup Script (Recommended)

```bash
./setup_and_test.sh
```

This script will:
1. Install pytest and pytest-cov
2. Run all tests with coverage
3. Generate HTML coverage report

### Option 2: Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install just testing dependencies
pip install pytest pytest-cov
```

### Option 3: Using Python's pip module

```bash
python3 -m pip install pytest pytest-cov
```

## Running Tests

### Run all tests
```bash
pytest tests/test_clean_data.py -v
```

### Run with coverage report
```bash
pytest tests/test_clean_data.py --cov=clean_data --cov-report=html --cov-report=term-missing
```

### Run specific test classes
```bash
# Test data loading
pytest tests/test_clean_data.py::TestLoadStringData -v

# Test data cleaning
pytest tests/test_clean_data.py::TestCleanStringData -v

# Test saving
pytest tests/test_clean_data.py::TestSaveCleanedData -v

# Test statistics
pytest tests/test_clean_data.py::TestGetDataStatistics -v

# Test integration
pytest tests/test_clean_data.py::TestIntegrationWorkflow -v
```

### Run by marker
```bash
# Run only unit tests
pytest -m unit -v

# Run only integration tests
pytest -m integration -v
```

## Viewing Coverage Reports

After running tests with coverage, you'll get:

1. **Terminal output**: Shows coverage summary with missing lines
2. **HTML report**: Open `htmlcov/index.html` in your browser for detailed coverage

### Coverage Goals

- **Target**: >90% line coverage for `clean_data.py`
- **Current Status**: All tests written, coverage to be verified after running tests

## Expected Test Results

When tests run successfully, you should see:

```
tests/test_clean_data.py::TestLoadStringData::test_load_valid_csv_file PASSED
tests/test_clean_data.py::TestLoadStringData::test_load_missing_file PASSED
...
========================================= test session starts =========================================
collected 40+ items

tests/test_clean_data.py .................................. [100%]

========================================= 40+ passed in X.XXs =========================================

---------- coverage: platform darwin, python 3.x.x -----------
Name           Stmts   Miss  Cover
-----------------------------------
clean_data.py    146      X    9X%
-----------------------------------
TOTAL             146      X    9X%
```

## Troubleshooting

### Issue: "No module named 'pytest'"
**Solution**: Install pytest using one of the methods above

### Issue: "Permission denied" when installing
**Solutions**:
- Try: `pip install --user pytest pytest-cov`
- Or: `python3 -m pip install --user pytest pytest-cov`
- Or use a virtual environment: `python3 -m venv venv && source venv/bin/activate && pip install pytest pytest-cov`

### Issue: Tests fail with import errors
**Solution**: Make sure you're running from the project root directory where `clean_data.py` is located

### Issue: Coverage report not generated
**Solution**: Make sure `pytest-cov` is installed: `pip install pytest-cov`

## Test Structure

The test suite is organized as follows:

- **40+ test cases** covering all functions
- **5 test classes** organized by function
- **11 fixtures** for reusable test data
- **3 fixture files** for CSV test data

## Next Steps After Running Tests

1. **Review coverage report**: Open `htmlcov/index.html` to see which lines are covered
2. **Check for gaps**: Identify any untested code paths
3. **Add missing tests**: If coverage is below 90%, add tests for uncovered lines
4. **Verify all tests pass**: All 40+ tests should pass

## Continuous Integration

To set up automated testing:

1. Create `.github/workflows/test.yml` (if using GitHub Actions)
2. Configure to run `pytest tests/test_clean_data.py --cov=clean_data --cov-report=xml`
3. Set coverage threshold in CI configuration

## Notes

- All test files have been validated for syntax errors
- Tests are designed to run quickly (<10 seconds total)
- Tests use temporary directories to avoid file conflicts
- All fixtures are properly isolated and cleaned up after tests
