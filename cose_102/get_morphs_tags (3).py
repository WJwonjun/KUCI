#!/usr/bin/env python3
# coding: utf-8

import sys

def get_morphs_tags(tagged):
    a=1
    while a==1:
        for i in range(len(tagged)):
            if tagged[i]=='+' and tagged[i+1]=='+':
                tagged=tagged[:i]+' '+tagged[i+1:]
                continue
        a=0
    b=1
    while b==1:
        for i in range(1,len(tagged)):
            if tagged[i]=='+' and tagged[i-1]!=' ':
                tagged=tagged[:i]+' '+tagged[i+1:]
                continue
        b=0
    tmp=tagged.split(' ')
    ans=[]
    for i in tmp:
        for j in range(len(i)):
            if i[j]=='/' and i[j+1]=='/':
                list=['/',i[j+2:]]
                ans.append(tuple(list))
                break
            elif i[j]=='/' and i[j+1]!='/':
                ans.append(tuple(i.split(i[j])))
                break
    return ans



###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as fin:

        for line in fin.readlines():

            # 2 column format
            segments = line.split('\t')

            if len(segments) < 2: 
                continue

            # result : list of tuples
            result = get_morphs_tags(segments[1].rstrip())
        
            for morph, tag in result:
                print(morph, tag, sep='\t')
