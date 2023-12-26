import datetime
import os
import pickle
import json
import re
import logging
from ast import literal_eval

import cn2an

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


def is_xxCH(v_string,query_conten):
    if v_string=="":
        return True
    p=r"[0-9a-zA-Z]+"
    m=re.findall(p, v_string)
    query = re.findall(p, query_conten)
    ch_num = re.findall(r'[0-9负一二三四五六七八九十百千万亿零]+', query_conten, re.DOTALL)
    if len(ch_num):
        for e in ch_num:
            if re.match(r"^[0-9]+$", e, re.DOTALL):
                pass
            else:
                try:
                    num = cn2an.cn2an(e, "smart")
                    query.append(str(int(num)))
                    query.append(str(float(num)))
                except:
                    pass
    for e in m:
        if e not in query :
            i_s = v_string.index(e)
            i_end = i_s + len(e)
            char = v_string[i_end:i_end + 1]
            if char in ["、", ".", "，", ":", "："]:
                continue
            else:
                return True
    return False


def is_xyzchar(v_string,query_content):
    if validate_date_string(v_string):
        return False

    if v_string=="":
        return True
    p=r"[0-9a-zA-Z]+\.?[0-9a-zA-Z]+"
    m=re.findall(p, v_string)
    query = re.findall(p, query_content)
    ch_num=re.findall(r'[0-9负一二三四五六七八九十百千万亿零]+', query_content, re.DOTALL)
    if len(ch_num):
        for e in ch_num:
            if re.match(r"^[0-9]+$",e, re.DOTALL):
                pass
            else:
                try:
                    num=cn2an.cn2an(e, "smart")
                    query.append(str(int(num)))
                    query.append(str(float(num)))
                except:
                    pass
    for e in m:
        if e not  in query  and e not in ["user", "assistant", "system","function"]:
            return True
    return False



import re

def is_true_number(text, query):
    pattern = r'\d+\.?\d*[千万亿]*'
    numbers = re.findall(pattern, text, re.DOTALL)
    query=re.findall(pattern, query, re.DOTALL)
    res = True
    if len(numbers) != 0:
        for number in numbers:
            if number not in query:
                try:
                    i_s=text.index(number)
                    i_end=i_s+len(number)
                    char=text[i_end:i_end+1]
                    if char in ["、",".","，",":","："]:
                        res = True
                    else:
                        res = False
                except:

                    res = False
    return res

if __name__=="__main__":
    # v_string=""
    vstring="""幸福西饼覆盖多少个城市,详情结果如下:3.{"商品名称":"四重奏","排名":"NO1"},4.{"商品名称":"甜心莓莓","排名":"NO2"}]"""
    query_conten="""[{"商品名称":"四重奏","排名":"NO1"},{"商品名称":"甜心莓莓","排名":"NO2"}]"""
    print(is_xxCH(vstring,query_conten))
    pass
