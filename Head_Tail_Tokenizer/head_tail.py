# -*- coding: utf-8 -*-
from konlpy.utils import pprint
from konlpy.tag import Mecab
import sys 

#조사 어미 접미사 목록 추출
def getJoEomiSuffixList(file_name):
	mecab = Mecab()
	f = open(file_name, 'r', encoding='utf-8')
	JESary = [[],[],[]] #JESary[0] = jo, JESary[1] = eomi, JESary[2] = suffix
	jo = ['JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKQ', 'JX' ,'JC'] #JKV 제외, 조사
	eomi = ['EF', 'ETN','ETM'] #어미(연결어미, 선어말어미 제외)
	suffix = ['XSN', 'XSV', 'XSA'] #접미사

	while(True): 
		line = f.readline() #한줄씩 읽어들임
		if len(line) == 0: break #더이상 들어오지 않으면 종료
		token = mecab.pos(line)
		for i in token: #('??', 'JKS + EP') 이런식으로 들어옴			
			#JKS+EP 를 분해 ex ) ('??', 'JKS + 'EP') => ('??', 'JKS'), ('??', 'EP')
			tmpAry = i[1].split('+') #tmpAry = ['JKS', 'EP']
			for t in tmpAry: 
				#각각 해당되면 해당 리스트에 append
				if (t in jo and i[0] not in JESary[0]): JESary[0].append(i[0])
				elif (t in eomi and i[0] not in JESary[1]): JESary[1].append(i[0])
				elif (t in suffix and i[0] not in JESary[2]): JESary[2].append(i[0])

	f = open('JESList.txt', 'w')

	#빠른 test를 위해 output 파일 작성
	for l in JESary:
		for w in l: 
			w = w + ' '
			f.write(w)
		f.write('\n')
	f.close()
	return JESary

#word분해
def splitWord(word, JESary):
	flag = 0 #분해 되지 않는경우

	#해당단어를 처음부터 슬라이싱해서 분해
	for i in range(len(word)):
		if (word[i] in JESary[0] or word[i] in JESary[1] or word[i:] in JESary[2]):
			flag = 1
			if (i == 0): print('{}/head'.format(word))
			else:
				if (word[i] in JESary[0]): print('{}/head + {}/tail_Josa'.format(word[:i],word[i:]))
				if (word[i] in JESary[1]): print('{}/head + {}/tail_Eomi'.format(word[:i],word[i:]))
				if (word[i:] in JESary[2]): print('{}/head + {}/tail_suffix'.format(word[:i],word[i:]))

	if flag == 0: print('{}/head'.format(word))

if __name__ == "__main__":
	Tag = []
	if (len(sys.argv) == 2):
		fileName = sys.argv[1]
		f = open(fileName, 'r', encoding='utf-8')
		line = f.readlines()
		for i in line:
			Tag.append(i.split())
	else:
		fileName = "./ko_wiki_text_EUCKR.txt"
		Tag = getJoEomiSuffixList(fileName) #조사, 어미, 접미사 목록 추출
	#----------------------------------
	#입력 어절 조사/어미 분리
	while (True): 
		word = input("Input(If 0 is Stop) >> ")
		if (word == '0'): break
		answer = splitWord(word, Tag)
		print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
