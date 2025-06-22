#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

_CHO_ = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
_JUNG_ = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
_JONG_ = 'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ' # index를 1부터 시작해야 함

# 겹자음 : 'ㄳ', 'ㄵ', 'ㄶ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ'
# 겹모음 : 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ'

_GYP_ = {
    ('ㄱ','ㅅ'):'ㄳ',
    ('ㄴ','ㅈ'):'ㄵ',
    ('ㄴ','ㅎ'):'ㄶ',
    ('ㄹ','ㄱ'):'ㄺ',
    ('ㄹ','ㅁ'):'ㄻ',
    ('ㄹ','ㅂ'):'ㄼ',
    ('ㄹ','ㅅ'):'ㄽ',
    ('ㄹ','ㅌ'):'ㄾ',
    ('ㄹ','ㅍ'):'ㄿ',
    ('ㄹ','ㅎ'):'ㅀ',
    ('ㅂ','ㅅ'):'ㅄ',
    ('ㅗ','ㅏ'):'ㅘ',
    ('ㅗ','ㅐ'):'ㅙ',
    ('ㅗ','ㅣ'):'ㅚ',
    ('ㅜ','ㅓ'):'ㅝ',
    ('ㅜ','ㅔ'):'ㅞ',
    ('ㅜ','ㅣ'):'ㅟ',
    ('ㅡ','ㅣ'):'ㅢ'
}
_JAMO2ENGKEY_ = {
 'ㄱ': 'r',
 'ㄲ': 'R',
 'ㄴ': 's',
 'ㄷ': 'e',
 'ㄸ': 'E',
 'ㄹ': 'f',
 'ㅁ': 'a',
 'ㅂ': 'q',
 'ㅃ': 'Q',
 'ㅅ': 't',
 'ㅆ': 'T',
 'ㅇ': 'd',
 'ㅈ': 'w',
 'ㅉ': 'W',
 'ㅊ': 'c',
 'ㅋ': 'z',
 'ㅌ': 'x',
 'ㅍ': 'v',
 'ㅎ': 'g',
 'ㅏ': 'k',
 'ㅐ': 'o',
 'ㅑ': 'i',
 'ㅒ': 'O',
 'ㅓ': 'j',
 'ㅔ': 'p',
 'ㅕ': 'u',
 'ㅖ': 'P',
 'ㅗ': 'h',
 'ㅘ': 'hk',
 'ㅙ': 'ho',
 'ㅚ': 'hl',
 'ㅛ': 'y',
 'ㅜ': 'n',
 'ㅝ': 'nj',
 'ㅞ': 'np',
 'ㅟ': 'nl',
 'ㅠ': 'b',
 'ㅡ': 'm',
 'ㅢ': 'ml',
 'ㅣ': 'l',
 'ㄳ': 'rt',
 'ㄵ': 'sw',
 'ㄶ': 'sg',
 'ㄺ': 'fr',
 'ㄻ': 'fa',
 'ㄼ': 'fq',
 'ㄽ': 'ft',
 'ㄾ': 'fx',
 'ㄿ': 'fv',
 'ㅀ': 'fg',
 'ㅄ': 'qt'
}
_ENGKEY2JAMO_={
 'r': 'ㄱ',
 'R': 'ㄲ',
 's': 'ㄴ',
 'e': 'ㄷ',
 'E': 'ㄸ',
 'f': 'ㄹ',
 'a': 'ㅁ',
 'q': 'ㅂ',
 'Q': 'ㅃ',
 't': 'ㅅ',
 'T': 'ㅆ',
 'd': 'ㅇ',
 'w': 'ㅈ',
 'W': 'ㅉ',
 'c': 'ㅊ',
 'z': 'ㅋ',
 'x': 'ㅌ',
 'v': 'ㅍ',
 'g': 'ㅎ',
 'k': 'ㅏ',
 'o': 'ㅐ',
 'i': 'ㅑ',
 'O': 'ㅒ',
 'j': 'ㅓ',
 'p': 'ㅔ',
 'u': 'ㅕ',
 'P': 'ㅖ',
 'h': 'ㅗ',
 'hk': 'ㅘ',
 'ho': 'ㅙ',
 'hl': 'ㅚ',
 'y': 'ㅛ',
 'n': 'ㅜ',
 'nj': 'ㅝ',
 'np': 'ㅞ',
 'nl': 'ㅟ',
 'b': 'ㅠ',
 'm': 'ㅡ',
 'ml': 'ㅢ',
 'l': 'ㅣ',
 'rt': 'ㄳ',
 'sw': 'ㄵ',
 'sg': 'ㄶ',
 'fr': 'ㄺ',
 'fa': 'ㄻ',
 'fq': 'ㄼ',
 'ft': 'ㄽ',
 'fx': 'ㄾ',
 'fv': 'ㄿ',
 'fg': 'ㅀ',
 'qt': 'ㅄ'
}

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
    code = (((cho * 21) + jung) * 28) + jong + 0xAC00

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
def jamo2engkey(str):
    an=''
    for word in str:
        if word in _JAMO2ENGKEY_:
            an=an+_JAMO2ENGKEY_[word]
        else:
            an=an+word
    return an
    
def engkey2jamo(str):
    ans=''
    for word in str:
        if word in _ENGKEY2JAMO_:
            ans=ans+_ENGKEY2JAMO_[word]
        else:
            ans=ans+word
    return ans

def jamo2syllable(str):
    i=0
    ans=''
    tmpcho=''
    tmpjung=''
    tmpjong=''
    for word in str:

        if i==0 and word in _CHO_:
            tmpcho=word
            i=1

        elif i==0 and word in _JUNG_:
            tmpjung=word
            i=1
            
        elif i==0 and word not in _JAMO2ENGKEY_:
            ans=ans+word
            tmpcho=''

        elif i==1 and word in _CHO_:

            if len(tmpjung)==0:
                ans=ans+tmpcho
                tmpcho=word
                i=1

            elif len(tmpjung)>=1:
                i=2
                tmpjong=tmpjong+word

        elif i==1 and word in _JUNG_:

            if len(tmpjung)==0:
                tmpjung=tmpjung+word

            elif len(tmpjung)==1:
                tmpjung=tmpjung+word
                if tuple(tmpjung) in _GYP_:
                    tmpjung=_GYP_[tuple(tmpjung)]
                    i=2
                else:
                    devi=tuple(tmpjung)
                    if tmpcho!='':
                        ans=ans+compose(_CHO_.find(tmpcho),_JUNG_.find(devi[0]),0)
                        ans=ans+devi[1]
                        tmpcho=''
                        tmpjung=''
                        i=0
                    elif tmpcho=='':
                        ans=ans+devi[0]
                        ans=ans+devi[1]
                        i=0
                        tmpjung=''
        

        elif i==1 and word not in _JAMO2ENGKEY_:
            
            if len(tmpjung)==0:
                ans=ans+tmpcho
                ans=ans+word
                tmpcho=''
                i=0
            
            elif len(tmpjung)>=1:
                if tmpcho=='':
                    ans=ans+tmpjung
                    tmpjung=''
                    i=0
                else:
                    ans=ans+compose(_CHO_.find(tmpcho),_JUNG_.find(tmpjung),0)
                    ans=ans+word
                    tmpcho=''
                    tmpjung=''
                    tmpjong=''
                    i=0
            
        elif i==2 and word in _CHO_:

            if len(tmpjong)==0:
                tmpjong=tmpjong+word
            
            elif len(tmpjong)==1:
                tmpjong=tmpjong+word
                if tuple(tmpjong) not in _GYP_:
                    devi=tuple(tmpjong)
                    ans=ans+compose(_CHO_.find(tmpcho),_JUNG_.find(tmpjung),_JONG_.find(devi[0])+1)
                    i=1
                    tmpcho=devi[1]
                    tmpjung=''
                    tmpjong=''
            
            elif len(tmpjong)==2:
                tmpjong=_GYP_[tuple(tmpjong)]
                ans=ans+compose(_CHO_.find(tmpcho),_JUNG_.find(tmpjung),_JONG_.find(tmpjong)+1)
                i=1
                tmpcho=word
                tmpjung=''
                tmpjong=''

        elif i==2 and word in _JUNG_:

            if len(tmpjong)==1:
                ans=ans+compose(_CHO_.find(tmpcho), _JUNG_.find(tmpjung),0)
                i=1
                tmpcho=tmpjong
                tmpjung=word
                tmpjong=''

            elif len(tmpjong)==2:
                devi=tuple(tmpjong)
                ans=ans+compose(_CHO_.find(tmpcho),_JUNG_.find(tmpjung),_JONG_.find(devi[0])+1)
                i=1
                tmpcho=devi[1]
                tmpjung=word
                tmpjong=''

        elif i==2 and word not in _JAMO2ENGKEY_:
            if tmpjong=='':
                ans=ans+compose(_CHO_.find(tmpcho),_JUNG_.find(tmpjung),0)
            else:
                ans=ans+compose(_CHO_.find(tmpcho),_JUNG_.find(tmpjung),_JONG_.find(tmpjong)+1)
            ans=ans+word
            i=0
            tmpcho=''
            tmpjung=''
            tmpjong=''
    if tmpcho=='':
        if tmpjung!='':
            ans=ans+tmpjung
    elif tmpcho!='':
        if tmpjung=='':
            ans=ans+tmpcho
        elif tmpjung!='':
            if tmpjong=='':
                ans=ans+compose(_CHO_.find(tmpcho),_JUNG_.find(tmpjung),0)
            elif len(tmpjong)==1:
                ans=ans+compose(_CHO_.find(tmpcho),_JUNG_.find(tmpjung),_JONG_.find(tmpjong)+1)
            elif len(tmpjong)==2:
                tmpjong=_GYP_[tuple(tmpjong)]
                ans=ans+compose(_CHO_.find(tmpcho),_JUNG_.find(tmpjung),_JONG_.find(tmpjong)+1)
    return ans

if __name__ == "__main__":
    
    i = 0
    line = sys.stdin.readline()

    while line:
        line = line.rstrip()
        i += 1
        print('[%06d:0]\t%s' %(i, line)) # 원문
    
        # 문자열을 자모 문자열로 변환 ('닭고기' -> 'ㄷㅏㄺㄱㅗㄱㅣ')
        jamo_str = str2jamo(line)
        print('[%06d:1]\t%s' %(i, jamo_str)) # 자모 문자열

        # 자모 문자열을 키입력 문자열로 변환 ('ㄷㅏㄺㄱㅗㄱㅣ' -> 'ekfrrhrl')
        key_str = jamo2engkey(jamo_str)
        print('[%06d:2]\t%s' %(i, key_str)) # 키입력 문자열
        
        # 키입력 문자열을 자모 문자열로 변환 ('ekfrrhrl' -> 'ㄷㅏㄹㄱㄱㅗㄱㅣ')
        jamo_str = engkey2jamo(key_str)
        print('[%06d:3]\t%s' %(i, jamo_str)) # 자모 문자열

        # 자모 문자열을 음절열로 변환 ('ㄷㅏㄹㄱㄱㅗㄱㅣ' -> '닭고기')
        syllables = jamo2syllable(jamo_str)
        print('[%06d:4]\t%s' %(i, syllables)) # 음절열

        line = sys.stdin.readline()


