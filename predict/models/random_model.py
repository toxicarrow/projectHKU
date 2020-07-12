import random
class RandomModel(object):
    def __init__(self,allNames):
        self.allNames = allNames
    def setSingleNum(self,singleNum):
        self.singleNum = singleNum
    def getRecommendation(self,names):
        num = self.singleNum*len(names)
        return random.sample(self.allNames,num)