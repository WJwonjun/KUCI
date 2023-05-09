def find_cross_max_array(list,low,mid,high):
    left_sum=0
    right_sum=0
    sum=0
    for i in range (mid,low-1,-1) :
        sum=sum+list[i]
        if sum > left_sum or i==mid:
            left_sum=sum
            max_left=i
    sum=0
    for j in range(mid+1,high+1):
        sum=sum+list[j]
        if sum>right_sum or j==mid+1:
            right_sum=sum
            max_right=j
    return(max_left,max_right,left_sum+right_sum)
    
def find_max_array(list,low,high):
    if high==low :
        return low,high,list[low]
    else :
        mid=(low+high)//2
        (left_low,left_high,left_sum)=find_max_array(list, low, mid)
        (right_low,right_high,right_sum)=find_max_array(list,mid+1,high)
        (cross_low,cross_high,cross_sum)=find_cross_max_array(list,low,mid,high)
        if left_sum>=right_sum and left_sum>=cross_sum :
            return (left_low,left_high,left_sum)
        elif right_sum>=left_sum and right_sum>=cross_sum :
            return (right_low,right_high,right_sum)
        else :
            return (cross_low,cross_high,cross_sum)
def main():
  n=int(input())
  list=[]
  for k in range(0,n):
    list.append(int(input()))
  a,b,c=find_max_array(list,0,n-1)
  print(a)
  print(b)
  print(c)

main()