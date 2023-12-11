# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:43:15 2023

@author: admin
"""

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import random
import datetime

import requests
import threading
import time
import json
from utils import parse_json_markdown,parse_json_markdown_for_list
text="""
现在有一些意图，类别为：['站点当天实时业绩查询', '门店当天实时业绩查询', '订单号查询', '查某一天下单总量', '站点按天查询业绩', '门店按天查询业绩', '意图不明']，
你扮演AI角色的任务是根据***分隔符的文本对话，并根据user聊天记录上下文理解识别user一个或多个意图,当意图模糊可列出所有相关的模糊意图,
输出应该是严格按以下模式格式化的标记代码片段，必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":

{
"intention_name": list // 意图类别，意图类别必须在提供的类别中
}
备注意图详情描述：
1、站点当天实时业绩查询:站点当天实时业绩查询
2、门店当天实时业绩查询:门店当天实时业绩查询
3、订单号查询:通过订单号查询订单详情
4、查某一天下单总量:查询具体日期的下单总量
5、站点按天查询业绩:站点按天查询业绩
6、门店按天查询业绩:门店按天查询业绩
7、意图不明:用户随便询问的内容,当其他意图不匹配时请选择该意图

历史对话沟通记录：
***
user:查询今天下午六点366大街的业绩
***
你的回答:
"""
text2="""
你的任务是根据***分隔符的历史对话沟通记录，从user和assistant聊天记录理解user需求，并从聊天记录抽取正确的结构值以结构化数据格式返回，取不到的值使用None代替,
部分时间直接从user聊天抽取不出来才结合系统当前时间推理,系统当前时间2023-11-28 16:48:34,比如则根据系统当前时间推理:今天的开始日期时间为2023-11-28 00:00:00,今天的结束日期时间为2023-11-28 23:59:59,严格禁止生成聊天记录不存在的数据,
输出应该是严格按以下模式格式化的标记代码片段，必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":

```json
{
	"orderNo": STRING  // 订单号，抽取不到时使用"None"代替
    "day": STRING  // 日期(yyyy-MM-dd)，抽取不到时使用"None"代替
    "shop_name": STRING  // 店铺名称，抽取不到时使用"None"代替
}

历史对话沟通记录：
***
user:我想366大街昨天的订单为xs4569的详情
***
你的回答:
"""

text3="""
给你api文档说明以及聊天记录:
api名称类别如下['站点当天实时业绩查询', '门店当天实时业绩查询', '订单号查询', '站点按天查询业绩', '门店按天查询业绩', '今昨日下单对比', '新零售每天完成订单', '城市数', '近十天每日销售', '意图不明'],
api描述如下：
1、站点当天实时业绩查询:站点当天实时业绩查询
2、门店当天实时业绩查询:门店当天实时业绩查询
3、订单号查询:通过订单号查询订单详情
4、站点按天查询业绩:站点按天查询业绩
5、门店按天查询业绩:门店按天查询业绩
6、今昨日下单对比:今天的订单量和昨天的订单量比较
7、新零售每天完成订单:新零售门店每天完成的订单量汇总
8、城市数:幸福西饼覆盖多少个城市
9、近十天每日销售:最近十天每天的销售额
10、意图不明:用户随便询问的内容,当其他意图不匹配时请选择该意图
聊天记录：
user:业绩

请你结合api说明和聊天记录,完成与聊天相关意图的api接口调用类别的选择,可通过意图或关键词匹配
,严格禁止生成不存在的api名称,最终结果使用列表返回,比如["a","b"],
你的回答:

"""

import numpy as np
#查询今天下午六点366大街的业绩
class Presstest(object):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    def __init__(self,model,base_url):

        self.model=model
        self.base_url=base_url

    ##函数参数解析
    def testinterface(self):
        '''压测接口'''
        '''压测接口'''
        global ERROR_NUM
        try:
            print('开始调接口：', datetime.datetime.now().strftime('%Y-%m-%d- %H:%M:%S:%f'))
            user_inpt="abc店铺今天的下单量"
            
            
            post_json=json.dumps({"funtion_id":"2118","message":[{"role": "user", "content": user_inpt}]})
            r1 = requests.post(f"http://{self.base_url}/chat_funtion_intention/completions", data=post_json)
            try:
                content = json.loads(r1.content.decode("utf8"))
                print(content)
                return content
            except :
                # print(r1.content.decode("utf8"))
                res=r1.content.decode("utf8")
                print(f"错误解析：{res}")

        except Exception as e:
            print(e)
            ERROR_NUM += 1
        
        ###意图识别
    def testinterface2(self):
        
        '''压测接口'''
        global ERROR_NUM
        try:
            print('开始调接口：', datetime.datetime.now().strftime('%Y-%m-%d- %H:%M:%S:%f'))
            post_json =json.dumps({"message" :[{"role": "user", "content": "用户推荐商品"}]})
            r1 = requests.post(f"http://{self.base_url}/chat_intention_search/completions", data=post_json)

            try:
                content = json.loads(r1.content.decode("utf8"))

                print(content)
                return content
            except :
                print(r1.content.decode("utf8"))

        except Exception as e:
            print(e)
            ERROR_NUM += 1


    def testinterface3(self):
        '''压测接口'''
        global ERROR_NUM
        try:
            print('开始调接口：', datetime.datetime.now().strftime('%Y-%m-%d- %H:%M:%S:%f'))
            history = []
            messages="""
给你下面的系统背景、api参数文档说明以及聊天记录:
当前系统背景：
当前时间2023-12-08 17:48:16,今日星期属于周五,今天的开始日期时间为2023-12-08 00:00:00,今天的结束日期时间为2023-12-08 23:59:59,今天的日期为2023-12-08，
昨天的开始日期时间为2023-12-07 00:00:00,昨天的结束日期时间为2023-12-07 23:59:59,昨天的日期为2023-12-07,
前天的开始日期时间为2023-12-06 00:00:00,前天的结束日期时间为2023-12-06 23:59:59,前天的日期为2023-12-06,
api参数说明：
day |STRING | 日期(yyyy-MM-dd),抽取不到时使用null代替,默认值为null,严格禁止捏造user问题无关参数值
businessTypeNames |STRING | 业务类型[新零售业务,商场业务],抽取不到时使用null代替,默认值为null,严格禁止捏造user问题无关参数值
聊天记录：
user:昨天下单总量

请你结合当前系统背景、参数说明和聊天记录,完成user表达的api参数值的提取,其中时间相关字段根据系统背景推理，而其他字段不能根据时间推理比如订单号,严格禁止捏造user聊天未提到参数值,最终结果使用json格式返回参数说明的所需字段名称跟值,比如{"a":"a","b":"b"},未知参数请返回null,且不能构建新的字段名称,
你的回答:

            """
            # messages=text3
            if isinstance(messages,str):
                history.append({"role": "user", "content": messages})
            else:
                for mess in messages:
                    history.append({"role": mess.role, "content": mess.content})
            api_base = "http://192.168.0.11:8081/v1"
            llm_model="Qwen-7B-Chat"
            # llm_model="internlm-chat"
            data=json.dumps({
                "model": llm_model,
                "messages": history,
                "stream": False,


              })
            r1 = requests.post(f"{api_base}/chat/completions", headers={'Content-Type': 'application/json'},data=data)
            # print(r1.content)
            res = json.loads(r1.content.decode("utf8"))
            content=res["choices"][0]["message"]["content"]
            # print(f"------------------------------------")
            
            print("解析后参数",parse_json_markdown(content))
            return r1
            

        except Exception as e:
            print(e)
            ERROR_NUM += 1


    def testonework(self):
        '''一次并发处理单个任务'''
        i = 0
        while i < ONE_WORKER_NUM:
            i += 1
            self.testinterface()
        time.sleep(LOOP_SLEEP)

    def run(self):
        '''使用多线程进程并发测试'''
        t1 = time.time()
        Threads = []

        for i in range(THREAD_NUM):
            t = threading.Thread(target=self.testonework, name="T" + str(i))
            t.setDaemon(True)
            Threads.append(t)

        for t in Threads:
            t.start()
        for t in Threads:
            t.join()
        t2 = time.time()

        print("===============压测结果===================")

        print("任务用户数:", THREAD_NUM, "；每个用户请求数目：", ONE_WORKER_NUM, "总请求数目：", THREAD_NUM * ONE_WORKER_NUM)
        print("总耗时(秒):", t2 - t1)
        print("每次请求耗时(秒):", (t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM))
        print("每秒承载请求数:", 1 / ((t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM)))
        print("错误数量:", ERROR_NUM)


"""

8000
===============压测结果===================
任务数量: 10 * 10 = 100
总耗时(秒): 229.98357558250427
每次请求耗时(秒): 2.299835755825043
每秒承载请求数: 0.43481365896116353
错误数量: 0

===============压测结果===================
任务数量: 1 * 100 = 100
总耗时(秒): 130.3460624217987
每次请求耗时(秒): 1.3034606242179871
每秒承载请求数: 0.7671884991538975
错误数量: 0

任务数量: 3 * 10 = 30
总耗时(秒): 49.80372714996338
每次请求耗时(秒): 1.6601242383321126
每秒承载请求数: 0.602364556163987
错误数量: 0

===============压测结果===================
任务数量: 1 * 10 = 10
总耗时(秒): 12.27692437171936
每次请求耗时(秒): 1.227692437171936
每秒承载请求数: 0.8145362549463615
错误数量: 0

===============压测结果===================
任务数量: 2 * 5 = 10
总耗时(秒): 13.927287578582764
每次请求耗时(秒): 1.3927287578582763
每秒承载请求数: 0.7180149001430756
错误数量: 0


8081：


===============压测结果===================
任务数量: 2 * 5 = 10
总耗时(秒): 11.0851411819458
每次请求耗时(秒): 1.1085141181945801
每秒承载请求数: 0.9021084924283008
错误数量: 0

===============压测结果===================
任务数量: 1 * 10 = 10
总耗时(秒): 9.978099346160889
每次请求耗时(秒): 0.9978099346160889
每秒承载请求数: 1.0021948722977525
错误数量: 0
"""

if __name__ == '__main__':

    # press_url = f"http://192.168.0.11:8081/v1/chat/completions"

    THREAD_NUM =1  # 并发线程总数
    ONE_WORKER_NUM = 100  # 每个线程的循环次数
    LOOP_SLEEP = 0.1  # 每次请求时间间隔(秒)
    ERROR_NUM = 0  # 出错数
    model="Qwen-7B-Chat"
    base_url="127.0.0.1:8084"
    base_url="61.141.232.106:8084"
    obj = Presstest(model,base_url)
    t1 = time.time()
    ##openai 接口
    # r1=obj.testinterface3()
    # # print(r1.content)
    # res = json.loads(r1.content.decode("utf8"))
    # content=res["choices"][0]["message"]["content"]
    # print(f"------------------------------------")
    # print("解析前参数",content)
    
    # print("解析后参数",parse_json_markdown_for_list(content))
    
    #意图识别
    # obj.testinterface2()
    #函数参数解析
    obj.testinterface()
    # print(content)
    # obj.run()
    t2 = time.time()
    print("总耗时(秒):", t2 - t1)

"""
lmdeploy serve api_server /home/ubuntu/.cache/modelscope/hub/qwen/Qwen-14B-Chat-Int4 --model-name Qwen-14B-Chat-Int4 --instance_num 32 --tp 1  /
--server_name 0.0.0.0 --server_port 8081

lmdeploy chat --mode-path /home/ubuntu/.cache/modelscope/hub/qwen/Qwen-14B-Chat --model-name Qwen-14B-Chat-Int4



lmdeploy lite calibrate --mode-path ./Qwen-14B-Chat --work-dir ./Qwen-14B-Chat-my4bit

lmdeploy lite calibrate --mode ./internlm-20b --work-dir ./internlm-20b-my4bit
lmdeploy lite auto_awq --mode ./internlm-20b --work-dir ./internlm-20b-my4bit


"""