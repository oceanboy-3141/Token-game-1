"""
File Locking Utilities for Token Quest
Provides safe file operations to prevent race conditions in multi-user environment
"""

import os
import json
import csv
import time
import threading
import logging
from contextlib import contextmanager
from typing import Any, Dict, List

# Configure logging
logger = logging.getLogger(__name__)


class FileLock:
    """Simple file-based locking mechanism for cross-process safety"""
    
    def __init__(self, lock_file_path: str, timeout: int = 30):
        self.lock_file_path = lock_file_path + '.lock'
        self.timeout = timeout
        self.acquired = False
    
    def acquire(self) -> bool:
        """Acquire the file lock"""
        start_time = time.time()
        
        while time.time() - start_time < self.timeout:
            try:
                # Try to create lock file exclusively
                fd = os.open(self.lock_file_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                self.acquired = True
                return True
            except FileExistsError:
                # Lock file exists, wait a bit and try again
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error acquiring lock {self.lock_file_path}: {e}")
                return False
        
        return False
    
    def release(self):
        """Release the file lock"""
        if self.acquired:
            try:
                os.remove(self.lock_file_path)
                self.acquired = False
            except Exception as e:
                logger.error(f"Error releasing lock {self.lock_file_path}: {e}")
    
    def __enter__(self):
        if not self.acquire():
            raise TimeoutError(f"Could not acquire lock for {self.lock_file_path}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


@contextmanager
def safe_file_write(file_path: str, timeout: int = 30):
    """Context manager for safe file writing with locking"""
    lock = FileLock(file_path, timeout)
    try:
        with lock:
            yield file_path
    except TimeoutError:
        logger.warning(f"Could not acquire lock for {file_path} within {timeout} seconds")
        # Proceed without lock as fallback (not ideal but prevents total failure)
        yield file_path


def safe_json_write(file_path: str, data: Any, indent: int = 2, timeout: int = 30) -> bool:
    """Safely write JSON data to file with locking"""
    try:
        with safe_file_write(file_path, timeout):
            # Write to temporary file first, then rename (atomic operation)
            temp_file = file_path + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, default=str)
            
            # Atomic rename
            if os.path.exists(file_path):
                backup_file = file_path + '.backup'
                os.rename(file_path, backup_file)
            
            os.rename(temp_file, file_path)
            
            # Clean up backup if write was successful
            backup_file = file_path + '.backup'
            if os.path.exists(backup_file):
                os.remove(backup_file)
            
            return True
    except Exception as e:
        logger.error(f"Error in safe_json_write for {file_path}: {e}")
        # Clean up temp file if it exists
        temp_file = file_path + '.tmp'
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        return False


def safe_json_read(file_path: str, default_value: Any = None, timeout: int = 30) -> Any:
    """Safely read JSON data from file with locking"""
    if not os.path.exists(file_path):
        return default_value
    
    try:
        with safe_file_write(file_path, timeout):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error in safe_json_read for {file_path}: {e}")
        return default_value


def safe_csv_append(file_path: str, row_data: Dict, fieldnames: List[str], timeout: int = 30) -> bool:
    """Safely append a row to CSV file with locking"""
    try:
        with safe_file_write(file_path, timeout):
            file_exists = os.path.exists(file_path)
            
            with open(file_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                # Write header if file is new
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(row_data)
            
            return True
    except Exception as e:
        logger.error(f"Error in safe_csv_append for {file_path}: {e}")
        return False


def safe_file_operation(operation_func, file_path: str, *args, timeout: int = 30, **kwargs):
    """Generic safe file operation wrapper with locking"""
    try:
        with safe_file_write(file_path, timeout):
            return operation_func(file_path, *args, **kwargs)
    except Exception as e:
        logger.error(f"Error in safe_file_operation for {file_path}: {e}")
        return None


# Thread-local storage for in-memory locks (for same-process thread safety)
_thread_local = threading.local()

def get_memory_lock(lock_key: str) -> threading.Lock:
    """Get or create a thread lock for in-memory synchronization"""
    if not hasattr(_thread_local, 'locks'):
        _thread_local.locks = {}
    
    if lock_key not in _thread_local.locks:
        _thread_local.locks[lock_key] = threading.Lock()
    
    return _thread_local.locks[lock_key]


@contextmanager
def memory_lock(lock_key: str):
    """Context manager for in-memory thread synchronization"""
    lock = get_memory_lock(lock_key)
    lock.acquire()
    try:
        yield
    finally:
        lock.release()


class SafeFileManager:
    """Manager class for coordinating multiple file operations safely"""
    
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
    
    def write_json(self, filename: str, data: Any, indent: int = 2) -> bool:
        """Write JSON data safely"""
        file_path = os.path.join(self.base_dir, filename)
        return safe_json_write(file_path, data, indent)
    
    def read_json(self, filename: str, default_value: Any = None) -> Any:
        """Read JSON data safely"""
        file_path = os.path.join(self.base_dir, filename)
        return safe_json_read(file_path, default_value)
    
    def append_csv(self, filename: str, row_data: Dict, fieldnames: List[str]) -> bool:
        """Append to CSV file safely"""
        file_path = os.path.join(self.base_dir, filename)
        return safe_csv_append(file_path, row_data, fieldnames)
    
    def batch_write_json(self, file_data_pairs: List[tuple]) -> Dict[str, bool]:
        """Write multiple JSON files safely"""
        results = {}
        for filename, data in file_data_pairs:
            results[filename] = self.write_json(filename, data)
        return results 