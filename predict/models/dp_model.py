import heapq
import json
import time

from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean
from models.cf_model import CfModel
import numpy as np


def read_file(file_path):
    data = dict()
    values = []
    dataIds = []
    f = open(file_path, 'r')
    f.readline()
    line = f.readline()
    while line:
        #处理数据
        idstrs = line.strip().split(" ")
        id = int(idstrs[0])
        embeddings = []
        i = 1
        while i<63:
            embeddings.append(float(idstrs[i]))
            i+=1
        data[id] = embeddings
        values.append(embeddings)
        dataIds.append(id)
        line = f.readline()
    return data,values,dataIds

def read_map(map_path):
    with open(map_path, 'r') as f:
        dict = json.load(fp=f)
        # print(dict)
    return dict

def reverse_map(map,dataIds):
    idmap2 = dict()
    names = []
    for k, v in map.items():
        idmap2.setdefault(v, k)
    for item in dataIds:
        names.append(idmap2[item])
    return idmap2,names
class DPModel(object):
    #maxNum是一个物品最多推荐的数目
    def __init__(self, model_path,map_path, maxNum):
        self.path = model_path
        self.map_path = map_path
        self.maxNum = maxNum
        self.read_model()
        self.reversedMap,self.names = reverse_map(self.idMap,self.dataIds)
    def setMaxNum(self,num):
        self.maxNum = num
    def read_model(self):
        self.data,self.values,self.dataIds = read_file(self.path)
        self.idMap = read_map(self.map_path)
        # print(self.mapSimilarity.keys())
    def getKey(self,name):
        return self.idMap[name]
    # def getAll(self,key):
    #     return self.mapSimilarity.get(key)
    def getEmbeddingByKey(self,key):
        return self.data[key]
    def getEmbeddingByName(self,name):
        if self.idMap[name] is not None:
            return self.data[self.idMap[name]]
    def getMaxNum(self):
        return self.maxNum
    def getSimilarity(self,name1,name2):
        return 1/cosine(self.data[self.idMap[name1]],self.data[self.idMap[name2]])
    def getSimilarityByKey(self,key1,key2):
        return 1/cosine(self.data[key1],self.data[key2])
    def getSimilarityByKeyAndEmbedding(self,embd,key2):
        return 1/cosine(embd,self.data[key2])
    def getAllSimilarity(self,names):
        embeddings = []
        totalNum = self.maxNum*len(names)
        result = []
        usefulName = []
        for name in names:
            if name in self.names:
                usefulName.append(name)
                embeddings.append(self.data[self.idMap[name]])
        similarity = cosine_similarity(embeddings,self.values)
        sortList = []
        for i in range(len(usefulName)):
            currentSim = similarity[i]
            a = np.argsort(-currentSim)
            finalResult = []
            for i in range(self.maxNum*2):
                if i!=0:
                    finalResult.append((currentSim[a[i]],self.names[a[i]]))
            sortList.extend(finalResult)
        sortList = set(sortList)
        sortList = list(sortList)
        sortList = sortList[np.argsort(-result)]
        return sortList[:totalNum]

    def getMostSimilar(self, name):
        id = self.idMap[name]
        embedding = self.data[id]
        result = cosine_similarity([embedding], self.values)
        result = result[0]
        # 降序排序
        a = np.argsort(-result)
        finalResult = []
        for i in range(self.maxNum + 1):
            if i != 0:
                finalResult.append((result[a[i]], self.names[a[i]]))
        return finalResult
    # def getListSimilarity(self,names):
    #     embeddings = []
    #     for name in names:
    #         embeddings.append(self.data[self.idMap[name]])
    #
    # key 格式 ： cases/hkca/2018/821  全都处理成这样
    # def getSimilarItems(self, key):
    #     items = self.mapSimilarity.get(key)
    #     if items==None:
    #         return None
    #     if len(items) != 0 and len(items) > self.maxNum:
    #         return items[:self.maxNum]
    #     return items

if __name__ == '__main__':
    DPModel = DPModel("../model_data/log.embeddings","../model_data/idmap.txt",100)
    demo = "cases/hkcfi/1998/1039"
    print(DPModel.getSimilarity(demo,'cases/hkcfi/2012/995'))
    print(DPModel.getSimilarity(demo, 'cases/hkcfi/2005/168'))
    t0 = time.time()
    result = DPModel.getMostSimilar("cases/hkcfi/1998/1039")
    print(result)
    t1 = time.time()
    print('time cost: %s sec' % (t1 - t0))
    # CFModel = CfModel("../model_data/similarities.txt",50)
    # tmpresult2 = CFModel.getSimilarItems(demo)
    # result1 = [item[1] for item in result]
    # result2 = [item[1] for item in tmpresult2]
    # print(result2)
    # print(result1)
    # num = 0
    # for item in result1:
    #     if item in result2:
    #         print(item)
    #         num+=1
    # print(num)