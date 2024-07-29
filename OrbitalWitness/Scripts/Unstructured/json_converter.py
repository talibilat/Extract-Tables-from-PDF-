import json

class JSONConverter:
    @staticmethod
    def convert_elements_to_json(elements):
        """
        Convert a list of elements to a JSON formatted string.
        Args:
            elements (list): List of elements, each having a to_dict() method to convert to a dictionary.
        Returns:
            str: JSON formatted string representation of the elements.
        """
        # Convert each element to a dictionary using its to_dict method
        element_dict = [el.to_dict() for el in elements]
        # Convert the list of dictionaries to a JSON string with pretty printing
        output = json.dumps(element_dict, indent=2)
        return output

# Explanation:
# 1. The convert_elements_to_json method converts a list of elements into a JSON formatted string.
#    This is useful for serializing elements into a standard format for storage, transmission, or further processing.
# 2. Each element in the list is assumed to have a to_dict() method, which converts the element to a dictionary.
#    This ensures that each element can be easily serialized into JSON format.
# 3. The list of dictionaries is then converted to a JSON string using json.dumps(), with an indent of 2 for pretty printing.
#    Pretty printing makes the JSON output more readable and easier to inspect.

