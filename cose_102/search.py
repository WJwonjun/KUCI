#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle

def print_html_header(query):
    print('''<!DOCTYPE html>
<html lang="ko">
\t<head>
\t\t<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
\t\t<title>용례검색 결과 (%s)</title>
\t</head>
\t<body>''' % query)

###############################################################################
def print_html_footer():
    print('''\t</body>
</html>''')

###############################################################################
def get_highlight(query, sentence):
    """ 문장(sentence)에서 query에 포함된 단어를 하이라이트 처리('<font color="blue"><b>...</b></font>')한 문자열을 출력
    query : 사용자 쿼리
    sentence : 문장
    return value : highlighted sentece
    """
    a=query.split(' ')
    for word in a:
            sentence=sentence.replace(word,'<font color="blue"><b>'+word+'</b></font>')

    return sentence
###############################################################################
def search( inverted_indexing, sentences, query):
    """ 사용자 쿼리를 받아 용례 검색 결과(문장)를 출력
    inverted_indexing : 역색인 dictionary (key : index term, value : set of sentences)
    sentences : 색인된 문장 리스트
    query : 사용자 쿼리 (둘 이상의 단어가 포함된 쿼리는 각 단어의 용례 문장들의 교집합을 구해야 함)
    return value: 검색된 문장 (번호) 리스트 (문장 번호 순)
    """
    a=[]
    a=query.split(' ')
    ans=set()
    tr=0
    for word in a:
        if tr==0:
            ans=inverted_indexing[word]
        else:
            ans= ans & inverted_indexing[word]
        tr+=1
    return ans

###############################################################################
if __name__ == "__main__":

    with open("index.pickle","rb") as fin:
        inverted_indexing, sentences = pickle.load(fin)
    
    print('\n검색할 단어를 입력하세요(type "^D" to exit): ', file=sys.stderr)
    query = sys.stdin.readline().rstrip()

    if not query:
        sys.exit()

    # HTML header
    print_html_header(query)

    # 용례 검색
    snts = search( inverted_indexing, sentences, query)

    # 용례 출력
    if len(snts):
        print('\t\t%d 개의 문장<br>' % len(snts))
        print('\t\t<table border="1" cellspacing="0" bordercolor="lightgrey">')
        for i, snt_index in enumerate(snts):
            hight_snt = get_highlight(query, sentences[snt_index])
            print('\t\t\t<tr><td width="30">%d</td><td>%s</td>' %(i+1, hight_snt))
        print('\t\t</table>')
    else:
        print("결과가 없습니다.")
    
    # HTML footer    
    print_html_footer()
