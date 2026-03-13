"""
Pytest configuration and shared fixtures for testing clean_data.py
"""
import pandas as pd
import pytest
import os
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_valid_data():
    """Create a sample DataFrame with valid STRING data format."""
    data = {
        'protein1': ['9606.ENSP00000123456', '9606.ENSP00000234567', '9606.ENSP00000345678'],
        'protein2': ['9606.ENSP00000456789', '9606.ENSP00000567890', '9606.ENSP00000678901'],
        'combined_score': [500, 600, 450]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_with_missing():
    """Create a sample DataFrame with missing values."""
    data = {
        'protein1': ['9606.ENSP00000123456', None, '9606.ENSP00000345678'],
        'protein2': ['9606.ENSP00000456789', '9606.ENSP00000567890', None],
        'combined_score': [500, 600, None]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_no_species_prefix():
    """Create a sample DataFrame without species prefix."""
    data = {
        'protein1': ['ENSP00000123456', 'ENSP00000234567'],
        'protein2': ['ENSP00000456789', 'ENSP00000567890'],
        'combined_score': [500, 600]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_with_self_interactions():
    """Create a sample DataFrame with self-interactions."""
    data = {
        'protein1': ['9606.ENSP00000123456', '9606.ENSP00000234567', '9606.ENSP00000345678'],
        'protein2': ['9606.ENSP00000456789', '9606.ENSP00000234567', '9606.ENSP00000345678'],
        'combined_score': [500, 600, 450]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_with_duplicates():
    """Create a sample DataFrame with duplicate interactions."""
    data = {
        'protein1': ['9606.ENSP00000123456', '9606.ENSP00000456789', '9606.ENSP00000123456'],
        'protein2': ['9606.ENSP00000456789', '9606.ENSP00000123456', '9606.ENSP00000456789'],
        'combined_score': [500, 500, 500]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_low_scores():
    """Create a sample DataFrame with scores below threshold."""
    data = {
        'protein1': ['9606.ENSP00000123456', '9606.ENSP00000234567', '9606.ENSP00000345678'],
        'protein2': ['9606.ENSP00000456789', '9606.ENSP00000567890', '9606.ENSP00000678901'],
        'combined_score': [300, 350, 399]  # All below 400 threshold
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_mixed_scores():
    """Create a sample DataFrame with mixed scores (above and below threshold)."""
    data = {
        'protein1': ['9606.ENSP00000123456', '9606.ENSP00000234567', '9606.ENSP00000345678', '9606.ENSP00000789012'],
        'protein2': ['9606.ENSP00000456789', '9606.ENSP00000567890', '9606.ENSP00000678901', '9606.ENSP00000890123'],
        'combined_score': [500, 300, 400, 450]  # Mixed: 500, 400, 450 above; 300 below
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_no_score_column():
    """Create a sample DataFrame without combined_score column."""
    data = {
        'protein1': ['9606.ENSP00000123456', '9606.ENSP00000234567'],
        'protein2': ['9606.ENSP00000456789', '9606.ENSP00000567890']
    }
    return pd.DataFrame(data)


@pytest.fixture
def empty_dataframe():
    """Create an empty DataFrame with correct columns."""
    return pd.DataFrame(columns=['protein1', 'protein2', 'combined_score'])


@pytest.fixture
def sample_data_single_interaction():
    """Create a sample DataFrame with a single interaction."""
    data = {
        'protein1': ['9606.ENSP00000123456'],
        'protein2': ['9606.ENSP00000456789'],
        'combined_score': [500]
    }
    return pd.DataFrame(data)
