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

作为AI客服，请根据以下数据库查询信息回复聊天记录中用户的问题，
1.渠道查询：查询结果如下:[{"渠道名称":"线下收银","渠道id":21},{"渠道名称":"门店收银","渠道id":22},{"渠道名称":"门店收银（有赞）","渠道id":23},{"渠道名称":"外卖渠道-美团外卖西饼","渠道id":31},{"渠道名称":"外卖渠道-饿了么西饼","渠道id":32},{"渠道名称":"无人售货机","渠道id":396},{"渠道名称":"新零售APP","渠道id":437},{"渠道名称":"幸福西饼GO小程序","渠道id":1101},{"渠道名称":"新零售APP","渠道id":1102},{"渠道名称":"幸福西饼DIY","渠道id":1104},{"渠道名称":"智慧零售小程序","渠道id":1105},{"渠道名称":"幸福西饼生日蛋糕自烤面包","渠道id":1106},{"渠道名称":"幸福商城","渠道id":1301},{"渠道名称":"星厨","渠道id":1302},{"渠道名称":"中石化商城","渠道id":1303},{"渠道名称":"新零售商城","渠道id":1304},{"渠道名称":"鹏福供应商城","渠道id":1305},{"渠道名称":"团购频道","渠道id":1306},{"渠道名称":"农行商城","渠道id":1307},{"渠道名称":"商城团购频道","渠道id":1308},{"渠道名称":"自营团购","渠道id":1309},{"渠道名称":"幸福送H5","渠道id":1310},{"渠道名称":"B端商城","渠道id":1311},{"渠道名称":"外卖渠道-饿了么切件","渠道id":3202},{"渠道名称":"有赞-王森世界名厨蛋糕","渠道id":3304},{"渠道名称":"有赞-幸福西饼微信商城","渠道id":3305},{"渠道名称":"有赞-幸福先生旗舰店","渠道id":3307},{"渠道名称":"有赞-喜芝派","渠道id":3308},{"渠道名称":"有赞-幸福西饼糕点铺","渠道id":3309},{"渠道名称":"有赞-幸福in成都","渠道id":3310},{"渠道名称":"秋华蓝卡","渠道id":3601},{"渠道名称":"苏州中国银行","渠道id":3602},{"渠道名称":"第三方小渠道-东方福利网","渠道id":3603},{"渠道名称":"商城大客户部-生活榜样","渠道id":3604},{"渠道名称":"第三方小渠道-花礼网","渠道id":3605},{"渠道名称":"丰食","渠道id":3606},{"渠道名称":"第三方小渠道-礼舍网","渠道id":3608},{"渠道名称":"第三方小渠道-联联周边游","渠道id":3609},{"渠道名称":"第三方小渠道-云闪付银联","渠道id":3610},{"渠道名称":"商城大客户部-品诺","渠道id":3611},{"渠道名称":"商城大客户部-熊猫优福","渠道id":3612},{"渠道名称":"商城大客户部-优荟加","渠道id":3613},{"渠道名称":"商城大客户部-聚福宝","渠道id":3614},{"渠道名称":"电商渠道-拼多多","渠道id":3701},{"渠道名称":"美团团购配送","渠道id":31001},{"渠道名称":"外卖渠道-美团外卖星厨","渠道id":31002},{"渠道名称":"外卖渠道-饿了么星厨","渠道id":32001},{"渠道名称":"电商渠道-京东旗舰店","渠道id":39101},{"渠道名称":"电商渠道-京东自营店","渠道id":39102},{"渠道名称":"京东-幸福先生旗舰店","渠道id":39103},{"渠道名称":"电商渠道-京东食品店","渠道id":39104},{"渠道名称":"电商渠道-天猫旗舰店","渠道id":39202},{"渠道名称":"第三方小渠道-考拉订蛋糕","渠道id":40423},{"渠道名称":"第三方小渠道-盒马鲜生","渠道id":40424},{"渠道名称":"团购渠道-支付宝口碑","渠道id":40438},{"渠道名称":"团购渠道-美团点评","渠道id":40439},{"渠道名称":"团购渠道-抖音","渠道id":40441},{"渠道名称":"团购渠道-快手","渠道id":40442},{"渠道名称":"商城大客户部","渠道id":40712},{"渠道名称":"售后单","渠道id":40715},{"渠道名称":"全名营销订单","渠道id":40744},{"渠道名称":"抖店-幸福西饼官方旗舰店","渠道id":300101},{"渠道名称":"抖店-幸福西饼烘焙旗舰店","渠道id":300102},{"渠道名称":"外卖渠道-抖音外卖","渠道id":360701},{"渠道名称":"小渠道","渠道id":4044041},{"渠道名称":"市场部免费单","渠道id":4070926},{"渠道名称":"市场部销售单","渠道id":4070927}]
2.覆盖城市数:查询结果如下：{"城市数量":350}
3.订单查询：查询结果如下：单号：xs1234565，商品名称：黑森林，单价：158，数量：1，总价：158，配送状态：结束
数据库查询信息不存在请回复，暂无法解答
用户聊天记录：
user:帮我查询单号xs1234565的详情
assistant:尊敬的用户，感谢您的咨询。您的单号为xs1234565的订单已经结束，商品名称为黑森林，单价为158，数量为1，总价为158元。如果您还有其他问题，欢迎再次咨询。
user:广东省直营店最高销量多少
你的回复：

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
        global ERROR_NUM
        try:
            print('开始调接口：', datetime.datetime.now().strftime('%Y-%m-%d- %H:%M:%S:%f'))
            user_inpt="订单查询XS2023121515590681195"
            post_json=json.dumps({"funtion_id":"2114","message":[{"role": "user", "content": user_inpt}]})
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
            post_json =json.dumps({"message" :[{"role": "user", "content": "广东省直营店最高销量多少"}]})
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
            system_conten="""\n你当前是幸福西饼AI客服，请根据幸福西饼的查询信息尽可能回答用户的问题，\n幸福西饼查询信息如下：1.通过订单号查询订单详情,查询结果如下:单号：xs1234565，商品名称：黑森林，单价：158，数量：1，用户购买量：三千万，总价：158，配送时间：2023-11-18配送状态：结束\n2.幸福西饼覆盖多少个城市,查询结果如下:{数量：300}\n请使用仅限于查询信息尽可能回复用户一个或多个问题，其他跟幸福西饼无关问题请回复:未查到信息，请尝试咨询其他业务\n你的回复:\n
            """
            
            message=[
                    {"role": "user", "content":"订单xs1234565详情和在多少个城市开店(请使用幸福西饼查询信息回复我的问题)"},
                    #   {"role": "assistant", "content":" 单号：xs1234565，商品名称：黑森林，单价：158，数量：1，用户购买量：三千万，总价：158，配送时间：2023-11-18配送状态：结束。幸福西饼覆盖300个城市。"},
                    #   {"role": "user", "content":"用户购买量"},
                    #   {"role": "assistant", "content":"用户购买量为三千万。"},
                    # {"role": "user", "content":"谷歌的创始人是谁（请使用幸福西饼查询信息回复）"},
                    {"role": "function", "content":" 单号：xs1234565，商品名称：黑森林，单价：158，数量：1，用户购买量：三千万，总价：158，配送时间：2023-11-18配送状态：结束。幸福西饼覆盖300个城市。"},
                ]


            messs=[{"role": "system", "content": system_conten}]
            messs.extend(message)
            if isinstance(messs,str):
                # history.append({"role": "user", "content":text3})
                history=messs
            else:
                for mess in messs:
                    history.append({"role": mess["role"], "content": mess["content"]})
            api_base = "http://192.168.0.11:8081/v1"
            llm_model=self.model
            # llm_model="internlm-chat"
            data=json.dumps({
                "model": llm_model,
                "messages": history,
                "stream": False,
                "top_p":0.


              })
            r1 = requests.post(f"{api_base}/chat/completions", headers={'Content-Type': 'application/json'},data=data)
            # print(r1.content)
            
            try:
                res = json.loads(r1.content.decode("utf8"))
                content=res["choices"][0]["message"]["content"]
                # print(f"------------------------------------")
                
                print("解析后参数",parse_json_markdown(content))
            except:
                
                res = json.loads(r1.content.decode("utf8"))
                content=res["choices"][0]["message"]["content"]
                print(content)
            return r1
            

        except Exception as e:
            print(e)
            ERROR_NUM += 1



    #### 美化语言
    def testinterface4(self):

        
        cont="""{"订单号":"XS2023121515590681195","配送时间":"2023-12-15 19:30:00","订单id":1185249689478250496,"订单状态":"待备货"}"""
        cont2="""{数量：300}"""
        post_json=json.dumps({
            "funname_resp":[{"funtion_id": "2114", "resp": cont},
                            {"funtion_id": "2123", "resp": cont2}],
            "message":[
                    # {"role": "user", "content":"订单XS2023121515590681195和覆盖了多少个城市"},
                        # {"role": "assistant", "content":"您好，订单XS2023121515590681195的配送时间是2023-12-15 19:30:00，订单状态是\"待备货\"。关于幸福西饼覆盖的城市数量，查询详情结果如下:数量：300。感谢您的提问！"},
                        # {"role": "user", "content":"配送时间是多少"},
                        # {"role": "assistant", "content":"您好，订单XS2023121515590681195的配送时间是2023-12-15 19:30:00。感谢您的提问！"},
                        # {"role": "user", "content":"XS2023121515590681195"},
                    # {"role": "assistant", "content":"未查到信息，请尝试咨询其他业务。"},
                    {"role": "user", "content":"广州销量最高的店铺"},
                ]})

        r1 = requests.post(f"http://{self.base_url}/beautify_chat/completions", data=post_json)
        print(r1.content.decode("utf8"))

    def testonework(self):
        '''一次并发处理单个任务'''
        i = 0
        while i < ONE_WORKER_NUM:
            i += 1
            self.testinterface4()
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

    THREAD_NUM =100  # 并发线程总数
    ONE_WORKER_NUM = 1  # 每个线程的循环次数
    LOOP_SLEEP = 0.1  # 每次请求时间间隔(秒)
    ERROR_NUM = 0  # 出错数
    model="Qwen-14B-Chat-Int4"
    base_url="127.0.0.1:8084"
    # base_url="61.141.232.106:8084"
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
    
    #### 美化语言
    # obj.testinterface4()
    
    #函数参数解析
    for i in range(1):
        t0 = time.time()
        obj.testinterface4()
        t02 = time.time()
        print("总耗时(秒):", t02 - t0)
    # print(content)
    # obj.run()
    t2 = time.time()
    print("总耗时(秒):", t2 - t1)



