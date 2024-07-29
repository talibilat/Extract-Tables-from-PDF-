import json
import pandas as pd
from IPython.display import HTML
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import dict_to_elements
from lxml import etree
from io import StringIO

import warnings
warnings.filterwarnings('ignore')

# Specify the path to your PDF file
filename = "/Users/talib/Documents/Projects/OrbitalWitness/Data/Official_Copy_Register_EGL363613.pdf"

# Function to extract elements from PDF
def extract_elements_from_pdf(file_path):
    elements = partition_pdf(file_path)
    return elements

# Function to convert elements to JSON format
def convert_elements_to_json(elements):
    element_dict = [el.to_dict() for el in elements]
    output = json.dumps(element_dict, indent=2)
    return output

# Function to get elements using UnstructuredClient
def get_elements_using_client(client, file_path):
    with open(file_path, "rb") as f:
        files = shared.Files(content=f.read(), file_name=file_path)
    
    req = shared.PartitionParameters(
        files=files,
        strategy="hi_res",
        hi_res_model_name="yolox",
        skip_infer_table_types=[],
        pdf_infer_table_structure=True,
    )

    try:
        resp = client.general.partition(req)
        elements = dict_to_elements(resp.elements)
    except SDKError as e:
        print(e)
        elements = []
    
    return elements

# Function to combine table HTML from elements
def combine_table_html(elements):
    tables = [el for el in elements if el.category == "Table"]
    combined_html = "<html><body>"
    
    for table in tables:
        combined_html += table.metadata.text_as_html
    
    combined_html += "</body></html>"
    return combined_html

# Function to parse and pretty print HTML
def pretty_print_html(html_content):
    parser = etree.HTMLParser(remove_blank_text=True)
    file_obj = StringIO(html_content)
    tree = etree.parse(file_obj, parser)
    return etree.tostring(tree, pretty_print=True).decode()

# Function to save tables as CSV
def save_tables_as_csv(tables, output_file):
    dfs = []
    
    for table in tables:
        df = pd.read_html(table.metadata.text_as_html)[0]
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv(output_file, index=False)

# Main execution
if __name__ == "__main__":
    elements = extract_elements_from_pdf(filename)
    json_output = convert_elements_to_json(elements)
    print(json_output)
    
    client = UnstructuredClient(api_key_auth="API key")
    elements = get_elements_using_client(client, filename)
    
    combined_html = combine_table_html(elements)
    pretty_html = pretty_print_html(combined_html)
    print(pretty_html)
    
    HTML(combined_html)
    
    tables = [el for el in elements if el.category == "Table"]
    save_tables_as_csv(tables, "output.csv")


