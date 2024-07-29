import pandas as pd

class processing_df:
    def __init__(self, filepath):
        """
        Initialize the DataFrameProcessor with the file path and load the data into a DataFrame.
        Args:
            filepath (str): Path to the file to be processed.
        """
        self.filepath = filepath
        # Read fixed-width formatted file into a DataFrame
        self.df = pd.read_fwf(filepath, delimiter=' ')

    def get_non_nan_indices(self, column_name):
        """
        Get the indices of rows where the specified column is not NaN.
        Args:
            column_name (str): The name of the column to check for NaN values.
        Returns:
            list: List of indices where the column is not NaN.
        """
        # Return list of indices where column values are not NaN
        return self.df.index[self.df[column_name].notna()].tolist()

    def merge_rows(self, merge_indices):
        """
        Merge rows of the DataFrame based on the provided indices.
        Args:
            merge_indices (list): List of indices indicating where to start and end merges.
        Returns:
            pd.DataFrame: DataFrame with merged rows.
        """
        merged_rows = []
        # Iterate through the indices to merge rows
        for i in range(len(merge_indices) - 1):
            start_idx = merge_indices[i]
            end_idx = merge_indices[i + 1]
            # Select rows between the start and end indices
            temp_df = self.df.loc[start_idx:end_idx - 1]
            # Merge rows by joining non-NaN values into a single string
            merged_row = temp_df.apply(lambda x: ' '.join(x.dropna().astype(str)), axis=0)
            merged_rows.append(merged_row)
        # Create a new DataFrame from the merged rows
        merged_df = pd.DataFrame(merged_rows)
        return merged_df

# Explanation:
# 1. The __init__ method initializes the class with the file path and reads the data into a DataFrame. 
#    Using pd.read_fwf() allows us to handle fixed-width formatted files, which is common in structured text data.
# 2. The get_non_nan_indices method finds indices of rows where a specified column is not NaN.
#    This is useful for identifying rows that contain meaningful data.
# 3. The merge_rows method merges rows based on provided indices.
#    The merging is done by concatenating non-NaN values from specified rows into a single string.
#    This approach is chosen to handle cases where data is split across multiple rows and needs to be combined.
