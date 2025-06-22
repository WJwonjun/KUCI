class node:
  def __init__(self,name,pie=None,d=-1):
    self.name=name
    self.pie=None
    self.d=-1
    
def Extract_Min(q):
  q.sort(key=lambda x:x.d)
  for i in range(len(q)):
    if q[i].d>=0:
      a=q[i]
      del q[i]
      break
  return a

nodes=raw_input().split(',')
n=int(input())
q=[]
w=[]
for nod in nodes:
  q.append(node(nod))
q[0].d=0
s=[]
for i in range(n):
  w.append(tuple(raw_input().split(',')))

while len(q)>0:
  u=Extract_Min(q)
  s.append(u)
  for nod in q:
    for tup in w:
      if tup[0]==u.name and tup[1]==nod.name: #adj vertex?
        distance=int(tup[2])
        if nod.d>u.d+distance or nod.d==-1: #relax
          nod.d=u.d+distance
          nod.pie=u.name
for alp in nodes:
    for node in s:
      if alp==node.name:
        print(node.d)
        break
    






