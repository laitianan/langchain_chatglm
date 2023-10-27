import os
import pickle
import json
import re

def load_interface_template(path):
    path=os.path.join(path,"interface_template.pkl")
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data = pickle.load(f)
            return data
    else:
        return None

def save_interface_template(data,path):
    path=os.path.join(path,"interface_template.pkl")
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def parse_json_markdown(json_string: str) -> dict:
    """
    Parse a JSON string from a Markdown string.

    Args:
        json_string: The Markdown string.

    Returns:
        The parsed JSON object as a Python dictionary.
    """
    # Try to find JSON string within triple backticks
    match = re.search(r"```(json)?(.*)```", json_string, re.DOTALL)

    # If no match found, assume the entire string is a JSON string
    if match is None:
        json_str = json_string
    else:
        # If match found, use the content within the backticks
        json_str = match.group(2)

    # Strip whitespace and newlines from the start and end
    json_str = json_str.strip()

    # Parse the JSON string into a Python dictionary
    parsed = json.loads(json_str)

    return parsed

