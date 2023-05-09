#define SHOW_STEP 0 // 제출시 0
#define BALANCING 1 // 제출시 1

#include <stdlib.h>
#include <stdio.h>
#include <string.h> //strcmp, strdup

#define max(x, y)	(((x) > (y)) ? (x) : (y))

////////////////////////////////////////////////////////////////////////////////
// AVL_TREE type definition
typedef struct node
{
	char		*data;
	struct node	*left;
	struct node	*right;
	int			height;
} NODE;

typedef struct
{
	NODE	*root;
	int		count;  // number of nodes
} AVL_TREE;

////////////////////////////////////////////////////////////////////////////////
// Prototype declarations

/* Allocates dynamic memory for a AVL_TREE head node and returns its address to caller
	return	head node pointer
			NULL if overflow
*/
AVL_TREE *AVL_Create( void);

/* Deletes all data in tree and recycles memory
*/
void AVL_Destroy( AVL_TREE *pTree);
static void _destroy( NODE *root);

/* Inserts new data into the tree
	return	1 success
			0 overflow
*/
int AVL_Insert( AVL_TREE *pTree, char *data);

/* internal function
	This function uses recursion to insert the new data into a leaf node
	return	pointer to new root
*/
static NODE *_insert( NODE *root, NODE *newPtr);

static NODE *_makeNode( char *data);

/* Retrieve tree for the node containing the requested key
	return	address of data of the node containing the key
			NULL not found
*/
char *AVL_Retrieve( AVL_TREE *pTree, char *key);

/* internal function
	Retrieve node containing the requested key
	return	address of the node containing the key
			NULL not found
*/
static NODE *_retrieve( NODE *root, char *key);

/* Prints tree using inorder traversal
*/
void AVL_Traverse( AVL_TREE *pTree);
static void _traverse( NODE *root);

/* Prints tree using inorder right-to-left traversal
*/
void printTree( AVL_TREE *pTree);
/* internal traversal function
*/
static void _infix_print( NODE *root, int level);

/* internal function
	return	height of the (sub)tree from the node (root)
*/
static int getHeight( NODE *root);

/* internal function
	Exchanges pointers to rotate the tree to the right
	updates heights of the nodes
	return	new root
*/
static NODE *rotateRight( NODE *root);

/* internal function
	Exchanges pointers to rotate the tree to the left
	updates heights of the nodes
	return	new root
*/
static NODE *rotateLeft( NODE *root);

////////////////////////////////////////////////////////////////////////////////
int main( int argc, char **argv)
{
	AVL_TREE *tree;
	char str[1024];
	
	if (argc != 2)
	{
		fprintf( stderr, "Usage: %s FILE\n", argv[0]);
		return 0;
	}
	
	// creates a null tree
	tree = AVL_Create();
	
	 if (!tree)
	{
		fprintf( stderr, "Cannot create tree!\n");
		return 100;
	} 

	FILE *fp = fopen( argv[1], "rt");
	if (fp == NULL)
	{
		fprintf( stderr, "Cannot open file! [%s]\n", argv[1]);
		return 200;
	}

	while(fscanf( fp, "%s", str) != EOF)
	{

#if SHOW_STEP
		fprintf( stdout, "Insert %s>\n", str);
#endif		
		// insert function call
		AVL_Insert( tree, str);

#if SHOW_STEP
		fprintf( stdout, "Tree representation:\n");
		printTree( tree);
#endif
	}
	
	fclose( fp);
	
#if SHOW_STEP
	fprintf( stdout, "\n");

	// inorder traversal
	fprintf( stdout, "Inorder traversal: ");
	AVL_Traverse( tree);
	fprintf( stdout, "\n");

	// print tree with right-to-left infix traversal
	fprintf( stdout, "Tree representation:\n");
	printTree(tree);
#endif
	fprintf( stdout, "Height of tree: %d\n", tree->root->height);
	fprintf( stdout, "# of nodes: %d\n", tree->count);
	
	// retrieval
	char *key;
	fprintf( stdout, "Query: ");
	while( fscanf( stdin, "%s", str) != EOF)
	{
		key = AVL_Retrieve( tree, str);
		
		if (key) fprintf( stdout, "%s found!\n", key);
		else fprintf( stdout, "%s NOT found!\n", str);
		
		fprintf( stdout, "Query: ");
	}
	
	// destroy tree
	AVL_Destroy( tree);

	return 0;
}

AVL_TREE *AVL_Create( void){
	AVL_TREE *newtree;
	newtree=(AVL_TREE*)malloc(sizeof(AVL_TREE));
	newtree->root=NULL;
	newtree->count=0;
	return newtree;
}


int AVL_Insert( AVL_TREE *pTree, char *data){
	NODE *newnode;
	newnode=_makeNode(data);
	if(pTree->root==NULL){
		pTree->root=newnode;
		pTree->count++;
		return 1;
	}
	else {
		pTree->root=_insert(pTree->root,newnode);
		pTree->count++;
		return 1;
	}
	return 0;
}

static NODE *_insert( NODE *root, NODE *newPtr){
	if(root==NULL) return newPtr;


	if( strcmp(newPtr->data,root->data)<0 ){
			root->left=_insert(root->left,newPtr);					
	}
	
	else{
			root->right=_insert(root->right,newPtr);
	}	
				
	root->height=getHeight(root);

	int balance=0;
	balance=getHeight(root->left)-getHeight(root->right);


	if( balance >1 ){
		if( strcmp( newPtr->data , root->left->data )<0 ) //ll
			return rotateRight(root);


		else if(strcmp( newPtr->data , root->left->data )>0){  //lr
			root->left = rotateLeft(root->left);
			return rotateRight(root);
		}

	}


	else if( balance <-1 ){
		if(strcmp( newPtr->data, root->right->data)>0) //rr
			return rotateLeft(root);

		else if(strcmp( newPtr->data, root->right->data)<0){ //rl
			root->right= rotateRight(root->right);
			return rotateLeft(root);
		}

	}
	return root;
}

static NODE *_makeNode( char *data){
	NODE *newnode;
	newnode=(NODE *)malloc(sizeof(NODE));
	newnode->data=strdup(data);
	newnode->left=NULL;
	newnode->right=NULL;
	newnode->height=1;
	return newnode;
}
static int getHeight( NODE *root){
	if(root==NULL) return 0;
	if(root->left==NULL && root->right==NULL) return 1;
	else if(root->left!=NULL){
		if(root->right!=NULL)return 1+max((root->left->height),(root->right->height));
		else return 1+root->left->height;
	}
	else return 1+root->right->height;
	
}


static void _infix_print( NODE *root, int level){
	if(root!=NULL){
		if(root->right!=NULL)_infix_print(root->right,level+1);
		for(int i=0;i<level;i++){
			printf("\t");
		}
		printf("%s\n",root->data);
		if(root->left!=NULL)_infix_print(root->left,level+1);
	}
}


void printTree(AVL_TREE *pTree){
	if(pTree->root!=NULL)_infix_print(pTree->root,0);
}


static NODE *rotateRight( NODE *root){
	NODE *x1=root->left;
	NODE *x2=x1->right;
	x1->right=root;
	root->left=x2;

	root->height=getHeight(root);
	x1->height=getHeight(x1);
	
	return x1;
}


static NODE *rotateLeft( NODE *root){
	NODE *x1=root->right;
	NODE *x2=x1->left;
	x1->left=root;
	root->right=x2;

	root->height=getHeight(root);
	x1->height=getHeight(x1);
	return x1;
	}


static NODE *_retrieve( NODE *root, char *key){
	NODE *temp=root;
	while(strcmp(temp->data,key)!=0){
		if(strcmp(temp->data,key)<0){
			if(temp->right!=NULL)temp=temp->right;
			else return NULL;
		}
		else if(strcmp(temp->data,key)>0){
			if(temp->left!=NULL)temp=temp->left;
			else return NULL;
	}
	}
	return temp;
}


char *AVL_Retrieve( AVL_TREE *pTree, char *key){
	NODE* find;
	if(pTree->root==NULL)return NULL;
	if((find=_retrieve(pTree->root,key))!=NULL)return (find->data);
	else return NULL;
	
}


static void _destroy( NODE *root){		
		if(root==NULL)return;
		_destroy(root->left);
		_destroy(root->right);
		free(root->data);
		free(root);
}


void AVL_Destroy( AVL_TREE *pTree){
	if(pTree->root!=NULL)_destroy(pTree->root);
	free(pTree);
}


void AVL_Traverse( AVL_TREE *pTree){
	if(pTree->root!=NULL)_traverse(pTree->root);
}


static void _traverse( NODE *root){
	if(root!=NULL){
		if(root->left!=NULL)_traverse(root->left);
		printf("%s ",root->data);
		if(root->right!=NULL)_traverse(root->right);
	}
}

