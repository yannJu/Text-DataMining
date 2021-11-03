#-*-coding:utf-8-*-
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
#import random

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
def vectorize(lines, op = 0):
    vector = TfidfVectorizer()
    X = vector.fit_transform(lines)
    if op == 1: return X.todok(), vector
    return X.todok()

def makeTextRepresentation(output, vector, target, op = 0, tfIdf = None):
    wordLength = -1
    if (op == 1): 
        wordF = open('word.txt', 'w', encoding='utf-8')
        wordLst = []
    textRepresent = ["{} ".format(i) for i in target]
    for v in vector.items():
        key = v[0]
        val = v[1]
        textRepresent[key[0]] += "{}:{} ".format(key[1], val)
        wordLength = max(wordLength, key[1])
                                   
    for t in textRepresent: output.write(t + "\n")
    output.close()
    
    if op == 1: 
        for f in range(wordLength): wordF.write(tfIdf.get_feature_names()[f] + "\n")
        print("WordList Done-")
        wordF.close()

def mainStart(option = None):
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

    #dict type : {key-tuple():value-float)
    trainVector, trainTFIDF = vectorize(lines_train, 1)
    print("TrainSet Vectorize Done-")
    testVector = vectorize(lines_test)
    print("TestSet Vectorize Done-")

    v_train.close()
    v_test.close()  
    
    #SVM format으로 TextRepresentation
    if option != 1: makeTextRepresentation(wv_train, trainVector, trainTarget)
    else: makeTextRepresentation(wv_train, trainVector, trainTarget, 1, trainTFIDF)
    print("TrainSet TextRepresentation Done-")
    makeTextRepresentation(wv_test, testVector, testTarget)
    print("TestSet TextRepresentation Done-")

def findSimDoc(search):
        #----------------print Test Comment
    tRf = open('ratings_test.txt', 'r', encoding='utf-8') #test Comment 
    testComment = tRf.readlines()[search]
    tRfSplit = testComment.split()
    wordIdx = len(tRfSplit[0])
    comment = testComment[wordIdx + 1:-3]
    print("Search Comment : ", comment)
    
    #----------------file open (bigram testComment, SVM train Set, WordList)
    testTRf = open('output_Optimal_test.txt', 'r', encoding='utf-8') #test Comment 
    trainTRf = open('output_TextRepresentation_train.txt', 'r', encoding='utf-8')  #trainText Representation
    trainCmtf = open('ratings_train.txt', 'r', encoding='utf-8') #train Comment
    wordf = open('word.txt', 'r', encoding='utf-8') #word List
    
    #----------------search Comment Bigram Doc split
    searchBigramLine = testTRf.readlines()[search - 1] #feature
    searchBigramLine = searchBigramLine.split()
    searchWordIdx = []#feature Idx Lst
    #----------------search Comment Bigram Doc split
    trainLines = trainTRf.readlines() #train SVM  Set
    trainCmt = trainCmtf.readlines()[1:] #train Comment List
    word = wordf.readlines() #wordList
    for x in range(len(word)): word[x] = word[x][:-1]
    #----------------variable
    resultAry = [] 
    minidx = 0 #resultAry의 최소 유사도를 가진 값의 인덱스
    cntPositive = 0 # 1(positive)인 수를 cnt
    resultPositive =  1
    
    #trainComment Doc 분리
    for l in range(len(trainCmt)):
        tmp = trainCmt[l].split()
        idIdx = len(tmp[0])
        trainCmt[l] = trainCmt[l][idIdx:-3]
    
    # feature가 있는 경우를 찾음
    for i in searchBigramLine:
        try:
            idx = word.index(i)
            searchWordIdx.append(idx)
        except ValueError:
            continue
    #Train Text Representaion탐색
    for t in range(len(trainLines)):
        similarity = 0  #유사도 계산을 위한 변수
        tmp = trainLines[t].split() 
        target = int(tmp[0])
        #TextRepresentation 에서 bigram 된 test Comment를 탐색하여 유사도 계산
        for j in range(1, len(tmp)):
            fandval = tmp[j].split(':')
            feature = int(fandval[0])
            val = float(fandval[1])
            if feature in searchWordIdx: 
                similarity += val
        if (len(resultAry) < 5): resultAry.append((similarity, t, target))
        else:
            if ((similarity > resultAry[minidx][0]) or (-0.3 <= similarity - resultAry[minidx][0] and target == resultAry[minidx][2])):
                resultAry[minidx] = (similarity, t, target)
        resultAry = sorted(resultAry, key = lambda x:x[0]) #정렬을 통해 min값이 0번째에 오도록 함
    
    print("-------------------------------------------------------")
    for r in range(len(resultAry) - 1, -1, -1): print("댓글({}) -> {}\n 유사도 : {} Positive? : {}\nIDX : {}".format(len(resultAry) - r, trainCmt[resultAry[r][1]], resultAry[r][0], resultAry[r][2], resultAry[r][1]))
    print("-------------------------------------------------------")
    for p in range(5): 
        if resultAry[p][2] == 1: cntPositive += 1
    if cntPositive <= 2: resultPositive = 0
    print("Positive VS Negative(1:positive/0:negative) = {} VS {}\nRESULT : {}".format(cntPositive, 5 - cntPositive, resultPositive))
                                                  
    testTRf.close()
    trainTRf.close()
    trainCmtf.close()
    wordf.close()
    
if __name__ == "__main__":
    if len(sys.argv) == 3: mainStart(sys.argv[2]) #mainStart()를 통해 token, textRepresentation, wordList(argv[2] == 1인경우만)생성
    searchIdx = int(sys.argv[1])
    # searchIdxLst = [random.randrange(1, 50001) for x in range(20)]
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
    print(searchIdx)
    findSimDoc(searchIdx)
    # for i in searchIdxLst:
    #     print(i)
    #     findSimDoc(i)