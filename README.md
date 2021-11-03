# TextMining
1. **Head-Tail Tokenizer**
        
    -  주어진 텍스트 파일을 형태소 분석하여 Head-Tail을 구분
2. **Text Representation**
  
   - 주어진 train set을 bigram단위로 token화 하고 tf-idf유사도를 구함
   -  선택한 test set comment와 가장 흡사한 train set 상위 5개를 출력