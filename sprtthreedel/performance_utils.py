"""
Performance utilities for profiling, caching, and checkpointing.

This module provides utilities for:
- Performance profiling
- Caching expensive computations
- Checkpoint/resume functionality
- Progress indicators
"""

import os
import hashlib
import pickle
import json
import time
from pathlib import Path
from functools import wraps
from typing import Optional, Dict, Any
import psutil
import sys

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("Warning: tqdm not available. Install with: pip install tqdm")


def get_file_hash(filepath: str) -> str:
    """Calculate MD5 hash of a file to detect changes."""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        return ""


def get_memory_usage() -> float:
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def check_memory_threshold(threshold_mb: float = 2048) -> bool:
    """Check if memory usage exceeds threshold."""
    memory_mb = get_memory_usage()
    if memory_mb > threshold_mb:
        print(f"Warning: Memory usage ({memory_mb:.1f} MB) exceeds threshold ({threshold_mb} MB)")
        return True
    return False


class CacheManager:
    """Manages caching of expensive computations."""
    
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_path(self, key: str) -> Path:
        """Get cache file path for a given key."""
        return self.cache_dir / f"{key}.pkl"
    
    def get_metadata_path(self, key: str) -> Path:
        """Get metadata file path for a given key."""
        return self.cache_dir / f"{key}.meta"
    
    def save(self, key: str, data: Any, metadata: Optional[Dict] = None):
        """Save data to cache with metadata."""
        cache_path = self.get_cache_path(key)
        meta_path = self.get_metadata_path(key)
        
        # Save data
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)
        
        # Save metadata
        if metadata is None:
            metadata = {}
        metadata['timestamp'] = time.time()
        with open(meta_path, 'w') as f:
            json.dump(metadata, f)
    
    def load(self, key: str) -> Optional[Any]:
        """Load data from cache."""
        cache_path = self.get_cache_path(key)
        if cache_path.exists():
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        return None
    
    def is_valid(self, key: str, input_hash: Optional[str] = None) -> bool:
        """Check if cache entry is valid based on input hash."""
        meta_path = self.get_metadata_path(key)
        if not meta_path.exists():
            return False
        
        try:
            with open(meta_path, 'r') as f:
                metadata = json.load(f)
            
            if input_hash and metadata.get('input_hash') != input_hash:
                return False
            
            return True
        except:
            return False
    
    def clear(self, key: Optional[str] = None):
        """Clear cache entry or entire cache."""
        if key:
            self.get_cache_path(key).unlink(missing_ok=True)
            self.get_metadata_path(key).unlink(missing_ok=True)
        else:
            # Clear all cache
            for file in self.cache_dir.glob("*.pkl"):
                file.unlink()
            for file in self.cache_dir.glob("*.meta"):
                file.unlink()


class CheckpointManager:
    """Manages checkpoint/resume functionality."""
    
    def __init__(self, checkpoint_dir: str = ".checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)
    
    def save_checkpoint(self, stage: str, data: Any, metadata: Optional[Dict] = None):
        """Save checkpoint for a pipeline stage."""
        checkpoint_path = self.checkpoint_dir / f"{stage}.pkl"
        meta_path = self.checkpoint_dir / f"{stage}.meta"
        
        # Save checkpoint data
        with open(checkpoint_path, 'wb') as f:
            pickle.dump(data, f)
        
        # Save metadata
        if metadata is None:
            metadata = {}
        metadata['stage'] = stage
        metadata['timestamp'] = time.time()
        with open(meta_path, 'w') as f:
            json.dump(metadata, f)
    
    def load_checkpoint(self, stage: str) -> Optional[Any]:
        """Load checkpoint for a pipeline stage."""
        checkpoint_path = self.checkpoint_dir / f"{stage}.pkl"
        if checkpoint_path.exists():
            with open(checkpoint_path, 'rb') as f:
                return pickle.load(f)
        return None
    
    def get_last_checkpoint(self) -> Optional[str]:
        """Get the last checkpoint stage."""
        checkpoints = list(self.checkpoint_dir.glob("*.pkl"))
        if not checkpoints:
            return None
        
        # Get most recent checkpoint
        latest = max(checkpoints, key=lambda p: p.stat().st_mtime)
        return latest.stem
    
    def clear_checkpoints(self):
        """Clear all checkpoints."""
        for file in self.checkpoint_dir.glob("*.pkl"):
            file.unlink()
        for file in self.checkpoint_dir.glob("*.meta"):
            file.unlink()


def progress_bar(iterable, desc: str = "Processing", disable: bool = False):
    """Create a progress bar wrapper."""
    if TQDM_AVAILABLE and not disable:
        return tqdm(iterable, desc=desc, file=sys.stdout)
    return iterable


def profile_function(func):
    """Decorator to profile function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = get_memory_usage()
        result = func(*args, **kwargs)
        end_time = time.time()
        end_memory = get_memory_usage()
        
        print(f"{func.__name__}: {end_time - start_time:.2f}s, "
              f"Memory: {end_memory - start_memory:.1f} MB")
        return result
    return wrapper
