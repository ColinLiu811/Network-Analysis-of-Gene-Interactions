# Test Suite for clean_data.py

This directory contains comprehensive unit tests for the `clean_data.py` module.

## Setup

Install the required testing dependencies:

```bash
pip install -r requirements.txt
```

This will install `pytest` and `pytest-cov` along with other project dependencies.

## Running Tests

### Run all tests
```bash
pytest tests/test_clean_data.py -v
```

### Run with coverage report
```bash
pytest tests/test_clean_data.py --cov=clean_data --cov-report=html --cov-report=term-missing
```

This will generate:
- Terminal output with coverage summary
- HTML coverage report in `htmlcov/index.html`

### Run specific test classes
```bash
pytest tests/test_clean_data.py::TestLoadStringData -v
pytest tests/test_clean_data.py::TestCleanStringData -v
pytest tests/test_clean_data.py::TestSaveCleanedData -v
pytest tests/test_clean_data.py::TestGetDataStatistics -v
pytest tests/test_clean_data.py::TestIntegrationWorkflow -v
```

### Run by marker
```bash
pytest -m unit -v          # Run only unit tests
pytest -m integration -v    # Run only integration tests
```

## Test Structure

### Test Classes

1. **TestLoadStringData**: Tests for `load_string_data()` function
   - Valid CSV file loading
   - Missing file handling
   - Empty file handling
   - Fixture file loading

2. **TestCleanStringData**: Tests for `clean_string_data()` function
   - Missing value removal
   - Column validation and auto-renaming
   - Protein ID extraction (with/without species prefix)
   - Confidence score filtering
   - Self-interaction removal
   - Duplicate interaction removal
   - Index reset
   - Empty DataFrame handling

3. **TestSaveCleanedData**: Tests for `save_cleaned_data()` function
   - Saving to valid paths
   - File format verification
   - Return value verification

4. **TestGetDataStatistics**: Tests for `get_data_statistics()` function
   - Statistics calculation
   - Empty DataFrame handling
   - Single interaction edge case
   - Non-modification of input DataFrame

5. **TestIntegrationWorkflow**: Integration tests
   - Full workflow: load → clean → statistics → save
   - Realistic data processing
   - Error propagation

### Test Fixtures

Located in `tests/conftest.py`:
- `temp_dir`: Temporary directory for test files
- `sample_valid_data`: Valid STRING format data
- `sample_data_with_missing`: Data with missing values
- `sample_data_no_species_prefix`: Data without species prefix
- `sample_data_with_self_interactions`: Data with self-interactions
- `sample_data_with_duplicates`: Data with duplicate interactions
- `sample_data_low_scores`: Data with scores below threshold
- `sample_data_mixed_scores`: Data with mixed scores
- `sample_data_no_score_column`: Data without score column
- `empty_dataframe`: Empty DataFrame
- `sample_data_single_interaction`: Single interaction DataFrame

### Test Data Files

Located in `tests/fixtures/`:
- `valid_data.csv`: Valid STRING format data
- `data_with_missing.csv`: Data with missing values
- `empty_file.csv`: Empty CSV file

## Coverage Goals

- **Target**: >90% line coverage for `clean_data.py`
- **Current**: All major functions and edge cases are covered

## Test Count

The test suite includes **40+ individual test cases** covering:
- All public functions in `clean_data.py`
- Edge cases and error conditions
- Integration scenarios
- Data validation and transformation logic
