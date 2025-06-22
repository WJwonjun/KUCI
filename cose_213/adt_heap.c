#include <stdio.h>
#include <stdlib.h> // malloc, realloc

#include "adt_heap.h"

/* Reestablishes heap by moving data in child up to correct location heap array
*/
static void _reheapUp( HEAP *heap, int index){
        void* temp=(heap->heapArr)[index];
  while((index>0) && (((heap->compare)(temp,(heap->heapArr)[(index-1)/2]))>0)){
        (heap->heapArr)[index]=(heap->heapArr)[(index-1)/2];
        index=(index-1)/2;
  }
  
  (heap->heapArr)[index]=temp;
}


/* Reestablishes heap by moving data in root down to its correct location in the heap
*/
static void _reheapDown( HEAP *heap, int index){
    int child;
    if(heap->last==(index*2+1))child=(index*2+1);
    else if(heap->last<(index*2+1))return;
    else{
    if((heap->compare)((heap->heapArr)[index*2+1],(heap->heapArr)[(index+1)*2])>0)child=(index*2+1);
    else child=((index+1)*2);
}
    if((heap->compare)((heap->heapArr)[index],(heap->heapArr)[child])<0){
    void* temp=(heap->heapArr)[index];
    heap->heapArr[index]=heap->heapArr[child];
    heap->heapArr[child]=temp;
    return _reheapDown(heap,child);
    }
    else return;
}

HEAP *heap_Create( int capacity, int (*compare) (void *arg1, void *arg2)){
    HEAP* newheap;
    newheap=(HEAP*)malloc(sizeof(HEAP));
    void* arr=(void *)malloc(sizeof(void *) * capacity);
    (newheap->heapArr)=arr;
    newheap->last=-1;
    newheap->capacity=capacity;
    newheap->compare=compare;
    return newheap;
}

int heap_Insert( HEAP *heap, void *dataPtr){
    
    if(((heap->last)+1)==heap->capacity){
        heap->capacity=(heap->capacity)*2;
        heap->heapArr=(void*)realloc((heap->heapArr),sizeof(void*)*(heap->capacity));    
    }
    (heap->last)++;
    (heap->heapArr)[(heap->last)]=dataPtr;
    
   _reheapUp(heap,heap->last);
    
}

void heap_Print( HEAP *heap, void (*print_func) (void *data)){
   for(int i=0;i<=(heap->last);i++){
        print_func((heap->heapArr)[i]);
    }
    printf("\n");
}

int heap_Empty(  HEAP *heap){
    if(heap->last==-1)return 1;
    else return 0;
}

int heap_Delete( HEAP *heap, void **dataOutPtr){
    *dataOutPtr=(heap->heapArr)[0];
    (heap->heapArr)[0]=(heap->heapArr)[heap->last];
    _reheapDown(heap,0);
    heap->last--;
}


void heap_Destroy( HEAP *heap){
    while((heap->last)>-1){
        free(heap->heapArr[heap->last]);
        (heap->last)--;
    }
    free(heap->heapArr);
    free(heap);
}