import heapq
import json


def read_file(file_path):
    with open(file_path,'r') as f:
        dict = json.load(f)
    return dict
class DWModel(object):
    def __init__(self, model_path,singleNum):
        self.data = read_file(model_path)
        self.keySet = set(self.data.keys())
        # self.singleNum = singleNum
    def getRecommendation(self,names):
        result = []
        for name in names:
            if name in self.keySet:
                result.extend(self.data[name])
        # result = set(result)
        # result = list(result)
        newSet = set()
        result.sort(reverse=True)
        finalResult = []
        for item in result:
            if item[1] not in newSet:
                newSet.add(item[1])
            elif item[1] not in finalResult:
                finalResult.append(item[1])
        # finalResult = list(set(finalResult))
        if(len(finalResult)>len(names)*self.singleNum):
            return finalResult[:len(names)*self.singleNum]
        leftNum = len(names)*self.singleNum-len(finalResult)
        if leftNum>0:
            initResult = result[:leftNum]
            tmpResult = [key[1] for key in initResult]
            finalResult.extend(tmpResult)
        # finalResult = list(finalResult)
        # finalResult = set(finalResult)
        return set(finalResult)
        # if len(result)>len(names)*self.singleNum:
        #     return heapq.nlargest(result,len(names)*self.singleNum)
        # else:
        #     return result
    def setSingleNum(self,singleNum):
        self.singleNum = singleNum
    def getAll(self,name):
        if name in self.keySet:
            return self.data[name]
        return []
    def getAllNamesSet(self):
        return self.keySet