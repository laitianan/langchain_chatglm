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
        match = re.findall(r"{.*?}", json_string, re.DOTALL)
        if len(match)==0:
            json_str = json_string
        else:
            json_str = match[0]
    else:
        json_str = match.group(2)
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


def validate_date_string(date_string):
    pattern = r'^\d{4}[-/年]\d{2}[-/月]\d{2}'  # 匹配YYYY-MM-DD格式的日期字符串
    if re.match(pattern, date_string):
        return True
    else:
        return False


def get_num(string):
    pattern = r'^\d{5,}'
    m = re.findall(pattern, string, re.DOTALL)
    if len(m):
        return m[0]
    else:
        return ""

def is_xxCH(v_string,query):
    if v_string=="":
        return True
    m=re.findall(r"[a-zA-Z]{2,}", v_string)
    if len(m) and m[0] not in query:
        return True
    else:
        return False


def is_true_number(text, query):
    pattern = r'\d+\.?\d*[千万亿]*'
    numbers = re.findall(pattern, text, re.DOTALL)

    res = True
    if len(numbers) != 0:
        for number in numbers:
            if number not in query:
                try:
                    number = float(number)
                    if number <= 30.:
                        res = True
                    else:
                        res = False
                except:

                    res = False
    return res