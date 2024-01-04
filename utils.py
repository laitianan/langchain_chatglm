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

def have_Ch(string):
    p=r".*[\u4e00-\u9fa5]+.*"
    match=re.match(p,string)
    if match:
        return True
    else:
        return False


if __name__=="__main__":
    # v_string=""
    # vstring="""幸福西饼覆盖多少个城市,详情结果如下:3.{"商品名称":"四重奏","排名":"NO1"},4.{"商品名称":"甜心莓莓","排名":"NO2"}]"""
    # query_conten="""[{"商品名称":"四重奏","排名":"NO1"},{"商品名称":"甜心莓莓","排名":"NO2"}]"""
    # print(is_xxCH(vstring,query_conten))
    # pass
    resp="您好，感谢您选择幸福西饼。根据我们已知的信息，我们无法查询到广州市具体的直营店数量。建议您可以通过幸福西饼官方网站或者拨打客服电话进行查询。如有其他问题，欢迎随时咨询。"
    history="""system:
幸福西饼业务主要分布在全国各个城市,
当前系统背景：
当前时间2024-01-04 16:34:28,今日星期属于周四,
幸福西饼已知信息：
信息1:门店按天查询业绩,查询结果详情:请用户提供：店铺名称 才可查询
信息2:未查到信息，请尝试咨询其他业务,
请结合当前系统背景、幸福西饼已知信息选择符合用户需求信息组织语言回复用户问题,如果符合的信息需要用户提供参数，请一定要回复让用户提供，
未能解答回复或跟幸福西饼无关问题请直接回复:未能理解你的问题，请尝试咨询其他业务,
未能解答案列举例：
用户问题：查询习近平是出生日期是多少和广东省的最高GDP是多少
你的回复：未查到信息，请尝试咨询其他业务（跟幸福西饼无关问题无法解答）

用户问题：幸福西饼创始人是谁
你的回复：未查到信息，请尝试咨询其他业务（已知信息无法解答）

用户问题：苹果手机每年的销量多少
你的回复：未查到信息，请尝试咨询其他业务（跟幸福西饼无关问题无法解答）

用户问题：核销苹果账单
你的回复：未查到信息，请尝试咨询其他业务（跟幸福西饼无关问题无法解答）

你的回复:

user:XS454545454
assistant:您好，感谢您选择幸福西饼。根据您提供的订单号XS454545454，我们查询到该订单目前暂无数据"""
    if "？" not in resp and "?" not in resp and is_true_number(resp, history) and not is_xxCH(resp,
                                                                                          history) and "你的回复" not in resp and "系统背景" not in resp and "用户问题" not in resp:

        print(have_Ch("122323"))
