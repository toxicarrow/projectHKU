import json
import numpy as np


def read_file(file_path):
    with open(file_path, 'r') as f:
        dict = json.load(fp=f)
        # print(dict)
    return dict


class CfModel(object):
    #maxNum是一个物品最多推荐的数目
    def __init__(self, model_path, maxNum):
        self.path = model_path
        self.maxNum = maxNum
        self.read_model()
    def setMaxNum(self,num):
        self.maxNum = num
    def read_model(self):
        self.mapSimilarity = read_file(self.path)
        self.keySet = set(self.mapSimilarity.keys())
        # print(self.mapSimilarity.keys())
    def getAll(self,key):
        if key in self.keySet:
            return self.mapSimilarity.get(key)
        return []
    def getMaxNum(self):
        return self.maxNum
    # key 格式 ： cases/hkca/2018/821  全都处理成这样
    def getSimilarItems(self, key):
        items = self.mapSimilarity.get(key)
        if items==None:
            return None
        if len(items) != 0 and len(items) > self.maxNum:
            return items[:self.maxNum]
        return items
