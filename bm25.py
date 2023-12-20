#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: juzipi
@file: bm25.py
@time:2022/04/16
@description:
"""
import collections
import math
import os
from typing import List

import jieba
import pickle
import logging

from doc import Doc

jieba.setLogLevel(log_level=logging.INFO)


class BM25Param(object):
    def __init__(self, f, df, idf, length, avg_length, docs_list, line_length_list,key_docindex,k1=1.5, k2=1.0,b=0.75):
        """

        :param f:
        :param df:
        :param idf:
        :param length:
        :param avg_length:
        :param docs_list:
        :param line_length_list:
        :param k1: 可调整参数，[1.2, 2.0]
        :param k2: 可调整参数，[1.2, 2.0]
        :param b:
        """
        self.f = f
        self.df = df
        self.k1 = k1
        self.k2 = k2
        self.b = b
        self.idf = idf
        self.length = length
        self.avg_length = avg_length
        self.docs_list = docs_list
        self.line_length_list = line_length_list
        self.key_docindex=key_docindex

    def __str__(self):
        return f"k1:{self.k1}, k2:{self.k2}, b:{self.b}"


class BM25(object):
    _stop_words_path = "data/stop_words.txt"
    _stop_words = []

    def __init__(self, docs:List[Doc]):
        self.docs=docs
        self.param: BM25Param = self._load_param()

    def _load_stop_words(self):
        if not os.path.exists(self._stop_words_path):
            ValueError(f"system stop words: {self._stop_words_path} not found")
        stop_words = []
        with open(self._stop_words_path, 'r', encoding='utf8') as reader:
            for line in reader:
                line = line.strip()
                stop_words.append(line)
        return stop_words

    def _build_param(self,Docs:List[Doc]):
            f = []  # 列表的每一个元素是一个dict，dict存储着一个文档中每个词的出现次数
            df = {}  # 存储每个词及出现了该词的文档数量
            idf = {}  # 存储每个词的idf值

            length = len(Docs)
            words_count = 0
            docs_list = []
            line_length_list =[]
            for doc in Docs:
                line=doc.name
                if not line:
                    continue
                words = [word for word in jieba.lcut_for_search(line) if word and word not in self._stop_words]
                line_length_list.append(len(words))
                docs_list.append(doc)
                words_count += len(words)
                tmp_dict = {}
                for word in words:
                    tmp_dict[word] = tmp_dict.get(word, 0) + 1
                f.append(tmp_dict)
                for word in tmp_dict.keys():
                    df[word] = df.get(word, 0) + 1
            for word, num in df.items():
                idf[word] = math.log(length - num + 0.5) - math.log(num + 0.5)

            key_docindex=collections.defaultdict(set)
            for i,doc in enumerate(f):
                for word in doc:
                    key_docindex[word].add(i)

            param = BM25Param(f, df, idf, length, words_count / length, docs_list, line_length_list,key_docindex)
            return param

    def _load_param(self):
        self._stop_words = self._load_stop_words()
        self._stop_words.append("查询")
        param = self._build_param(self.docs)
        return param

    def _cal_similarity(self, words, index):
        score = 0
        for word in words:
            if word not in self.param.f[index]:
                continue
            molecular = self.param.idf[word] * self.param.f[index][word] * (self.param.k1 + 1)
            denominator = self.param.f[index][word] + self.param.k1 * (1 - self.param.b +
                                                                       self.param.b * self.param.line_length_list[index] /
                                                                       self.param.avg_length)
            score += molecular / denominator
        return score

    def cal_similarity(self, query: str)->List[Doc]:
        """
        相似度计算，无排序结果
        :param query: 待查询结果
        :return: [(doc, score), ..]
        """
        key_docindex=self.param.key_docindex
        words = [word for word in jieba.lcut_for_search(query) if word and word not in self._stop_words]
        indexs=set()
        for word in words:
            indexs=indexs.union(key_docindex[word])

        indexs=list(indexs)
        score_list = []
        for index in indexs:
            score = self._cal_similarity(words, index)
            doc=self.param.docs_list[index]
            doc.score=score
            score_list.append(doc)
        return score_list

    def __sim_rank__(self, query: str)->List[Doc]:
        """
        相似度计算，排序
        :param query: 待查询结果
        :return: [(doc, score), ..]
        """
        result = self.cal_similarity(query)
        result.sort(key=lambda x: -1*x.score)

        res=[e for e in result if e.score>=0]

        if len(res):
            high_score=res[0].score
            E=10E-8
            res=[e for e in res if (e.score+E)/(high_score+E)>=0.8 and (e.score+E)/(high_score+E)<=1]

        res=res or result
        log=",".join([f"{e.name}/{e.score}" for e in res])
        logging.info(f"query:{query},\tresult:{log}")
        log = ",".join([f"{e.name}/{e.score}" for e in result])
        print(f"query:{query},\tresult--all:{log}")
        return res or result

    async def cal_similarity_rank(self,query)->List[Doc]:

        return self.__sim_rank__(query)

    def calc_similarity_rank(self, query) -> List[Doc]:

        return self.__sim_rank__(query)

if __name__ == '__main__':
    # bm25 = BM25()
    query_content = "站点业绩"
    docs = ["门店当天实时业绩查询", "门店按天查询业绩",
                          "站点当天实时业绩查询", "站点按天查询业绩","查询订单详情", "查询订单配送状态", "查询订单金额状态"]

    docs = [Doc(funtion_id=f"id:{i}", name=name) for i, name in enumerate(docs)]

    bm25 = BM25(docs)
    # sim = search.calc_similarity_rank("业绩")
    # print(sim)
    # result = bm25.cal_similarity(query_content)
    # for i,(line, score) in enumerate(result):
    #     print(i,line, score)
    # print("**"*20)
    result = bm25.calc_similarity_rank(query_content)
    for i,line in enumerate(result):
        print(i,line.funtion_id,line.name,line.score)
