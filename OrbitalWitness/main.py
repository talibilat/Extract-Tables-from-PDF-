import time
from Scripts.Regex.pdf_processor import processing_pdf
from Scripts.Regex.text_processor import processing_test
from Scripts.Regex.dataframe_processor import processing_df
import warnings

from Scripts.Unstructured.pdf_processor import PDFProcessor
from Scripts.Unstructured.json_converter import JSONConverter
from Scripts.Unstructured.unstructured_client_processor import UnstructuredClientProcessor
from Scripts.Unstructured.html_processor import HTMLProcessor
from Scripts.Unstructured.csv_saver import CSVSaver

from Scripts.Tabula.dataframe_processer import processing_df_tabula
from Scripts.Tabula.pdf_processer import pdf_analyzer
import tabula as tb


warnings.filterwarnings('ignore')

def main():

    """ 
    ________________________________________________________________________________________________________________________________________________


                                                                        METHOD 1
    ________________________________________________________________________________________________________________________________________________

    """

    regex_time_start = time.process_time()
    pdf_path = "Data/Official_Copy_Register_EGL363613.pdf"
    output_path = 'Output/preprocessed_text_file.txt'

    # Process the PDF file
    pdf_processor = processing_pdf(pdf_path)
    data = pdf_processor.read_and_process_pdf()


    # Process the extracted text
    text_processor = processing_test(data)
    data_list = text_processor.text_to_list_of_strings()
    fixed_data = text_processor.fix_note_column(data_list)
    text_data = text_processor.converting_to_text(fixed_data)
    text_processor.save_file(text_data, output_path)

    # Convert to DataFrame and process it
    df_processor = processing_df(output_path)
    non_nan_indices = df_processor.get_non_nan_indices('Title')
    merged_df = df_processor.merge_rows(non_nan_indices)

    # Optionally, save the merged DataFrame to a new file or print it
    merged_df.to_csv('Output/output_with_regex.csv', index=False)
    regex_time_stop = time.process_time()
    regex_time_taken = regex_time_stop - regex_time_start
    print(f"Regex Start Time: {regex_time_start}")
    print(f"Regex End Time: {regex_time_stop}")
    print(f"Regex Total Time: {regex_time_taken} seconds")



    """ 
    ________________________________________________________________________________________________________________________________________________


                                                                        METHOD 2
    ________________________________________________________________________________________________________________________________________________

    """
    unsrtuctured_api_key = "YOUR API KEY"
    un_time_start = time.process_time()

    filename = "Data/Official_Copy_Register_EGL363613.pdf"
    
    # Extract elements from PDF
    pdf_processor = PDFProcessor(filename)
    elements = pdf_processor.extract_elements()
    
    # Convert elements to JSON and print
    json_output = JSONConverter.convert_elements_to_json(elements)
    print(json_output)
    
    # Use UnstructuredClient to get elements
    client_processor = UnstructuredClientProcessor(api_key=unsrtuctured_api_key)
    elements = client_processor.get_elements(filename)
    
    # Combine table HTML and pretty print it
    combined_html = HTMLProcessor.combine_table_html(elements)
    pretty_html = HTMLProcessor.pretty_print_html(combined_html)
    print(pretty_html)
    
    # Display HTML content (if using Jupyter or similar environment)
    from IPython.display import HTML
    HTML(combined_html)
    
    # Save tables as CSV
    tables = [el for el in elements if el.category == "Table"]
    CSVSaver.save_tables_as_csv(tables, "Output/output_with_unstructured.csv")

    un_time_stop = time.process_time()
    un_time_taken = un_time_stop - un_time_start
    print(f"Unstructured Start Time: {un_time_start}")
    print(f"Unstructured End Time: {un_time_stop}")
    print(f"Unstructured Total Time: {un_time_taken} seconds")



    """ 
    ________________________________________________________________________________________________________________________________________________


                                                                        METHOD 3
    ________________________________________________________________________________________________________________________________________________

    """
    tabula_time_start = time.process_time()
    file = 'Data/Official_Copy_Register_EGL363613.pdf'
    
    # Create instances of the processor classes
    pdf_processor = pdf_analyzer(file)
    dataframe_processor = processing_df_tabula()

    # Count the number of pages in the PDF
    pages = pdf_processor.count_pdf_pages()

    # Loop over each page and process it
    for pageiter in range(pages):
        df_page = tb.read_pdf(file, pages=pageiter+1, area=[120, 0, 820, 900], columns=[80, 180, 350, 450, 520], pandas_options={'header': None}, stream=True)
        dataframe_processor.combine_dataframes(df_page)

    # Clean the combined dataframe
    df = dataframe_processor.clean_dataframe()

    # Remove rows after pattern
    result_df, df_noterows = dataframe_processor.remove_rows_after_pattern(df, 1, 'NOTE')

    # Process the notes
    notes = dataframe_processor.process_notes(df_noterows)

    # Format the schedule
    schedule_formatted = dataframe_processor.format_schedule(result_df, notes)

    # Save the merged DataFrame to a new file or print it
    schedule_formatted.to_csv('Output/output_with_tabula.csv', index=False)
    tabula_time_stop = time.process_time()
    tabula_time_taken = tabula_time_stop - tabula_time_start
    print(f"Tabula Start Time: {tabula_time_start}")
    print(f"Tabula End Time: {tabula_time_stop}")
    print(f"Tabula Total Time: {tabula_time_taken} seconds")

    


if __name__ == "__main__":
    main()





