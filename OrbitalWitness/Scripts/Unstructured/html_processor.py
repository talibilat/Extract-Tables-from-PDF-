from lxml import etree
from io import StringIO

class HTMLProcessor:
    @staticmethod
    def combine_table_html(elements):
        """
        Combine HTML tables from a list of elements into a single HTML document.
        Args:
            elements (list): List of elements, each with a category and metadata containing HTML text.
        Returns:
            str: Combined HTML content of all tables.
        """
        # Filter elements to get only those categorized as "Table"
        tables = [el for el in elements if el.category == "Table"]
        combined_html = "<html><body>"
        
        # Append the HTML text of each table to the combined HTML
        for table in tables:
            combined_html += table.metadata.text_as_html
        
        combined_html += "</body></html>"
        return combined_html

    @staticmethod
    def pretty_print_html(html_content):
        """
        Pretty print the given HTML content.
        Args:
            html_content (str): Raw HTML content to be pretty printed.
        Returns:
            str: Pretty printed HTML content.
        """
        # Parse the HTML content, removing blank text nodes
        parser = etree.HTMLParser(remove_blank_text=True)
        file_obj = StringIO(html_content)
        tree = etree.parse(file_obj, parser)
        # Convert the parsed tree back to a string with pretty printing
        return etree.tostring(tree, pretty_print=True).decode()

# Explanation:
# 1. The combine_table_html method combines HTML tables from a list of elements into a single HTML document.
#    This is useful for aggregating multiple tables into one document for further processing or display.
# 2. The method filters the elements list to include only those with the category "Table".
#    This ensures that only table elements are processed.
# 3. Each table's HTML content is appended to a combined HTML string, which is then returned.
#    This approach is straightforward and ensures that all table content is included in the final HTML.
# 4. The pretty_print_html method takes raw HTML content and returns a pretty printed version.
#    Pretty printing makes the HTML more readable and easier to inspect, which is useful for debugging and presentation.
# 5. The method uses lxml's HTMLParser to parse the HTML content, removing blank text nodes for cleaner output.
#    It then converts the parsed tree back to a string with pretty printing enabled.
