# Plan Two: Unit Tests for `clean_data.py`

## Block Overview

This two-week block focuses on implementing comprehensive unit tests for the `clean_data.py` module, which is responsible for cleaning and formatting STRING database interaction data. The main learning goals include:

- **Understanding pytest framework**: Learn to structure test files, use fixtures, and write effective test cases
- **Test-driven development practices**: Develop skills in identifying edge cases and writing tests that validate expected behavior
- **Data validation testing**: Learn to test data processing functions with various input scenarios including valid data, malformed data, and edge cases

**Main Development Milestones:**
- Create a complete test suite for all functions in `clean_data.py`
- Achieve >90% code coverage for the `clean_data.py` module
- Establish testing patterns that can be reused for other modules

**Anticipated Risks and Challenges:**
- **Risk**: Understanding the expected behavior of data cleaning functions may require careful analysis of the existing code
  - *Mitigation*: Start by reading the source code thoroughly and documenting expected behaviors before writing tests
- **Risk**: Creating realistic test data that covers all edge cases may be time-consuming
  - *Mitigation*: Use the existing `generate_example_data.py` as a starting point and create focused test fixtures
- **Risk**: Some edge cases (e.g., very large files, encoding issues) may be difficult to test
  - *Mitigation*: Focus on core functionality first, then add edge case tests incrementally
- **Blocker**: If the existing code has unclear behavior or bugs, tests may reveal issues that need to be fixed first
  - *Mitigation*: Document any discovered issues and create tests that demonstrate the expected (correct) behavior

## Planned Work

### Task 1: Set up test infrastructure
**Description**: Create the test directory structure and initial test file for `clean_data.py`. Set up pytest configuration and create helper fixtures for test data.

**Success Criteria**:
- `tests/` directory exists with `tests/test_clean_data.py` file
- `pytest.ini` or `pyproject.toml` configured with basic settings
- Can run `pytest tests/test_clean_data.py` and see test discovery working
- At least one placeholder test passes

**Estimated Time**: 2-3 hours

### Task 2: Test data loading functionality
**Description**: Write tests for the `load_string_data()` function to verify it correctly loads CSV files with various formats and handles errors appropriately.

**Success Criteria**:
- Test loading valid CSV file with correct format
- Test handling of missing file (should raise appropriate error)
- Test handling of empty CSV file
- Test handling of CSV files with different delimiters or encodings
- All tests pass and provide clear failure messages

**Estimated Time**: 3-4 hours

### Task 3: Test data cleaning - missing values and column validation
**Description**: Write tests for the data cleaning function's handling of missing values and column validation logic.

**Success Criteria**:
- Test removal of rows with missing values in required columns
- Test behavior when required columns (`protein1`, `protein2`) are missing
- Test automatic column renaming when columns are present but differently named
- Test error handling when DataFrame has insufficient columns
- Verify correct row counts before and after cleaning

**Estimated Time**: 3-4 hours

### Task 4: Test protein ID extraction and cleaning
**Description**: Write tests for the protein ID extraction logic that removes species prefixes and creates cleaned protein IDs.

**Success Criteria**:
- Test extraction of protein IDs with species prefix (e.g., "9606.ENSP...")
- Test extraction of protein IDs without species prefix
- Test handling of various protein ID formats
- Verify `protein1_clean` and `protein2_clean` columns are created correctly
- Test edge cases (empty strings, special characters)

**Estimated Time**: 2-3 hours

### Task 5: Test confidence score filtering
**Description**: Write tests for the filtering logic that removes interactions below the confidence threshold.

**Success Criteria**:
- Test filtering with `combined_score >= 400` threshold
- Test behavior when `combined_score` column is missing (should not filter)
- Test with various score distributions (all above, all below, mixed)
- Verify correct number of interactions removed
- Test edge cases (exactly at threshold, negative scores, very high scores)

**Estimated Time**: 2-3 hours

### Task 6: Test self-interaction removal
**Description**: Write tests to verify that self-interactions (where protein1 == protein2) are correctly removed.

**Success Criteria**:
- Test removal of explicit self-interactions
- Test that interactions where `protein1_clean == protein2_clean` are removed
- Test with data containing no self-interactions (should remain unchanged)
- Test with data containing only self-interactions (should result in empty DataFrame)
- Verify correct count of removed interactions

**Estimated Time**: 2 hours

### Task 7: Test duplicate interaction removal
**Description**: Write tests for the deduplication logic that removes duplicate interactions (A-B is same as B-A).

**Success Criteria**:
- Test removal of exact duplicate rows
- Test removal of duplicate interactions where A-B and B-A are both present
- Test that only one instance of each unique interaction pair is retained
- Test with data containing no duplicates (should remain unchanged)
- Verify interaction pairs are correctly normalized (sorted)

**Estimated Time**: 2-3 hours

### Task 8: Test data statistics function
**Description**: Write tests for the `get_data_statistics()` function to verify it correctly calculates and displays statistics.

**Success Criteria**:
- Test statistics calculation with known data (verify counts, means, medians)
- Test with empty DataFrame (should handle gracefully)
- Test with single interaction (edge case)
- Verify all statistics are calculated correctly (total interactions, unique proteins, score statistics, interaction counts)
- Test that function doesn't modify the input DataFrame

**Estimated Time**: 2 hours

### Task 9: Test save functionality
**Description**: Write tests for the `save_cleaned_data()` function to verify it correctly saves data to CSV files.

**Success Criteria**:
- Test saving to valid file path
- Test that saved file can be loaded and matches original data
- Test handling of invalid file paths (permissions, directory doesn't exist)
- Test that function returns the output file path
- Verify file is created with correct format

**Estimated Time**: 1-2 hours

### Task 10: Integration test - full cleaning workflow
**Description**: Write an integration test that exercises the complete data cleaning workflow from loading through saving.

**Success Criteria**:
- Test complete workflow: load → clean → get statistics → save
- Test with realistic example data (use generated test data)
- Verify all intermediate steps produce expected results
- Test that output file matches expected cleaned data format
- Test error propagation through the workflow

**Estimated Time**: 2-3 hours

### Task 11: Code coverage and test quality review
**Description**: Run coverage analysis, review test quality, and add any missing test cases to achieve >90% coverage.

**Success Criteria**:
- Run `pytest --cov=clean_data --cov-report=html` and achieve >90% coverage
- Review coverage report and identify untested code paths
- Add tests for any missing edge cases
- Ensure all tests have clear, descriptive names
- Verify tests are fast (all tests should complete in <10 seconds)

**Estimated Time**: 3-4 hours

## Backlog Items

The following tasks from Sprint 1 are planned for future blocks and will not be addressed in this two-week period:

- Unit tests for `build_graph.py` (handling disconnected components, edge cases)
- Unit tests for `compute_centrality.py` (centrality measure validation, hub score calculation)
- Unit tests for `visualize_network.py` (visualization file generation, error handling)
- Integration tests for `run_pipeline.py` (full pipeline testing with various datasets)
- GitHub Actions workflow setup for automated testing
- Linting configuration (`.pylintrc` or `pyproject.toml`)
- Test coverage reporting setup for the entire project (currently focusing on single module)

Additionally, the following broader project items remain in the backlog:

- Performance optimization for large datasets (Sprint 3)
- Advanced network analysis features (Sprint 4)
- Enhanced visualization capabilities (Sprint 5)
- Comprehensive API documentation (Sprint 6)
- Package distribution and deployment (Sprint 7)

## Deliverables

By the end of this two-week block, the following artifacts will be produced:

### Code Artifacts
- **`tests/test_clean_data.py`**: Complete test suite with 30+ test cases covering all functions in `clean_data.py`
- **`tests/conftest.py`**: Pytest configuration and shared fixtures for test data
- **`tests/fixtures/`**: Directory containing sample CSV files for testing (valid data, malformed data, edge cases)
- **Updated `pytest.ini` or `pyproject.toml`**: Test configuration file with coverage settings

### Documentation Artifacts
- **Test coverage report**: HTML coverage report showing >90% coverage for `clean_data.py`
- **Test documentation**: Inline comments and docstrings explaining test scenarios
- **Brief reflection notes**: Document lessons learned about testing data processing functions, any bugs discovered, and testing patterns established

### Quality Metrics
- **Code coverage**: >90% line coverage for `clean_data.py` module
- **Test count**: 30+ individual test cases
- **Test execution time**: All tests complete in <10 seconds
- **Test reliability**: All tests pass consistently across multiple runs

### Optional Deliverables (if time permits)
- **Test performance benchmarks**: Document test execution times
- **Testing best practices document**: Notes on patterns and practices established for future test development
- **Bug reports**: If any bugs are discovered in `clean_data.py` during testing, document them with reproduction steps
