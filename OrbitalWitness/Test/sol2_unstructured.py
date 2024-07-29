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

def extract_elements_from_pdf(file_path: str) -> list:
    """
    Extract elements from a PDF file.
    
    Args:
    file_path (str): The path to the PDF file.
    
    Returns:
    list: A list of elements extracted from the PDF.
    """
    elements = partition_pdf(file_path,infer_table_structure=True)
    return elements

def convert_elements_to_json(elements: list) -> str:
    """
    Convert elements to JSON format.
    
    Args:
    elements (list): List of elements to be converted.
    
    Returns:
    str: JSON string of the elements.
    """
    element_dict = [el.to_dict() for el in elements]
    output = json.dumps(element_dict, indent=2)
    return output

def get_elements_using_client(client: UnstructuredClient, file_path: str) -> list:
    """
    Get elements from a PDF file using UnstructuredClient.
    
    Args:
    client (UnstructuredClient): An instance of UnstructuredClient.
    file_path (str): The path to the PDF file.
    
    Returns:
    list: A list of elements extracted using the client.
    """
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

def combine_table_html(elements: list) -> str:
    """
    Combine HTML content of all tables found in elements.
    
    Args:
    elements (list): List of elements containing table data.
    
    Returns:
    str: Combined HTML string of all tables.
    """
    tables = [el for el in elements if el.category == "Table"]
    combined_html = "<html><body>"
    
    for table in tables:
        combined_html += table.metadata.text_as_html
    
    combined_html += "</body></html>"
    return combined_html

def pretty_print_html(html_content: str) -> str:
    """
    Pretty print HTML content.
    
    Args:
    html_content (str): HTML content to be prettified.
    
    Returns:
    str: Prettified HTML content.
    """
    parser = etree.HTMLParser(remove_blank_text=True)
    file_obj = StringIO(html_content)
    tree = etree.parse(file_obj, parser)
    return etree.tostring(tree, pretty_print=True).decode()

def save_tables_as_csv(tables: list, output_file: str) -> None:
    """
    Save tables as CSV file.
    
    Args:
    tables (list): List of table elements.
    output_file (str): The path to the output CSV file.
    
    Returns:
    None
    """
    dfs = []
    
    for table in tables:
        df = pd.read_html(table.metadata.text_as_html)[0]
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv(output_file, index=False)

# Main execution
if __name__ == "__main__":
    # Extract and print JSON representation of elements from PDF
    elements = extract_elements_from_pdf(filename)
    json_output = convert_elements_to_json(elements)
    print(json_output)
    
    # Initialize UnstructuredClient and get elements using client
    client = UnstructuredClient(api_key_auth="YNGVoSDJkyu7P3D3sZXa3yku1jNFHI")
    elements = get_elements_using_client(client, filename)
    
    # Combine, pretty print, and display table HTML
    combined_html = combine_table_html(elements)
    pretty_html = pretty_print_html(combined_html)
    print(pretty_html)
    
    # Display HTML in Jupyter Notebook
    HTML(combined_html)
    
    # Save tables as CSV
    tables = [el for el in elements if el.category == "Table"]
    save_tables_as_csv(tables, "/Users/talib/Documents/Projects/OrbitalWitness/Output/output.csv")
