from models.dw_model import DWModel
from models.cf_model import CfModel
class LogModel(object):
    def __init__(self,cfModel,dwModel):
        self.cfModel = cfModel
        self.dwModel = dwModel
    def setSingleNum(self,singleNum):
        self.singleNum = singleNum
        self.dwModel.setSingleNum(singleNum)
    def getRecommendation(self,names):
        resultCF = []
        resultDW = []
        # allNames = self.dwModel.getAllNamesSet()
        for name in names:
            # if name in allNames:
            resultCF.extend(self.cfModel.getAll(name))
            resultDW.extend(self.dwModel.getAll(name))
        newSet = set()
        resultDW.sort(reverse=True)
        # print(resultDW.__class__)
        finalResult = []
        for item in resultDW:
            if item[1] not in newSet:
                newSet.add(item[1])
            elif item[1] not in finalResult:
                finalResult.append(item[1])
        for item in resultCF:
            if item[1] not in newSet:
                newSet.add(item[1])
            elif item[1] not in finalResult:
                finalResult.append(item[1])
        # finalResult = list(set(finalResult))
        # finalSet = set(finalResult)
        if (len(finalResult) > len(names) * self.singleNum):
            return set(finalResult[:len(names) * self.singleNum])
        # finalResult = set(finalResult)
        leftNum = len(names) * self.singleNum - len(finalResult)
        if leftNum > 0 and resultDW is not None:
            initResult = resultDW[:int(leftNum*1.2)]
            tmpResult = [key[1] for key in initResult]
            # tmpResult = list(set(tmpResult))
        index = 0
        num = 0
        finalResult = set(finalResult)
        while num<leftNum and index<len(tmpResult):
            if tmpResult[index] not in finalResult:
                finalResult.add(tmpResult[index])
                num+=1
            index+=1
        # finalResult = list(finalResult)
        # finalResult = set(finalResult)
        return finalResult