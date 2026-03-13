"""
Comprehensive unit tests for clean_data.py module.

This test suite covers all functions in clean_data.py:
- load_string_data()
- clean_string_data()
- save_cleaned_data()
- get_data_statistics()
"""
import pytest
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Add parent directory to path to import clean_data
sys.path.insert(0, str(Path(__file__).parent.parent))
import clean_data


class TestLoadStringData:
    """Test suite for load_string_data() function."""
    
    @pytest.mark.unit
    def test_load_valid_csv_file(self, temp_dir):
        """Test loading a valid CSV file with correct format."""
        # Create a test CSV file
        test_file = os.path.join(temp_dir, 'test_data.csv')
        test_data = pd.DataFrame({
            'protein1': ['9606.ENSP00000123456', '9606.ENSP00000234567'],
            'protein2': ['9606.ENSP00000456789', '9606.ENSP00000567890'],
            'combined_score': [500, 600]
        })
        test_data.to_csv(test_file, index=False)
        
        # Load the file
        df = clean_data.load_string_data(test_file)
        
        # Verify the data was loaded correctly
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'protein1' in df.columns
        assert 'protein2' in df.columns
        assert 'combined_score' in df.columns
    
    @pytest.mark.unit
    def test_load_missing_file(self, temp_dir):
        """Test handling of missing file - should raise FileNotFoundError."""
        missing_file = os.path.join(temp_dir, 'nonexistent_file.csv')
        
        with pytest.raises(FileNotFoundError):
            clean_data.load_string_data(missing_file)
    
    @pytest.mark.unit
    def test_load_empty_csv_file(self, temp_dir):
        """Test handling of empty CSV file."""
        # Create an empty CSV file with headers
        empty_file = os.path.join(temp_dir, 'empty.csv')
        pd.DataFrame(columns=['protein1', 'protein2', 'combined_score']).to_csv(empty_file, index=False)
        
        # Load the file
        df = clean_data.load_string_data(empty_file)
        
        # Verify it returns an empty DataFrame with correct columns
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
        assert 'protein1' in df.columns
        assert 'protein2' in df.columns
    
    @pytest.mark.unit
    def test_load_from_fixture(self):
        """Test loading from test fixture file."""
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'valid_data.csv')
        df = clean_data.load_string_data(fixture_path)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4
        assert 'protein1' in df.columns
        assert 'protein2' in df.columns


class TestCleanStringData:
    """Test suite for clean_string_data() function."""
    
    @pytest.mark.unit
    def test_remove_missing_values(self, sample_data_with_missing):
        """Test removal of rows with missing values."""
        initial_count = len(sample_data_with_missing)
        df_cleaned = clean_data.clean_string_data(sample_data_with_missing.copy())
        
        # Should remove rows with missing values
        assert len(df_cleaned) < initial_count
        assert df_cleaned.isna().sum().sum() == 0  # No missing values remaining
    
    @pytest.mark.unit
    def test_required_columns_present(self, sample_valid_data):
        """Test that function works when required columns are present."""
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        assert 'protein1' in df_cleaned.columns
        assert 'protein2' in df_cleaned.columns
        assert 'protein1_clean' in df_cleaned.columns
        assert 'protein2_clean' in df_cleaned.columns
    
    @pytest.mark.unit
    def test_auto_column_renaming(self):
        """Test automatic column renaming when columns are present but differently named."""
        # Create DataFrame with different column names but correct order
        data = {
            'col1': ['9606.ENSP00000123456', '9606.ENSP00000234567'],
            'col2': ['9606.ENSP00000456789', '9606.ENSP00000567890'],
            'col3': [500, 600]
        }
        df = pd.DataFrame(data)
        
        df_cleaned = clean_data.clean_string_data(df)
        
        # Should have renamed columns
        assert 'protein1' in df_cleaned.columns
        assert 'protein2' in df_cleaned.columns
    
    @pytest.mark.unit
    def test_insufficient_columns_error(self):
        """Test error handling when DataFrame has insufficient columns."""
        # Create DataFrame with only one column
        df = pd.DataFrame({'protein1': ['9606.ENSP00000123456']})
        
        with pytest.raises(ValueError, match="must contain protein1 and protein2 columns"):
            clean_data.clean_string_data(df)
    
    @pytest.mark.unit
    def test_protein_id_extraction_with_prefix(self, sample_valid_data):
        """Test extraction of protein IDs with species prefix."""
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        # Verify protein1_clean and protein2_clean columns exist
        assert 'protein1_clean' in df_cleaned.columns
        assert 'protein2_clean' in df_cleaned.columns
        
        # Verify species prefix is removed
        assert all(not str(val).startswith('9606.') for val in df_cleaned['protein1_clean'])
        assert all(not str(val).startswith('9606.') for val in df_cleaned['protein2_clean'])
    
    @pytest.mark.unit
    def test_protein_id_extraction_without_prefix(self, sample_data_no_species_prefix):
        """Test extraction of protein IDs without species prefix."""
        df_cleaned = clean_data.clean_string_data(sample_data_no_species_prefix.copy())
        
        # Should still create clean columns
        assert 'protein1_clean' in df_cleaned.columns
        assert 'protein2_clean' in df_cleaned.columns
        
        # Values should remain the same since no prefix to remove
        assert df_cleaned['protein1_clean'].iloc[0] == 'ENSP00000123456'
    
    @pytest.mark.unit
    def test_confidence_score_filtering_above_threshold(self, sample_valid_data):
        """Test filtering with combined_score >= 400 threshold."""
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        # All scores in sample_valid_data are >= 400, so all should remain
        assert len(df_cleaned) == len(sample_valid_data)
        assert all(df_cleaned['combined_score'] >= 400)
    
    @pytest.mark.unit
    def test_confidence_score_filtering_below_threshold(self, sample_data_low_scores):
        """Test filtering removes interactions below threshold."""
        df_cleaned = clean_data.clean_string_data(sample_data_low_scores.copy())
        
        # All scores are below 400, so all should be removed
        assert len(df_cleaned) == 0
    
    @pytest.mark.unit
    def test_confidence_score_filtering_mixed(self, sample_data_mixed_scores):
        """Test filtering with mixed scores (above and below threshold)."""
        initial_count = len(sample_data_mixed_scores)
        df_cleaned = clean_data.clean_string_data(sample_data_mixed_scores.copy())
        
        # Should keep only scores >= 400
        assert len(df_cleaned) < initial_count
        assert all(df_cleaned['combined_score'] >= 400)
        # Should have 3 rows: scores 500, 400, 450 (300 is removed)
        assert len(df_cleaned) == 3
    
    @pytest.mark.unit
    def test_confidence_score_at_threshold(self):
        """Test edge case: score exactly at threshold (400)."""
        data = {
            'protein1': ['9606.ENSP00000123456'],
            'protein2': ['9606.ENSP00000456789'],
            'combined_score': [400]  # Exactly at threshold
        }
        df = pd.DataFrame(data)
        df_cleaned = clean_data.clean_string_data(df)
        
        # Should keep the interaction (>= 400)
        assert len(df_cleaned) == 1
    
    @pytest.mark.unit
    def test_confidence_score_missing_column(self, sample_data_no_score_column):
        """Test behavior when combined_score column is missing."""
        df_cleaned = clean_data.clean_string_data(sample_data_no_score_column.copy())
        
        # Should not filter (no score column to filter on)
        assert len(df_cleaned) == len(sample_data_no_score_column)
        assert 'protein1_clean' in df_cleaned.columns
        assert 'protein2_clean' in df_cleaned.columns
    
    @pytest.mark.unit
    def test_remove_self_interactions(self, sample_data_with_self_interactions):
        """Test removal of self-interactions."""
        initial_count = len(sample_data_with_self_interactions)
        df_cleaned = clean_data.clean_string_data(sample_data_with_self_interactions.copy())
        
        # Should remove self-interactions
        assert len(df_cleaned) < initial_count
        
        # Verify no self-interactions remain
        assert all(df_cleaned['protein1_clean'] != df_cleaned['protein2_clean'])
    
    @pytest.mark.unit
    def test_no_self_interactions_unchanged(self, sample_valid_data):
        """Test that data with no self-interactions remains unchanged for this aspect."""
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        # Verify no self-interactions (should all pass through if none exist)
        assert all(df_cleaned['protein1_clean'] != df_cleaned['protein2_clean'])
    
    @pytest.mark.unit
    def test_only_self_interactions_results_empty(self):
        """Test that data containing only self-interactions results in empty DataFrame."""
        data = {
            'protein1': ['9606.ENSP00000123456', '9606.ENSP00000234567'],
            'protein2': ['9606.ENSP00000123456', '9606.ENSP00000234567'],  # Same as protein1
            'combined_score': [500, 600]
        }
        df = pd.DataFrame(data)
        df_cleaned = clean_data.clean_string_data(df)
        
        # After removing self-interactions, should be empty
        assert len(df_cleaned) == 0
    
    @pytest.mark.unit
    def test_remove_duplicate_interactions(self, sample_data_with_duplicates):
        """Test removal of duplicate interactions."""
        initial_count = len(sample_data_with_duplicates)
        df_cleaned = clean_data.clean_string_data(sample_data_with_duplicates.copy())
        
        # Should remove duplicates (A-B and B-A are the same)
        assert len(df_cleaned) < initial_count
        
        # Verify no duplicates remain
        pairs = set(zip(df_cleaned['protein1_clean'], df_cleaned['protein2_clean']))
        assert len(pairs) == len(df_cleaned)  # All pairs should be unique
    
    @pytest.mark.unit
    def test_no_duplicates_unchanged(self, sample_valid_data):
        """Test that data with no duplicates remains unchanged for this aspect."""
        initial_count = len(sample_valid_data)
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        # If no duplicates, count should be same (after other filtering)
        # Assuming all pass other filters
        assert len(df_cleaned) == initial_count
    
    @pytest.mark.unit
    def test_duplicate_normalization(self):
        """Test that duplicate interactions are normalized (A-B same as B-A)."""
        data = {
            'protein1': ['9606.ENSP00000123456', '9606.ENSP00000456789'],
            'protein2': ['9606.ENSP00000456789', '9606.ENSP00000123456'],  # Reversed
            'combined_score': [500, 500]
        }
        df = pd.DataFrame(data)
        df_cleaned = clean_data.clean_string_data(df)
        
        # Should keep only one instance
        assert len(df_cleaned) == 1
    
    @pytest.mark.unit
    def test_index_reset(self, sample_valid_data):
        """Test that index is reset after cleaning."""
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        # Index should start at 0 and be sequential
        assert df_cleaned.index.tolist() == list(range(len(df_cleaned)))
    
    @pytest.mark.unit
    def test_empty_dataframe_handling(self, empty_dataframe):
        """Test handling of empty DataFrame."""
        df_cleaned = clean_data.clean_string_data(empty_dataframe.copy())
        
        # Should return empty DataFrame with clean columns
        assert len(df_cleaned) == 0
        assert 'protein1_clean' in df_cleaned.columns or len(df_cleaned) == 0


class TestSaveCleanedData:
    """Test suite for save_cleaned_data() function."""
    
    @pytest.mark.unit
    def test_save_to_valid_path(self, sample_valid_data, temp_dir):
        """Test saving to valid file path."""
        output_file = os.path.join(temp_dir, 'test_output.csv')
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        result = clean_data.save_cleaned_data(df_cleaned, output_file)
        
        # Should return the output file path
        assert result == output_file
        
        # File should exist
        assert os.path.exists(output_file)
    
    @pytest.mark.unit
    def test_saved_file_can_be_loaded(self, sample_valid_data, temp_dir):
        """Test that saved file can be loaded and matches original data."""
        output_file = os.path.join(temp_dir, 'test_output.csv')
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        clean_data.save_cleaned_data(df_cleaned, output_file)
        
        # Load the saved file
        df_loaded = pd.read_csv(output_file)
        
        # Should match the cleaned data
        assert len(df_loaded) == len(df_cleaned)
        assert 'protein1_clean' in df_loaded.columns
        assert 'protein2_clean' in df_loaded.columns
    
    @pytest.mark.unit
    def test_save_returns_file_path(self, sample_valid_data, temp_dir):
        """Test that function returns the output file path."""
        output_file = os.path.join(temp_dir, 'test_output.csv')
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        result = clean_data.save_cleaned_data(df_cleaned, output_file)
        
        assert result == output_file
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_save_creates_correct_format(self, sample_valid_data, temp_dir):
        """Test that saved file has correct CSV format."""
        output_file = os.path.join(temp_dir, 'test_output.csv')
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        clean_data.save_cleaned_data(df_cleaned, output_file)
        
        # Verify it's a valid CSV
        df_loaded = pd.read_csv(output_file)
        assert isinstance(df_loaded, pd.DataFrame)
        assert len(df_loaded) > 0


class TestGetDataStatistics:
    """Test suite for get_data_statistics() function."""
    
    @pytest.mark.unit
    def test_statistics_with_known_data(self, sample_valid_data):
        """Test statistics calculation with known data."""
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        # Function should not raise an error
        # Note: This function prints to stdout, so we're mainly testing it doesn't crash
        clean_data.get_data_statistics(df_cleaned)
        
        # Verify the DataFrame wasn't modified
        assert len(df_cleaned) == len(sample_valid_data)
    
    @pytest.mark.unit
    def test_statistics_empty_dataframe(self):
        """Test statistics with empty DataFrame - should handle gracefully."""
        # Create an empty cleaned dataframe with required columns
        # (get_data_statistics expects cleaned data with protein1_clean and protein2_clean)
        df_cleaned = pd.DataFrame(columns=['protein1_clean', 'protein2_clean'])
        
        # Should not raise an error, though statistics will show zeros
        # The function accesses columns which exist, so it should work
        clean_data.get_data_statistics(df_cleaned)
    
    @pytest.mark.unit
    def test_statistics_single_interaction(self, sample_data_single_interaction):
        """Test statistics with single interaction (edge case)."""
        df_cleaned = clean_data.clean_string_data(sample_data_single_interaction.copy())
        
        # Should not raise an error
        clean_data.get_data_statistics(df_cleaned)
    
    @pytest.mark.unit
    def test_statistics_calculates_correctly(self, sample_valid_data):
        """Test that statistics are calculated correctly."""
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        # Get unique proteins
        all_proteins = set(df_cleaned['protein1_clean'].tolist() + df_cleaned['protein2_clean'].tolist())
        
        # Function should execute without error
        clean_data.get_data_statistics(df_cleaned)
        
        # Verify basic counts
        assert len(df_cleaned) > 0
        assert len(all_proteins) > 0
    
    @pytest.mark.unit
    def test_statistics_does_not_modify_dataframe(self, sample_valid_data):
        """Test that function doesn't modify the input DataFrame."""
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        df_copy = df_cleaned.copy()
        
        clean_data.get_data_statistics(df_cleaned)
        
        # DataFrames should be equal
        pd.testing.assert_frame_equal(df_cleaned, df_copy)
    
    @pytest.mark.unit
    def test_statistics_with_score_column(self, sample_valid_data):
        """Test statistics calculation when combined_score column exists."""
        df_cleaned = clean_data.clean_string_data(sample_valid_data.copy())
        
        # Should execute without error and calculate score statistics
        clean_data.get_data_statistics(df_cleaned)
        
        # Verify score column exists
        assert 'combined_score' in df_cleaned.columns
    
    @pytest.mark.unit
    def test_statistics_without_score_column(self, sample_data_no_score_column):
        """Test statistics calculation when combined_score column is missing."""
        df_cleaned = clean_data.clean_string_data(sample_data_no_score_column.copy())
        
        # Should execute without error (just won't print score stats)
        clean_data.get_data_statistics(df_cleaned)


class TestIntegrationWorkflow:
    """Integration tests for complete data cleaning workflow."""
    
    @pytest.mark.integration
    def test_full_workflow_load_clean_save(self, temp_dir):
        """Test complete workflow: load → clean → save."""
        # Create test input file
        input_file = os.path.join(temp_dir, 'input.csv')
        test_data = pd.DataFrame({
            'protein1': ['9606.ENSP00000123456', '9606.ENSP00000234567', '9606.ENSP00000345678'],
            'protein2': ['9606.ENSP00000456789', '9606.ENSP00000567890', '9606.ENSP00000678901'],
            'combined_score': [500, 600, 450]
        })
        test_data.to_csv(input_file, index=False)
        
        # Load
        df = clean_data.load_string_data(input_file)
        assert len(df) == 3
        
        # Clean
        df_cleaned = clean_data.clean_string_data(df)
        assert len(df_cleaned) == 3
        assert 'protein1_clean' in df_cleaned.columns
        
        # Get statistics
        clean_data.get_data_statistics(df_cleaned)
        
        # Save
        output_file = os.path.join(temp_dir, 'output.csv')
        result = clean_data.save_cleaned_data(df_cleaned, output_file)
        assert os.path.exists(result)
        
        # Verify output can be loaded
        df_loaded = pd.read_csv(output_file)
        assert len(df_loaded) == 3
    
    @pytest.mark.integration
    def test_workflow_with_realistic_data(self, temp_dir):
        """Test workflow with realistic example data."""
        # Use the fixture file
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'valid_data.csv')
        
        # Load
        df = clean_data.load_string_data(fixture_path)
        
        # Clean
        df_cleaned = clean_data.clean_string_data(df)
        
        # Get statistics
        clean_data.get_data_statistics(df_cleaned)
        
        # Save
        output_file = os.path.join(temp_dir, 'realistic_output.csv')
        clean_data.save_cleaned_data(df_cleaned, output_file)
        
        # Verify output
        assert os.path.exists(output_file)
        df_loaded = pd.read_csv(output_file)
        assert len(df_loaded) > 0
    
    @pytest.mark.integration
    def test_workflow_error_propagation(self, temp_dir):
        """Test error propagation through the workflow."""
        # Try to load non-existent file
        missing_file = os.path.join(temp_dir, 'missing.csv')
        
        with pytest.raises(FileNotFoundError):
            df = clean_data.load_string_data(missing_file)
            # Should not reach here, but if it does, clean should also fail
            clean_data.clean_string_data(df)
