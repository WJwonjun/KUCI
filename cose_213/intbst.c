#include <stdlib.h> // malloc, atoi, rand
#include <stdio.h>
#include <assert.h>
#include <time.h> // time

#define RANDOM_INPUT	1
#define FILE_INPUT		2

////////////////////////////////////////////////////////////////////////////////
// TREE type definition
typedef struct node
{
	int			data;
	struct node	*left;
	struct node	*right;
} NODE;

typedef struct
{
	NODE	*root;
} TREE;

////////////////////////////////////////////////////////////////////////////////
// Prototype declarations

/* Allocates dynamic memory for a tree head node and returns its address to caller
	return	head node pointer
			NULL if overflow
*/
TREE *BST_Create( void){
	TREE *newtree;
	newtree=(TREE*)malloc(sizeof(TREE));
	newtree->root=NULL;
	return newtree;
}

/* Deletes all data in tree and recycles memory
*/
static void _destroy( NODE *root){		
		if((root->left==NULL)&&(root->right==NULL)){
			free(root);
			return;
		}
		else if(root->left!=NULL){
			_destroy(root->left);
		}
		else if(root->right!=NULL){
			_destroy(root->right);
		}	
}

void BST_Destroy( TREE *pTree){
	if(pTree->root!=NULL)_destroy(pTree->root);
	free(pTree);
}
/* internal function (not mandatory)
*/

/* Inserts new data into the tree
	return	1 success
			0 overflow
*/
NODE* _makeNode( int data){
	NODE* newnode;
	newnode=(NODE*)malloc(sizeof(NODE));
	newnode->data=data;
	newnode->left=NULL;
	newnode->right=NULL;
	return newnode;
}
static void _insert( NODE *root, NODE *newPtr){
	if(root->data<=newPtr->data){
		if(root->right!=NULL) _insert(root->right,newPtr);
		else root->right=newPtr;
	}
	else{
		if(root->left!=NULL) _insert(root->left,newPtr);
		else root->left=newPtr;
	}
}

int BST_Insert( TREE *pTree, int data){
	NODE* newnode;
	newnode=_makeNode(data);
	if(pTree->root==NULL){
		pTree->root=newnode;
		return 1;
	}
	else{
	_insert(pTree->root,newnode);
	return 1;
	}
	return 0;
}

/* internal function (not mandatory)
*/

static NODE *_delete( NODE *root, int dltKey, int *success){
	NODE* temp=NULL;
	if(root==NULL)return NULL;

	if(root->data>dltKey){
			if(root->left==NULL){
				*success=0;
				return root;
			}
			root->left=_delete(root->left,dltKey,success);
			
		}
	else if(root->data<dltKey){
			if(root->right==NULL){
				*success=0;
				return root;
			}
			root->right=_delete(root->right,dltKey,success);
	}
	else{ 
        if(root->right!=NULL && root->left!=NULL)
        {
            temp = root->right;
			while(temp->left!=NULL){
				temp=temp->left;
			}
            root->data = temp->data;
            root->right=_delete(root->right, temp->data,success);
        }
        else
        {
            temp = (root->left==NULL) ? root->right : root->left;
            free(root);
			(*success)=1;
            return temp;
        }
    

    
}
return root;
}

/* Deletes a node with dltKey from the tree
	return	1 success
			0 not found
*/
int BST_Delete( TREE *pTree, int dltKey){
	int success;	
	pTree->root=_delete(pTree->root,dltKey,&success);
	if(success)return 1;
	else return 0;
}

/* internal function
	success is 1 if deleted; 0 if not
	return	pointer to root
*/
/* Retrieve tree for the node containing the requested key
	return	address of data of the node containing the key
			NULL not found		
*/
static NODE *_retrieve( NODE *root, int key){
	NODE *temp=root;
	while(temp->data!=key){
		if(temp->data<key){
			if(temp->right!=NULL)temp=temp->right;
			else return NULL;
		}
		else if(temp->data>key){
			if(temp->left!=NULL)temp=temp->left;
			else return NULL;
	}
	}
	return temp;
}
int *BST_Retrieve( TREE *pTree, int key){
	NODE* find;
	if(pTree->root==NULL)return NULL;
	if((find=_retrieve(pTree->root,key))!=NULL)return &(find->data);
	else return NULL;
	
}

/* internal function
	Retrieve node containing the requested key
	return	address of the node containing the key
			NULL not found
*/


/* prints tree using inorder traversal
*/
static void _traverse( NODE *root){
	if(root!=NULL){
		if(root->left!=NULL)_traverse(root->left);
		printf("%d ",root->data);
		if(root->right!=NULL)_traverse(root->right);
	}
}

void BST_Traverse( TREE *pTree){
	if(pTree->root!=NULL)_traverse(pTree->root);
}

/* Print tree using inorder right-to-left traversal
*/
static void _inorder_print( NODE *root, int level){
	if(root!=NULL){
		if(root->right!=NULL)_inorder_print(root->right,level+1);
		for(int i=0;i<level;i++){
			printf("\t");
		}
		printf("%d\n",root->data);
		if(root->left!=NULL)_inorder_print(root->left,level+1);
	}
}

void printTree( TREE *pTree){
	if(pTree->root!=NULL)_inorder_print(pTree->root,0);
}
/* internal traversal function
*/


/* 
	return 1 if the tree is empty; 0 if not
*/
int BST_Empty( TREE *pTree){
	if(pTree->root==NULL){
		return 1;
	}
	else{
		return 0;
	} 
}



int main( int argc, char **argv)
{
	int mode; // input mode
	TREE *tree;
	int data;
	
	if (argc != 2)
	{
		fprintf( stderr, "usage: %s FILE or %s number\n", argv[0], argv[0]);
		return 1;
	}
	
	FILE *fp;
	
	if ((fp = fopen(argv[1], "rt")) == NULL)
	{
		mode = RANDOM_INPUT;
	}
	else mode = FILE_INPUT;
	
	// creates a null tree
	tree = BST_Create();
	
	if (!tree)
	{
		printf( "Cannot create a tree!\n");
		return 100;
	}

	if (mode == RANDOM_INPUT)
	{
		int numbers;
		numbers = atoi(argv[1]);
		assert( numbers > 0);

		fprintf( stdout, "Inserting: ");
		
		srand( time(NULL));
		for (int i = 0; i < numbers; i++)
		{
			data = rand() % (numbers*3) + 1; // random number (1 ~ numbers * 3)
			
			fprintf( stdout, "%d ", data);
			
			// insert function call
			int ret = BST_Insert( tree, data);
			if (!ret) break;
		}
	}
	else if (mode == FILE_INPUT)
	{
		fprintf( stdout, "Inserting: ");
		
		while (fscanf( fp, "%d", &data) != EOF)
		{
			fprintf( stdout, "%d ", data);
			
			// insert function call
			int ret = BST_Insert( tree, data);
			if (!ret) break;
		}
		fclose( fp);
	}
	
	fprintf( stdout, "\n");

	if (BST_Empty( tree))
	{
		fprintf( stdout, "Empty tree!\n");
		BST_Destroy( tree);
		return 0;
	}	

	// inorder traversal
	fprintf( stdout, "Inorder traversal: ");
	BST_Traverse( tree);
	fprintf( stdout, "\n");
	
	// print tree with right-to-left inorder traversal
	fprintf( stdout, "Tree representation:\n");
	printTree(tree);
	
	while (1)
	{
		fprintf( stdout, "Input a number to delete: "); 
		int num;
		if (scanf( "%d", &num) == EOF) break;
		
		int ret = BST_Delete( tree, num);
		if (!ret)
		{
			fprintf( stdout, "%d not found\n", num);
			continue;
		}
		
		// print tree with right-to-left inorder traversal
		fprintf( stdout, "Tree representation:\n");
		printTree(tree);
		
		if (BST_Empty( tree))
		{
			fprintf( stdout, "Empty tree!\n");
			break;
		}
	}
	
	BST_Destroy( tree);

	return 0;
}

