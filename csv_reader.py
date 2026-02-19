import pandas as pd
import os
from typing import List, Dict, Optional


class GerenciadorCSV:
    """
    Manager for CSV data using pandas. Stores and retrieves dictionaries.
    """

    def __init__(self, file_path: str):
        """
        Initialize manager with CSV file path. If only a filename is provided,
        the file will be created under a `data/` folder next to this module.

        Args:
            file_path: filename or full path for the CSV file
        """
        # If only a filename was provided (no directory), place it in ./data
        if not os.path.dirname(file_path):
            root_dir = os.path.dirname(os.path.abspath(__file__))
            data_folder = os.path.join(root_dir, 'data')

            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            self.file_path = os.path.join(data_folder, file_path)
        else:
            self.file_path = file_path

        self.data_frame = None

        # Load existing file if present
        if os.path.exists(self.file_path):
            self._load_file()
        else:
            self.data_frame = pd.DataFrame()
    
    def _load_file(self):
        """Load CSV into the internal DataFrame."""
        try:
            self.data_frame = pd.read_csv(self.file_path)
        except Exception as e:
            print(f"Error loading file: {e}")
            self.data_frame = pd.DataFrame()
    
    def _save_file(self):
        """Save the internal DataFrame to the CSV file."""
        try:
            self.data_frame.to_csv(self.file_path, index=False)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def get_data(self) -> List[Dict]:
        """Return all records as a list of dictionaries."""
        if self.data_frame is None or self.data_frame.empty:
            return []
        return self.data_frame.to_dict('records')
    
    def save_data(self, data: Dict) -> bool:
        """Save a single record (dictionary) into the CSV."""
        try:
            new_df = pd.DataFrame([data])

            if self.data_frame.empty:
                self.data_frame = new_df
            else:
                self.data_frame = pd.concat([self.data_frame, new_df], ignore_index=True)

            return self._save_file()
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def save_multiple_data(self, data_list: List[Dict]) -> bool:
        """Save multiple records (list of dicts) into the CSV."""
        try:
            new_df = pd.DataFrame(data_list)

            if self.data_frame.empty:
                self.data_frame = new_df
            else:
                self.data_frame = pd.concat([self.data_frame, new_df], ignore_index=True)

            return self._save_file()
        except Exception as e:
            print(f"Error saving multiple data: {e}")
            return False
    
    def update_data(self, index: int, data: Dict) -> bool:
        """Update a record at a given index with the provided dictionary."""
        try:
            if index < 0 or index >= len(self.data_frame):
                print(f"Index {index} out of range")
                return False

            for key, value in data.items():
                self.data_frame.at[index, key] = value

            return self._save_file()
        except Exception as e:
            print(f"Error updating data: {e}")
            return False
    
    def delete_data(self, index: int) -> bool:
        """Delete the record at the specified index."""
        try:
            if index < 0 or index >= len(self.data_frame):
                print(f"Index {index} out of range")
                return False

            self.data_frame = self.data_frame.drop(index).reset_index(drop=True)
            return self._save_file()
        except Exception as e:
            print(f"Error deleting data: {e}")
            return False
    
    def search_data(self, filter_criteria: Dict) -> List[Dict]:
        """Return records matching all key/value pairs in filter_criteria."""
        try:
            result = self.data_frame.copy()

            for key, value in filter_criteria.items():
                if key in result.columns:
                    result = result[result[key] == value]

            return result.to_dict('records')
        except Exception as e:
            print(f"Error searching data: {e}")
            return []
    
    def clear_data(self) -> bool:
        """Clear all data from the CSV (resets to empty)."""
        try:
            self.data_frame = pd.DataFrame()
            return self._save_file()
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False
    
    def get_records_count(self) -> int:
        """Return number of records in the CSV."""
        return len(self.data_frame) if self.data_frame is not None else 0

    def get_columns(self) -> List[str]:
        """Return a list with the column names in the DataFrame."""
        return list(self.data_frame.columns) if self.data_frame is not None else []
