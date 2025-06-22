#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

_CHO_ = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
_JUNG_ = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
_JONG_ = "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ" # index를 1부터 시작해야 함

###############################################################################
def is_hangeul_syllable(ch):
    '''한글 음절인지 검사
    '''
    if not isinstance(ch, str):
        return False
    elif len(ch) > 1: 
        ch = ch[0]
    
    return 0xAC00 <= ord(ch) <= 0xD7A3

###############################################################################
def compose(cho, jung, jong):
    '''초성, 중성, 종성을 한글 음절로 조합
    cho : 초성
    jung : 중성
    jong : 종성
    return value: 음절
    '''
    if not (0 <= cho <= 18 and 0 <= jung <= 20 and 0 <= jong <= 27):
        return None
    code = (((cho * 21) + jung) * 28) + jong + 0xAC00 #'가'

    return chr(code)

###############################################################################
# input: 음절
# return: 초, 중, 종성
def decompose(syll):
    '''한글 음절을 초성, 중성, 종성으로 분해
    syll : 한글 음절
    return value : tuple of integers (초성, 중성, 종성)
    '''
    if not is_hangeul_syllable(syll):
        return (None, None, None)
    
    uindex = ord(syll) - 0xAC00
    
    jong = uindex % 28
    jung = ((uindex - jong) // 28) % 21
    cho = ((uindex - jong) // 28) // 21

    return (cho, jung, jong)

###############################################################################
def str2jamo(str):
    '''문자열을 자모 문자열로 변환
    '''
    jamo = []
    for ch in str:
        if is_hangeul_syllable(ch):
            cho, jung, jong = decompose(ch)
            jamo.append( _CHO_[cho])
            jamo.append( _JUNG_[jung])
            if jong != 0:
                jamo.append( _JONG_[jong-1])
        else:
            jamo.append(ch)
    return ''.join(jamo)

###############################################################################
def str2chostr(str):
    '''문자열을 초성 문자열로 변환
    한글음절이 아니면 해당 문자를 그대로 사용
    '''
    strtocho=[]
    for ch in str:
        if is_hangeul_syllable(ch):
            cho,jung,jong=decompose(ch)
            strtocho.append( _CHO_[cho])
        else:
            strtocho.append(ch)
    return ''.join(strtocho)

###############################################################################
def chosung_indexing(cho_indexing, filename):
    '''초성 색인
    cho_indexing : dictionary of indexed result (key : 초성문자열, value : a list of tuples (단어, 빈도))
                    리스트는 단어 빈도의 내림차순으로 정렬되어야 함 (빈도가 같은 경우 문자열 순으로 정렬)
    filename : input filename (frequency file)
    '''
    
    f=open(filename,'r')
    for line in f.readlines():
        segments=(line.split('\t'))
        segments[1]=int(segments[1].rstrip('\n'))
        segcho=str2chostr(segments[0])
        segments=tuple(segments)
        if segcho not in cho_indexing:
            cho_indexing[segcho]=[]
        cho_indexing[segcho].append(segments)
    for key in cho_indexing:
        cho_indexing[key].sort(key=lambda x: (-int(x[1]),x[0]),reverse=False)












###############################################################################
def print_list(t):
    for w, f in t:
        print('\t%s\t%d' %(w, f))

###############################################################################
if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file", file=sys.stderr)
        sys.exit()

    # 초성 색인용 dictionary
    cho_indexing = {}

    # 초성 색인
    chosung_indexing(cho_indexing, sys.argv[1])
    
    while True:
        query = input('검색할 단어의 초성을 입력하세요(type "exit" to exit): ')

        if query == "exit":
            break
        
        if query in cho_indexing:
            print_list(cho_indexing[query])
        else:
            print("결과가 없습니다.")
