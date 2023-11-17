import os
import pickle
import json
import re
import logging
from ast import literal_eval
from api_protocol import InitInterfaceRequest
def load_interface_template(path,name="interface_template_dict.pkl")->InitInterfaceRequest:
    path=os.path.join(path,name)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data_dict = pickle.load(f)
            obj=InitInterfaceRequest(**data_dict)
            return obj
    else:
        return None

def save_interface_template(data:InitInterfaceRequest,path,name="interface_template_dict.pkl"):
    path=os.path.join(path,name)
    with open(path, 'wb') as f:
        pickle.dump(data.dict(), f)




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

