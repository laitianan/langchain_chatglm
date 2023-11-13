#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import os
from typing import List, Optional
import jieba
import Levenshtein
import collections
class Doc():

    def __init__(self,funtion_id,name,score=0.0,fro="SEARCH"):

        self.funtion_id=funtion_id
        self.name=name
        self.score=score
        self.fro=fro
    def __eq__(self, other):
        h1 =self.__str__()
        h2 = other.__str__()
        return h1 == h2

    def __hash__(self):
        h=self.__str__()
        return hash(h)  # 如果直接写为hash(self)则会导致递归

    def __str__(self):
        h = f"name:{self.name},funtion_id:{self.funtion_id}"
        return h


class Query_Search(object):

    def __init__(self):

        self.word_docs=collections.defaultdict(set)


    def load(self,docs:List[Doc]):
        for doc in docs:
            for word in jieba.lcut(doc.name) :
                if  word not in ["查询"]:
                    a=self.word_docs[word]
                    a.add(doc)

    def __sim_rank__(self,query)->List[Doc]:
        docs = set()
        for word in jieba.lcut(query):
            docs = docs.union(self.word_docs[word])

        for doc in docs:
            # doc.score = Levenshtein.jaro(query, doc.name)
            doc.score=0
            doc.fro = "SEARCH"
        docs = list(docs)
        # docs = [e for e in docs if e.score > 0]
        # docs.sort(key=lambda x: x.score, reverse=False)
        return docs

    async def cal_similarity_rank(self,query)->List[Doc]:

        return self.__sim_rank__(query)

    def calc_similarity_rank(self, query) -> List[Doc]:

        return self.__sim_rank__(query)

if __name__ == '__main__':
    docs=["门店当天实时业绩查询","门店按天查询业绩"
"站点当天实时业绩查询","站点按天查询业绩"]


    docs=[Doc(funtion_id=f"{i}",name=name) for i,name in enumerate(docs)]

    search=Query_Search()
    search.load(docs)
    sim=search.calc_similarity_rank("业绩")
    print(sim)

    # bm25 = BM25()
    # query_content = "售后查询"
    # print(jieba.lcut(query_content))
    #
    # print(bm25.param.df)
    # print(bm25.param.idf)
    # result = bm25.cal_similarity(query_content)
    # for line, score in result:
    #     print(line, score)
    # print("**"*20)
    # result = bm25.cal_similarity_rank(query_content)
    # for line, score in result:
    #     print(line, score)




    # str1 = "订单售后查询"
    # str2 = "业绩"
    #
    # # Levenshtein距离
    # sim = Levenshtein.jaro(str1, str2)
    # print('Levenshtein similarity: ', sim)