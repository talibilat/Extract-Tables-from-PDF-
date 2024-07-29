import pandas as pd
import numpy as np
import re

class processing_df_tabula:
    def __init__(self):
        """
        Initialize the DataFrameProcessor with an empty DataFrame to combine data.
        """
        self.df_combine = pd.DataFrame([])

    def combine_dataframes(self, df_page):
        """
        Append a new DataFrame to the combined DataFrame.
        Args:
            df_page (pd.DataFrame): DataFrame to be combined.
        """
        if len(df_page) > 0:
            self.df_combine = self.df_combine._append(df_page)

    def clean_dataframe(self):
        """
        Clean and preprocess the combined DataFrame.
        Returns:
            pd.DataFrame: Cleaned DataFrame.
        """
        datas = np.array(self.df_combine, dtype='object')
        df = pd.DataFrame(datas)
        # Remove rows until 'and plan ref.' is found
        df = df.iloc[(df.loc[df[1] == 'and plan ref.'].index[0] + 1):, :]
        # Mark rows with numerical values in the first column
        df['border'] = df.apply(lambda x: 1 if re.findall('^[+-]?(\d*\.)?\d+$', str(x[0])) else 0, axis=1)
        # Create cumulative sum to group rows
        df['row'] = df['border'].transform('cumsum')
        # Identify rows containing 'NOTE'
        df['NoteRow'] = np.where(df[1].str.contains('NOTE'), df['row'], 0)
        # Drop unnecessary columns
        df = df.drop(['border', 5], axis=1)
        # Replace NaN values with empty strings
        df = df.replace(np.NaN, '')
        return df

    def remove_rows_after_pattern(self, df, pattern_column, pattern):
        """
        Remove rows after the first occurrence of a pattern in a specified column.
        Args:
            df (pd.DataFrame): DataFrame to process.
            pattern_column (str): Column to search for the pattern.
            pattern (str): Pattern to search for.
        Returns:
            tuple: Filtered DataFrame and DataFrame with 'NOTE' rows.
        """
        keep_mask = [True] * len(df)
        keep_mask_inverse = [False] * len(df)
        first_occurrence = {}

        for idx, (row_num, value) in enumerate(zip(df['row'], df[pattern_column])):
            if row_num in first_occurrence:
                keep_mask[idx] = False
                keep_mask_inverse[idx] = True
            elif 'NOTE' in value:
                first_occurrence[row_num] = idx
                keep_mask[idx] = False
                keep_mask_inverse[idx] = True

        df_filtered = df[keep_mask]
        df_noterows = df[keep_mask_inverse]
        return df_filtered, df_noterows

    def concat_selected_columns(self, group):
        """
        Concatenate selected columns in a group to form a string.
        Args:
            group (pd.DataFrame): Group of rows.
        Returns:
            str: Concatenated string.
        """
        concatenated_string = ' '.join(group.astype(str).values.flatten())
        match = re.search(r'\bNOTE\b', concatenated_string)
        if match:
            return concatenated_string[match.start():].strip()
        return ''

    def process_notes(self, df_noterows):
        """
        Process 'NOTE' rows and concatenate their values.
        Args:
            df_noterows (pd.DataFrame): DataFrame with 'NOTE' rows.
        Returns:
            pd.DataFrame: DataFrame with concatenated 'NOTE' values.
        """
        notes = df_noterows.groupby('row').apply(lambda group: self.concat_selected_columns(group)).reset_index().astype(str)
        notes.columns = ['NoteRow', 'ConcatenatedValues']
        return notes

    def format_schedule(self, result_df, notes):
        """
        Format the final schedule by merging data with notes and organizing columns.
        Args:
            result_df (pd.DataFrame): DataFrame with main data.
            notes (pd.DataFrame): DataFrame with concatenated notes.
        Returns:
            pd.DataFrame: Formatted schedule DataFrame.
        """
        result_df = result_df.replace(r"^ +| +$", r"", regex=True)
        result_df[0] = pd.to_numeric(result_df[0], errors='coerce').astype('Int64')
        notes['NoteRow'] = pd.to_numeric(notes['NoteRow'], errors='coerce').astype('Int64')

        merged_df = pd.merge(left=result_df[[0, 1, 2, 3, 4, 'row', 'NoteRow']], right=notes[['NoteRow', 'ConcatenatedValues']], how='left', left_on=0, right_on='NoteRow')

        schedule = merged_df[[0, 1, 2, 3, 4, 'ConcatenatedValues', 'row']]
        schedule = schedule[schedule[1].notnull()]
        schedule['index'] = schedule.groupby('row').cumcount() + 1
        schedule = schedule[schedule['row'] != 0]
        schedule['ConcatenatedValues'] = schedule['ConcatenatedValues'].replace(np.NaN, '')

        schedule = schedule.pivot_table(index=['row'], columns=['index'], values=[1, 2, 3, 4, 'ConcatenatedValues'], aggfunc=lambda x: ' '.join(x)).reset_index()
        schedule = schedule.replace(np.NaN, '')

        schedule_formatted = pd.DataFrame()
        schedule_formatted['Registration date and plan ref.'] = schedule.iloc[0:, 1:8].apply(lambda x: ''.join(map(str, x)), axis=1)
        schedule_formatted['Property description'] = schedule.iloc[0:, 9:16].apply(lambda x: ''.join(map(str, x)), axis=1)
        schedule_formatted['Date of lease and term.'] = schedule.iloc[0:, 17:24].apply(lambda x: ''.join(map(str, x)), axis=1)
        schedule_formatted['Lessee\'s title.'] = schedule.iloc[0:, 25:32].apply(lambda x: ''.join(map(str, x)), axis=1)
        schedule_formatted['Notes.'] = schedule.iloc[0:, 33:40].apply(lambda x: ''.join(map(str, x)), axis=1)

        return schedule_formatted

# Explanation:
# 1. combine_dataframes Method: This method appends a new DataFrame to an existing combined DataFrame. The _append method is used to ensure data is appended correctly.
# 2. clean_dataframe Method: This method cleans the combined DataFrame by:
#    - Converting it to a numpy array for consistency.
#    - Removing rows up to and including the row containing 'and plan ref.'.
#    - Marking rows with numerical values in the first column.
#    - Creating a cumulative sum to group rows.
#    - Identifying rows containing 'NOTE'.
# 3. remove_rows_after_pattern Method: This method removes rows after the first occurrence of a pattern in a specified column. It keeps track of rows to keep and not keep using masks.
# 4. concat_selected_columns Method: This method concatenates selected columns in a group to form a string. It looks for the occurrence of 'NOTE' and returns the substring from 'NOTE' onwards.
# 5. process_notes Method: This method processes 'NOTE' rows and concatenates their values. It groups the rows by 'row' and applies the concatenation function.
# 6. format_schedule Method: This method formats the final schedule by:
#    - Merging the main data with the notes.
#    - Organizing columns.
#    - Pivoting the table to arrange data in a structured format.
#    - Cleaning up and concatenating columns to create a final formatted schedule.
