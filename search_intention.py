#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import os
from typing import List, Optional
import jieba
import Levenshtein
import collections

from doc import Doc


class Query_Search(object):

    def __init__(self,docs:List[Doc]):

        self.word_docs=collections.defaultdict(set)
        self.load(docs)


    def load(self,docs:List[Doc]):
        for doc in docs:
            for word in jieba.lcut(doc.name) :
                if  word not in ["查询"]:
                    self.word_docs[word].add(doc)


    def __sim_rank__(self,query)->List[Doc]:
        docs = set()
        for word in jieba.lcut(query):
            docs = docs.union(self.word_docs[word])

        for doc in docs:
            doc.score = Levenshtein.jaro(query, doc.name)
            # doc.score=0
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
    docs=["门店当天实时业绩查询","门店按天查询业绩",
"站点当天实时业绩查询","站点按天查询业绩"]


    docs=[Doc(funtion_id=f"{i}",name=name) for i,name in enumerate(docs)]

    search=Query_Search(docs)
    # search.load(docs)
    sim=search.calc_similarity_rank("当天")
    for doc in sim:
        print(doc.name,doc.score)
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

    import jieba

    str = "幸福西饼是一家制作蛋糕非常美味的连锁企业"

    res=jieba.lcut(str,cut_all=True)
    print(res)
    res=jieba.lcut(str)
    print(res)