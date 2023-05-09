#include <stdlib.h> // malloc

#include "adt_dlist.h"

/* internal insert function
	inserts data into a new node
	return	1 if successful
			0 if memory overflow
*/
static int _insert( LIST *pList, NODE *pPre, void *dataInPtr){
	NODE *pNew;
	pNew=(NODE*)malloc(sizeof(NODE));
	if(pNew==NULL){
		return 0;
	}
	pNew->dataPtr=dataInPtr;
	pNew->llink=NULL;
	pNew->rlink=NULL;
	if(pPre==NULL){
		if(pList->count==0){
			pNew->llink=NULL;
			pNew->rlink=NULL;
			pList->rear=pNew;
		}
		else{
			pNew->rlink=pList->head;
			pList->head->llink=pNew;
		}
		pList->head=pNew;
	}
	else{
		
		if(pPre->rlink==NULL){	
			pList->rear=pNew;
			pPre->rlink=pNew;
			pNew->llink=pPre;
			pNew->rlink=NULL;		
			}
		else{
		pNew->llink=pPre;
		pNew->rlink=pPre->rlink;
		pPre->rlink->llink=pNew;
		pPre->rlink=pNew;
		}
	}
	(pList->count)++;
	//printf("%d\t%s\t%s\n",pList->count,pList->head->dataPtr->name,pList->rear->dataPtr->name);
	return 1;
}

/* internal delete function
	deletes data from a list and saves the (deleted) data to dataOut
*/
static void _delete( LIST *pList, NODE *pPre, NODE *pLoc, void **dataOutPtr){
		*(dataOutPtr)=pLoc->dataPtr;
		if(pPre==NULL){ 
			pList->head=pLoc->rlink;
			pLoc->rlink->llink=NULL;
		}
		else if(pLoc->rlink==NULL) {
			pList->rear=pPre;
			pPre->rlink=NULL;
		}
		else {
			pPre->rlink=pLoc->rlink;
			pLoc->rlink->llink=pPre;

		}
		free(pLoc);
		
		

		(pList->count)--;
}

/* internal search function
	searches list and passes back address of node
	containing target and its logical predecessor
	return	1 found
			0 not found
*/
static int _search( LIST *pList, NODE **pPre, NODE **pLoc, void *pArgu){
	int res;
	*pPre=NULL;
	*pLoc=pList->head;
	if(pList->count==0)return 0;
	int re;
	if((re=(*pList->compare)(pArgu,pList->rear->dataPtr))>0){
		*pPre=pList->rear;
		*pLoc=NULL;

		return 0;
	}
	while((res=(*pList->compare)(pArgu,(*pLoc)->dataPtr))>0){
		*pPre=*pLoc;
		*pLoc=(*pLoc)->rlink;
	}
	if(res==0) return 1;
	else return 0;
	
}


LIST *createList( int (*compare)(const void *, const void *)){
	LIST *newlist;
	newlist=(LIST *)malloc(sizeof(LIST));
	if(newlist){
		newlist->count=0;
		newlist->head=NULL;
		newlist->rear=NULL;
		newlist->compare=compare;
	}
}
/* Inserts data into list
	return	0 if overflow
			1 if successful
			2 if duplicated key
*/
int addNode( LIST *pList, void *dataInPtr, void (*callback)(const void *, const void *)){
	NODE *pPre;
		NODE *pLoc;
		int f;
		int in;
		f=_search(pList,&pPre,&pLoc,dataInPtr);
		if(f==1){
			callback(pLoc->dataPtr,dataInPtr);
			return 2;
		}
		in=_insert(pList,pPre,dataInPtr);
		if(in==0)return 0;

		return 1;
		
}

void traverseList( LIST *pList, void (*callback)(const void *)){
	NODE *cur;
	cur=pList->head;
	int i=1;
	while(i<=pList->count){
		callback(cur->dataPtr);
		cur=cur->rlink;
		i++;
	}
}

void traverseListR( LIST *pList, void (*callback)(const void *)){
	NODE *cur;
	cur=pList->rear;
	int i=1;
	while(i<=pList->count){
		callback(cur->dataPtr);
		cur=cur->llink;
		i++;
	}
}

void destroyList( LIST *pList, void (*callback)(void *)){
	NODE *delnode;
	if(pList){
		while(pList->count>0){
			delnode=pList->head;
			pList->head=pList->head->rlink;
			callback(delnode->dataPtr);
			free(delnode);
			(pList->count)--;
		}
		free(pList);
	}
}
int searchList( LIST *pList, void *pArgu, void **dataOutPtr){
	NODE *pPre;
	NODE *pLoc;
	int f;
	f=_search(pList,&pPre,&pLoc,pArgu);
	if(f==1){
	*(dataOutPtr)=pLoc->dataPtr;
	return 1;
	}
	return 0;
}

int removeNode( LIST *pList, void *keyPtr, void **dataOutPtr){
	NODE *pPre;
	NODE *pLoc;
	int f;
	f=_search(pList,&pPre,&pLoc,keyPtr);
	if(f==1){
		_delete(pList,pPre,pLoc,dataOutPtr);
		return 1;
	}
	return 0;
}

int countList( LIST *pList){
	return pList->count;
}