import pandas as pd

class CSVSaver:
    @staticmethod
    def save_tables_as_csv(tables, output_file):
        """
        Save multiple tables as a single CSV file.
        Args:
            tables (list): List of table objects, each containing HTML text.
            output_file (str): Name of the output CSV file.
        """
        dfs = []
        
        # Iterate over each table in the list of tables
        for table in tables:
            # Parse the HTML text of the table into a DataFrame
            df = pd.read_html(table.metadata.text_as_html)[0]
            dfs.append(df)
        
        # Concatenate all DataFrames into a single DataFrame
        combined_df = pd.concat(dfs, ignore_index=True)
        # Save the combined DataFrame to a CSV file
        combined_df.to_csv(output_file, index=False)

# Explanation:
# 1. The save_tables_as_csv method is a static method because it does not rely on any instance-specific data. 
#    It is designed to be called directly on the class without requiring an instance.
