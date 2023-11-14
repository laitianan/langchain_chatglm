import os
import pickle
import json
import re
import logging
from ast import literal_eval
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




def parse_json_markdown_for_list(json_string: str) -> list:
    match = re.search( r"(\[(.*?)\])", json_string, re.DOTALL)
    if match is None:
        json_str = '[]'
    else:
        json_str = match.group(0)
    json_str = json_str.strip()
    try:
        return literal_eval(json_str)
    except :
        return []


def parse_json_markdown(json_string: str) -> dict:
    match = re.search(r"```(json)?(.*)```", json_string, re.DOTALL)
    if match is None:
        match = re.search(r"{.*}", json_string, re.DOTALL)
        if match is None:
            json_str = json_string
        else:
            json_str = match.group(0)
            # print("8"*20,json_str)
    else:
        json_str = match.group(2)
        # print("9" * 20,json_str)

    json_str = json_str.strip()

    return literal_eval(json_str)

