#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

###############################################################################
def word_count(filename):
    """ 단어 빈도 dictionary를 생성한다. (key: word, value: frequency)
    
    filename: input file
    return value: a sorted list of tuple (word, frequency) 
    """
    dic=dict()
    f=open(filename,'r')
    for string in f:
        string=string.rstrip()
        if string not in dic:
          dic[string]=1
        else:
          dic[string]=dic[string]+1
    newdict=sorted(dic.items())
    return newdict
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file", file=sys.stderr)
        sys.exit()

    result = word_count( sys.argv[1])

    # list of tuples
    for w, freq in result:
        print( "%s\t%d" %(w, freq))
