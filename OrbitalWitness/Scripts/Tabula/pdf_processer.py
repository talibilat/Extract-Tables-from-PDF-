import re

class pdf_analyzer:
    def __init__(self, file):
        self.file = file

    def count_pdf_pages(self):
        rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE | re.DOTALL)
        with open(self.file, "rb") as temp_file:
            return len(rxcountpages.findall(temp_file.read().decode('latin-1')))