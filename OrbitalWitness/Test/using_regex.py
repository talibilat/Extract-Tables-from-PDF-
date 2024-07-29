import fitz  # PyMuPDF
import re
import pandas as pd

def read_and_process_pdf(filepath):
    data = 'DATE            Address                       Leese\'s Date    Title                Note'
    document = fitz.open(pdf_path)
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text()
        if re.search('\ntitle', text):
            data += text[(text.find("title")):(text.find("Title"))]
            data = data.replace("title","")
            data = data.replace("\n\n","\n")
    return data

def text_to_list_of_strings(data):
    # Split the entries by the pattern \n\d+\n
    entries = re.split(r'\n\d+\n', data.strip())

    # Further split each entry by newline
    processed_entries = [entry.split('\n') for entry in entries]

    return processed_entries


def fix_note_column(data):
    for entry_number, entry in enumerate(data):
        for index, line in enumerate(entry):
            if "NOTE" in line:
                if (len(entry)-1) == index:
                    data[entry_number][0] = data[entry_number][0] + "       " + data[entry_number][index]
                    data[entry_number].pop(index)
                else:
                    data[entry_number][index] += data[entry_number][index] + " " + data[entry_number][index + 1]
                    data[entry_number][0] = data[entry_number][0] + "       " + data[entry_number][index]
                    for i in range(len(entry) - index - 1):
                        data[entry_number].pop(index)
    return data

def converting_to_text(data):
        data = str(data)
        data =  data.replace(" ['", "\n")
        data =  data.replace("', '", "\n")
        data =  data.replace("[[\"", "")
        data =  data.replace("\"],", "")
        data =  data.replace("'],", "")
        return data


def saving_file(data, filename):
    with open(filename, "w") as output:
        output.write(data)

def convert_to_df(path):
    return pd.read_fwf(path, delimiter=' ')


# Function to get indices where values are not np.nan
def get_non_nan_indices(df, column_name):
    return df.index[df[column_name].notna()].tolist()

# Function to merge rows based on the provided list
def merge_rows(df, merge_indices):
    merged_rows = []
    
    for i in range(len(merge_indices) - 1):
        start_idx = merge_indices[i]
        end_idx = merge_indices[i + 1]
        
        # Select rows between start_idx and end_idx
        temp_df = df.loc[start_idx:end_idx-1]
        
        # Merge rows by dropping NaN and combining remaining values
        merged_row = temp_df.apply(lambda x: ' '.join(x.dropna().astype(str)), axis=0)
        
        # Append the merged row to the list
        merged_rows.append(merged_row)
    
    # Create a new DataFrame from the merged rows
    merged_df = pd.DataFrame(merged_rows)
    return merged_df


pdf_path = "/Users/talib/Documents/Projects/OrbitalWitness/Data/Official_Copy_Register_EGL363613.pdf"
output = '/Users/talib/Documents/Projects/OrbitalWitness/Output/preprocessed_text_file.txt'

data = read_and_process_pdf(pdf_path)
data = text_to_list_of_strings(data)
data = fix_note_column(data)
data = converting_to_text(data)
saving_file(data,output)
df = convert_to_df(output)
non_nan_indices = get_non_nan_indices(df, 'Title')
merged_df = merge_rows(df, non_nan_indices)