#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 복수의 빈도 파일을 병합하는 프로그램

import sys
import heapq

###############################################################################
def merge_k_sorted_freq(input_files):
    '''
    input_files : list of input filenames (frequency files; 2 column format)
    '''
    fins = []
    k = len(input_files)
    heap = []
    finished = [False for _ in range(k)] # [False] * k
    tups=[]
    for i in range(k):
        t=[]
        fins.append(open(input_files[i]))
        temp=[]
        for line in fins[i].readlines():
            temp=(line.split('\t'))
            temp[1]=int(temp[1].rstrip('\n'))
            temp.append(i)
            t.append(tuple(temp))    
        tups.append(t)

    for i in range(k):
        heapq.heapify(tups[i])
        heapq.heappush(heap, heapq.heappop(tups[i]))
    st=''
    a=0
    while False in finished:
        th=heapq.heappop(heap)
        if th[0]!=st :
            if st!='':
                print('%s\t%d' %(st, a))
            st=th[0]
            a=th[1]
        else:
            a+=th[1]
        
        if len(tups[th[2]])>0:    
            heapq.heappush(heap,heapq.heappop(tups[th[2]]))
        else:
            finished[th[2]]=True
             
    
        

    for i in range(k):
        fins[i].close()

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    merge_k_sorted_freq( sys.argv[1:])
