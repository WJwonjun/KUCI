def maxheapify(list,i,aheapsize):
      l=i*2
  r=i*2+1
  largest=i
  if l<=aheapsize and list[l]>list[largest]:
    largest=l
  if r<=aheapsize and list[r]>list[largest]:
    largest=r 
  if largest!=i:
    list[i],list[largest]=list[largest],list[i]
    return maxheapify(list,largest,aheapsize)

def heapsort(list):
  aheapsize=len(list)-1
  for i in range((aheapsize//2),0,-1):
    maxheapify(list,i,aheapsize)
  for k in range((len(list)-1),1,-1):
    list[1],list[k]=list[k],list[1]
    maxheapify(list,1,k-1)
def main():
  n=int(input())
  list=[]
  for i in range(0,n):
    list.append(int(input()))
  list=[0]+list
  heapsort(list)
  for k in range(1,n+1):
    print(list[k])

main()