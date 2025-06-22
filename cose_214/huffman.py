class node:
      def __init__(self,freq,l=None,r=None):
    self.freq=freq
    self.l=None
    self.r=None
    self.code=''

def Extract_Min(queue):
  queue.sort(key=lambda x:x.freq)
  a=queue.pop(0)
  return a

def insert(queue,node):
  queue.append(node)

def huff(node,s,start=''):
  update=start+str(node.code)
  if(node.l)!=None:
    huff(node.l,s,update)
  if(node.r)!=None:
    huff(node.r,s,update)
  if(node.l==None and node.r==None):
    s[node.freq]=update



queue=[]
n=int(input())
for i in range(n):
  freq=int(input())
  queue.append(node(freq))
orique=queue[:]


for i in range(n-1):
  l=Extract_Min(queue)
  l.code=0
  r=Extract_Min(queue)
  r.code=1
  nn=node(l.freq+r.freq)
  nn.l=l
  nn.r=r
  insert(queue,nn)
answer={}
huff(queue[0],answer)
for i in range(n):
  print(answer.get(orique[i].freq))






