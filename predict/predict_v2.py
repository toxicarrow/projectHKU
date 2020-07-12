import json
import time

import numpy as np

from models.cf_model import CfModel

path = "validate_data/access_July_inMap.txt"
import matplotlib.pyplot as plt
import numpy as np
from models.dw_model import DWModel
from models.log_model import LogModel
from models.random_model import RandomModel

def read_file(file_path):
    with open(file_path, 'r') as f:
        dict = json.load(fp=f)
        # print(dict)
    return dict

def split_evaluate_data(dict,trainNum,validateNum,baseNum):
    totalSize = trainNum+validateNum
    predictList = []
    validateList = []
    # i = 0
    # print(i)
    for key in dict.keys():
        accessObjs = dict.get(key)
        #去重
        accessObjs = set(accessObjs)
        accessObjs = list(accessObjs)
        accessNum = len(accessObjs)
        time = 0
        #小于划分大小，分为前半和后半
        if accessNum>baseNum and accessNum<totalSize:
            predictList.append(accessObjs[:int(accessNum/2)])
            validateList.append(accessObjs[int(accessNum/2):])
            # print(i)
        while (accessNum-totalSize*time)>totalSize:
            tmpPre = accessObjs[totalSize*time:(totalSize*time+trainNum)]
            predictList.append(tmpPre)
            if totalSize*(time+1)<accessNum:
                validateList.append(accessObjs[(totalSize*time+trainNum):(totalSize*(time+1))])
            else:
                validateList.append(accessObjs[(totalSize * time + trainNum):])
            # print(i)
            time = time+1
        # print(predictList,"\r")
        # if accessNum-totalSize*time>baseNum:
        #     half = int(totalSize*time + (accessNum-totalSize*time)/2)
        #     predictList[i] = accessObjs[totalSize*time:half]
        #     validateList[i] = accessObjs[half:]
        #     i+=1
    # print("return !!!!!!!")
    return predictList,validateList


def split_evaluate_dataV2(dict,maxNum):
    predictList = []
    validateList = []
    # i = 0
    # print(i)
    for key in dict.keys():
        accessObjs = dict.get(key)
        #去重
        # accessObjs = set(accessObjs)
        # accessObjs = list(accessObjs)
        accessNum = len(accessObjs)
        if(accessNum>maxNum):
            continue
        if accessNum>8:
            splitLine = int(accessNum/4)
            predictList.append(set(accessObjs[:splitLine]))
            validateList.append(set(accessObjs[splitLine:]))
        # print(predictList,"\r")
        # if accessNum-totalSize*time>baseNum:
        #     half = int(totalSize*time + (accessNum-totalSize*time)/2)
        #     predictList[i] = accessObjs[totalSize*time:half]
        #     validateList[i] = accessObjs[half:]
        #     i+=1
    # print("return !!!!!!!")
    return predictList,validateList

#这个是deepwalk版本
def get_predict_set_forDP(model,predicts):
    return model.getRecommendation(predicts)
#这个和版本1的区别就是会优先使用在不同item的相似度列表里都出现的item
def get_predict_set2(model,predicts):
    maxNum = model.getMaxNum()
    recSet = set()
    resultSet = set()
    recommendationList = []
    for access in predicts:
        recommendation = model.getAll(access)
        if recommendation is not None:
            recommendationList.append(recommendation)
            for item in recommendation:
                if item[1] in recSet:
                    resultSet.add(item[1])
                recSet.add(item[1])
    if len(recommendationList)==0:
        return resultSet
    if len(resultSet)>len(predicts)*maxNum:
        resultList = list(resultSet)
        return resultList[:len(predicts)*maxNum]
    leftEach = int((len(predicts)*maxNum-len(resultSet))/len(recommendationList))
    for i in range(len(recommendationList)):
        resultSet = getNMore(leftEach,recommendationList[i],resultSet)
    return resultSet

def get_predict_set(model,predicts):
    maxNum = model.getMaxNum()
    recSet = set()
    resultSet = set()
    recommendationList = []
    for access in predicts:
        recommendation = model.getAll(access)
        if recommendation is not None:
            recommendationList.append(recommendation)
            # for item in recommendation:
            #     if item[1] in recSet:
            #         resultSet.add(item[1])
            #     recSet.add(item[1])
    if len(recommendationList)==0:
        return resultSet
    leftEach = int((len(predicts)*maxNum)/len(recommendationList))
    for i in range(len(recommendationList)):
        resultSet = getNMore(leftEach,recommendationList[i],resultSet)
    return resultSet


def get_predict_set_logAll(model,predicts):
    return model.getRecommendation(predicts)
def getNMore(n,recommendation,resultSet):
    i = 0
    for item in recommendation:
        if i>=n:
            return resultSet
        if item[1] not in resultSet:
            i+=1
            resultSet.add(item[1])
    return resultSet

def preditV2( model,predictList,validateList,getPredictFunc):
    precision = []
    hits = []
    predict_num = []
    access_num = []
    # random_recommend_expect = []
    recall = []
    # i = 1
    for i in range(len(predictList)):
        predicts = predictList[i]
        validates = validateList[i]
        if len(predicts) == 0:
            break
        rec_set = getPredictFunc(model,predicts)
        hit = 0
        if i==10:
            break
        if len(rec_set)==0:
            continue
        # print(validates)
        for item in validates:
            # print(item)
            if item in rec_set:
                hit += 1
        if len(validates) is not 0 and len(rec_set) is not 0:
            precision.append(float(hit) / float(len(validates)))
            recall.append(float(hit) / float(len(rec_set)))
        else:
            continue
        hits.append(hit)
        predict_num.append(len(rec_set))
        access_num.append(len(validates))
        if i>1000:
            return precision, recall, hits, predict_num, access_num
    return precision, recall, hits, predict_num, access_num
def predit(model,predictList,validateList):
    # fileSave = open("result_hit_noHit.txt", 'w')
    # fileHitMuch = open("result_hit_much.txt", 'w')
    # hitmuch = dict()
    # ips = []
    # hasHit = []
    # noHit = []
    precision = []
    hits = []
    predict_num = []
    access_num = []
    # random_recommend_expect = []
    recall = []
    # i = 1
    for i in range(len(predictList)):
        predicts = predictList[i]
        validates = validateList[i]
        if len(predicts) == 0:
            break
        rec_set = set()
        for access in predicts:
            recommendation = model.getSimilarItems(access)
            if recommendation is not None:
                for item in recommendation:
                    rec_set.add(item[1])
                    # print(item[1], "\r")
        # print(rec_set,"\r")
        if len(rec_set)==0:
            continue
        hit = 0
        # print(validates)
        for item in validates:
            # print(item)
            if item in rec_set:
                hit += 1
        if len(validates) is not 0 and len(rec_set) is not 0:
            precision.append(float(hit) / float(len(validates)))
            recall.append(float(hit) / float(len(rec_set)))
        else:
            continue
        hits.append(hit)
        predict_num.append(len(rec_set))
        access_num.append(len(validates))
    return precision, recall, hits, predict_num, access_num

def get_random_recommend(model,names):
    return model.getRecommendation(names)
if __name__ == '__main__':
    mapPredict = read_file(path)
    cf_model = CfModel("model_data/similarities.txt",15)
    dw_model = DWModel("model_data/result.txt",10)
    # print(len(dict(map2).keys()))
    # predictList,validateList = split_evaluate_data(dict(mapPredict),5,15,6)
    predictList, validateList = split_evaluate_dataV2(dict(mapPredict), 400)
    # print(predictList[0], "aaaaaa")
    # print(validateList[0],"aaaaaa")
    print(len(predictList),'\n')
    print(len(validateList),'\n')
    predictNum = [5, 8, 10, 15, 20,25,30,35,40,45,50,55,60]
    recalls = []
    precisions = []
    hits = []
    hits2 = []
    recalls2 = []
    precisions2 = []

    recallCF = []
    precisionCF = []

    recallBase = []
    precisionBase = []

    random_model = RandomModel(dw_model.getAllNamesSet())
    # 随机模型
    for num in predictNum:
        random_model.setSingleNum(num)
        precision, recall, hit, predict_num, access_num = preditV2(random_model, predictList, validateList,
                                                                   get_random_recommend)
        # hits.append(np.average(hit))
        recallBase.append(np.sum(hit) / np.sum(access_num))
        precisionBase.append(np.sum(hit) / np.sum(predict_num))

    #cf用
    for num in predictNum:
        cf_model.setMaxNum(num)
        precision, recall, hit, predict_num, access_num = preditV2(cf_model, predictList, validateList,get_predict_set2)
        # hits.append(np.average(hit))
        precisionCF.append(np.sum(hit) / np.sum(access_num))
        recallCF.append(np.sum(hit) / np.sum(predict_num))

    # # for deepwalk
    # for num in predictNum:
    #     dw_model.setSingleNum(num)
    #     precision, recall, hit, predict_num, access_num = preditV2(dw_model, predictList, validateList,get_predict_set_forDP)
    #     precisions.append(np.sum(hit) / np.sum(access_num))
    #     recalls.append(np.sum(hit) / np.sum(predict_num))
    #     hits.append(np.average(hit))
    #     # fpr.append(np.sum(predict_num)-np.sum(hit)/np.sum(predict_num))
    #     # tpr.append()

    log_model = LogModel(cf_model,dw_model)
    #for dw & cf
    for num in predictNum:
        log_model.setSingleNum(num)
        precision, recall, hit, predict_num, access_num = preditV2(log_model, predictList, validateList,get_predict_set_logAll)
        precisions2.append(np.sum(hit) / np.sum(access_num))
        recalls2.append(np.sum(hit) / np.sum(predict_num))
        hits2.append(np.average(hit))

    # f = open("plot.txt",'w')
    # plotData = dict()
    # plotData["recalls"] = recalls
    # plotData["precisions"] = precisions
    # plotData["recalls2"] = recalls2
    # plotData["precisions2"] = precisions2
    # plotData["hits"] = hits
    # plotData["hits2"] = hits2
    # f.write(json.dumps(plotData))
    # f.close()


    plt.xlabel("predict num")
    plt.ylabel("precision&recall")
    # l1 = plt.plot(predictNum, recalls, color='#708069', label='dw_recall',linewidth=2)
    # l2 = plt.plot(predictNum, precisions, color='#808069', label='dw_precision',linewidth=2)
    plt.plot(predictNum, recallBase, color='#708069', label='random_recall', linewidth=2)
    plt.plot(predictNum, precisionBase, color='#292421', label='random_precision',linewidth=2)
    plt.plot(predictNum, precisions2, color='#E3CF57', label='log_precision',linewidth=2)
    plt.plot(predictNum, recalls2, color='#FF9912', label='log_recalls',linewidth=2)
    plt.plot(predictNum, precisionCF, color='#4169E1', label='cf_precision',linewidth=2)
    plt.plot(predictNum, recallCF, color='#40E0D0', label='cf_recalls',linewidth=2)
    # 显示图示
    plt.legend()
    # 显示图
    plt.show()

    # plt.xlabel("predict num")
    # plt.ylabel("hit num")
    # plt.plot(predictNum, hits, color='blue', label='hit num',linewidth=2)
    # plt.xlabel("predict num")
    # plt.ylabel("hit num2")
    # plt.plot(predictNum, hits2, color='red', label='hit num2', linewidth=2)
    # # 显示图示
    # plt.legend()
    # # 显示图
    # plt.show()
    # precision, recall, hits, predict_num, access_num = predit(cf_model, predictList, validateList)
    # print("max hits : ", np.max(hits))
    # print("max hits prob : ", np.max(precision))
    # print("average hits prob : ", np.sum(hits)/np.sum(access_num))
    # print("average hits recall : ", np.sum(hits) / np.sum(predict_num))
    # print("average hits : ", np.average(hits))
    # print("hit 0 : ", hits.count(0.0))
    # print("total number : ", len(hits))
    # print("precision : ", precision)
    # print("recall : ", recall)
    # print("hits : ", hits)
    # print("predict_num : ", predict_num)
    # print("access_num : ", access_num)
