import datetime
import os
import pickle
import json
import re
import logging
from ast import literal_eval
from api_protocol import InitInterfaceRequest

def load_interface_template(pathname="interface_template_dict.pkl")->InitInterfaceRequest:

    if os.path.exists(pathname):
        with open(pathname, 'rb') as f:
            data_dict = pickle.load(f)
            obj=InitInterfaceRequest(**data_dict)
            return obj
    else:
        return None

def save_interface_template(data:InitInterfaceRequest,pathname="interface_template_dict.pkl"):

    with open(pathname, 'wb') as f:
        pickle.dump(data.dict(), f)




def parse_json_markdown_for_list(json_string: str) :
    match = re.search( r"(\[(.*?)\])", json_string, re.DOTALL)
    if match is None:
        json_str = '[]'
    else:
        json_str = match.group(0)
    json_str = json_str.strip()
    try:
        try:
            return literal_eval(json_str)
        except:
            return json.loads(json_str)
    except :
        match = re.findall(r"(//(.*?))[\n]", json_str, re.DOTALL)
        for e in match:
            json_str = json_str.replace(e[0], "")
        match = re.search(r"(\[(.*?)\])", json_str, re.DOTALL)
        if match is None:
            json_str = '[]'
        else:
            json_str = match.group(0)

        json_str = json_str.strip()

        try:
            return literal_eval(json_str)
        except:
            return json.loads(json_str)
    return []


def parse_json_markdown(json_string: str) -> dict:
    try:
        return literal_eval(json_string)
    except:
        try:
            return json.loads(json_string)
        except:
            pass

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
    try:
        try:

            return literal_eval(json_str)
        except:
            return json.loads(json_str)
    except:
        match = re.findall(r"(//(.*?))[\n]", json_str, re.DOTALL)
        for e in match:
            json_str = json_str.replace(e[0], "")
    try:
        return literal_eval(json_str)
    except:
        return json.loads(json_str)





def get_current_weekday():
    current_date = datetime.datetime.now().date()
    current_weekday = current_date.weekday()  # Monday is 0 and Sunday is 6

    week_map={0:"周一",1:"周二",2:"周三",3:"周四",4:"周五",5:"周六",6:"周日"}

    return f"今日星期属于{week_map[current_weekday]}"