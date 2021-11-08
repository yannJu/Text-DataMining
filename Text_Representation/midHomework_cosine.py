#-*-coding:utf-8-*-
import re
from numpy.core.fromnumeric import sort
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy.linalg import norm
import sys
import numpy as np

def biGram(patternsSplit, output, lines):
    target = list()
    for l in range(1, len(lines)):
    #----------------document분리->공백단위로 split하면 0번, -1번 인덱스는 ID와 target, ID자릿수 + 1 부터 doc
        tmp = lines[l].split()
        target.append(tmp[-1])
        lenID = len(tmp[0])
        text = lines[l][lenID + 1:-3]
        #----------------ASCII문자열 분리 & 한글 이외의 문자열 분리
        arySplit = re.compile(patternsSplit).findall(text) #ASCII문자열이 들은 배열
        resultSplit = re.sub(patternsSplit, "?", text) #ASCII문자열제거
        resultSplit = "_" + resultSplit.replace(" ", "_") + "_"
        #----------------분리된 문자열 bigram처리
        answer = ""
        isStart = False #분리된 문자열들의 범위를 찾기 시작해도 되는지의 유무
        idx = 0 #분리된 문자열들의 ary의 begin idx
        idxCnt = 1 #분리된 문자열들의 범위

        
        #1. isStart True면 분리된 문자열들의 범위를 찾음
        #2. 다음 문자가 "?"라면 범위를 1키움
        #3. 아니라면 idx~idx+범위 만큼 ary에서 char를 가져와서 answer에 추가
        #4. isStart False면 bigram을 통해 answer 추가
        #5. 단 다음 문자가 "?"라면 다음 문자부터는 분리된 문자열들의 범위를 탐색
        
        for i in range(len(resultSplit) - 1):
            if not isStart:
                if (resultSplit[i + 1] != "?"): answer += resultSplit[i] + resultSplit[i + 1] + " "
                else: isStart = True
            else:
                if resultSplit[i + 1] == "?": idxCnt += 1
                else:
                    isStart = False
                    for j in range(idx, idx + idxCnt): answer += arySplit[j]
                    answer += " " 
                    idx += idxCnt
                    idxCnt = 1
        if (len(resultSplit) == 1):
            if (resultSplit == "?"): answer += arySplit[0] + " "
            else: answer += "_" + arySplit[0] + " " + arySplit[0] + "_ "
        answer = answer[:-1] + "\n"
        output.write(answer)
    output.close()
    return target

#(문서번호, 해당 feature idx = 유사도) 반환
def vectorize(train, test):
    lines =  train + test
    vector = TfidfVectorizer()
    X = vector.fit_transform(lines)
    return X.todok()

def makeTextRepresentation(trainTarget, testTarget, all_vector, output_train,  output_test):
    train_textRepresent = ["{} ".format(i) for i in trainTarget]
    test_textRepresent = ["{} ".format(i) for i in testTarget]
    
    for v in all_vector.items():
        key = v[0]
        val = v[1]
        if (key[0] < len(trainTarget)): train_textRepresent[key[0]] += "{}:{} ".format(key[1], val)
        else: test_textRepresent[key[0] - len(trainTarget)] += "{}:{} ".format(key[1], val)
                                   
    for t in train_textRepresent: output_train.write(t + "\n")
    for t in test_textRepresent: output_test.write(t + "\n")
    output_train.close()
    output_test.close()

def mainStart():
    f_train = open('ratings_train.txt', 'r', encoding="utf-8")
    f_test = open('ratings_test.txt', 'r', encoding="utf-8")
    wf_train = open('output_Optimal_train.txt', 'w', encoding="utf-8")
    wf_test = open('output_Optimal_test.txt', 'w', encoding="utf-8")
    lines_train = f_train.readlines()
    lines_test = f_test.readlines()

    #숫자, 알파벳, 특수문자, 'ㅋㅋㅋ','ㅠㅠ'같은 문자 분리
    patternsSplit = '[-=+,#/\;?:^$.@*\♡☆★♪♩♬"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…\♥》a-zA-Z0-9ㄱ-ㅎㅏ-ㅣ]'

    #train/test Set Bigram
    trainTarget = biGram(patternsSplit, wf_train, lines_train)
    print("TrainSet BiGram Done-")
    testTarget = biGram(patternsSplit, wf_test, lines_test)
    print("TestSet BiGram Done-")
    f_train.close()
    f_test.close()

    #Bigram 한 파일들을 vector화 하기 위해 파일 open
    v_train = open('output_Optimal_train.txt', 'r', encoding="utf-8")
    wv_train = open('output_TextRepresentation_train.txt', 'w', encoding="utf-8")
    lines_train = v_train.readlines()

    v_test = open('output_Optimal_test.txt', 'r', encoding="utf-8")
    wv_test = open('output_TextRepresentation_test.txt', 'w', encoding="utf-8")
    lines_test = v_test.readlines()

    #파일 저장을 위해 행구분 되어있는 부분을 다 지움
    for i in range(len(lines_train)): lines_train[i] = lines_train[i][:-1] 
    for i in range(len(lines_test)): lines_test[i] = lines_test[i][:-1] 

    all_vector= vectorize(lines_train, lines_test)
    print("TrainSet Vectorize & TestSet Vectorize Done-")
    v_train.close()
    v_test.close()  
    
    #SVM format으로 TextRepresentation
    makeTextRepresentation(trainTarget, testTarget, all_vector, wv_train,  wv_test)
    print("TrainSet TextRepresentation & TestSet TextRepresentation Done-")

def findSimDoc(search):
        #----------------print Test Comment
    tRf = open('ratings_test.txt', 'r', encoding='utf-8') #test Comment 
    testComment = tRf.readlines()[search]
    tRfSplit = testComment.split()
    wordIdx = len(tRfSplit[0])
    comment = testComment[wordIdx + 1:]
    print("Search Comment : ", comment)
    
    #----------------file open (bigram testComment, SVM train Set, WordList)
    trainTRf = open('output_TextRepresentation_train.txt', 'r', encoding='utf-8')  #trainText Representation
    testTRf = open('output_TextRepresentation_test.txt', 'r', encoding='utf-8')  #testText Representation
    trainCmtf = open('ratings_train.txt', 'r', encoding='utf-8') #train Comment
    
    #----------------files Readlines()_train textRepresentation 댓글을 split하여 feature별로 구분
    trainAry = trainTRf.readlines()
    trainAry = [x.split() for x in trainAry]
    #--_찾으려는 test댓글의 bigram 댓글을 찾아서 split
    testCmt = testTRf.readlines()
    testCmt = testCmt[search - 1].split()
    testCmt =testCmt[1:]
    testAry = []
    testdict = dict()
    #-- feature들의 인덱스를 testAry에 넣고, feature와 tf-idf유사도값을 dictionary에추가
    for t in testCmt:
        tmp = t.split(':')
        testAry.append(int(tmp[0]))
        testdict[int(tmp[0])] = float(tmp[1])
    #-- _train bigram 댓글들의 id와 target을 분리 후 column을 설명하는 첫번째 줄을 제외
    trainCmt = trainCmtf.readlines()
    for l in range(len(trainCmt)):
        tmp = trainCmt[l].split()
        idIdx = len(tmp[0])
        trainCmt[l] = trainCmt[l][idIdx:-3]
    trainCmt = trainCmt[1:]
    
    #----------------values
    resultLst = []
    minIdx = 0
    
    #----------------Finds
    # 1. train set을 전체 탐색하는데, target을 분리하고 feature 인덱스를 리스트에 append하고 feature:tf-idf유사도를 딕셔너리에 추가
    #2. train 과 test의 feature들을 set을 이용하여 합침
    #3. 합친 feature들이 test와 train에 존재하면 value값을, 없으면 0을 추가하여 벡터크기를 맞춤
    #4. numpy로 만들어 코싸인 유사도 값을 구함
    for t in range(len(trainAry)):
        target = trainAry[t][0]
        tmp = trainAry[t][1:]
        compareTrain = []
        traindict = dict()
        for ct in tmp:
            c = ct.split(':')
            compareTrain.append(int(c[0]))
            traindict[int(c[0])] = float(c[1])
        # -- 
        allFeature = set(compareTrain + testAry)
        resultTrain = []
        resultTest = []
        for aF in allFeature:
            if (aF in testdict): resultTest.append(testdict.get(aF))
            else: resultTest.append(0)
            if (aF in traindict): resultTrain.append(traindict.get(aF))
            else: resultTrain.append(0)
            
        #---result2numpy & dot + cosine 유사도 구하기
        trainNP = np.array(resultTrain)
        testNP = np.array(resultTest)
        sim = np.dot(trainNP, testNP) / norm(trainNP) * norm(testNP)

        if (len(resultLst) < 5): resultLst.append((sim, t, int(target)))
        else:
            if (resultLst[minIdx][0] < sim): resultLst[0] = (sim, t, int(target))
        resultLst = sorted(resultLst, key = lambda x:x[0])
        
    cntPositive = 0
    resultPositive = 1
    #----------------Print
    print("-------------------------------------------------------")
    for r in range(len(resultLst) - 1, -1, -1): print("댓글({}) -> {}\n 유사도 : {} Positive? : {}".format(len(resultLst) - r, trainCmt[resultLst[r][1]], resultLst[r][0], resultLst[r][2]))
    print("-------------------------------------------------------")
    for p in range(5): 
        if resultLst[p][2] == 1: cntPositive += 1
    if cntPositive <= 2: resultPositive = 0
    print("Positive VS Negative(1:positive/0:negative) = {} VS {}\nRESULT : {}".format(cntPositive, 5 - cntPositive, resultPositive))
        
    
if __name__ == "__main__":
    #마지막 추가 인자가 들어오면 main을 시작하여 bigram, vectorize, textRepresentation진행/ 안들어오면 비슷한 댓글 찾기만
    if (len(sys.argv) == 3): mainStart()
    searchIdx = int(sys.argv[1])
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
    print(searchIdx)
    findSimDoc(searchIdx)