import numpy as np
import sys,os
sys.path.append(pardir)
from common.functions import softmax,cross_entropy_error
class Relu:
    def __init__(self):
        self.mask = None
    
    def forward(self,x):
        self.mask  = (x <=0)
        out  = x.copy()
        out[self.mask] = 0
        
        return out
    
    def backward(self,dout):
        dout[self.mask] = 0
        dx = dout
        return dx

class sigmoid:
    def __init__(self):
        self.out = None

    def forward(self,x):
        out = 1/(1+np.exp(-x))
        self.out = out
        return out
    
    def backward(self,dout):
        dx = dout*(1.0-self.out) * self.out
        
class affine:
    def __init__(self,W,b):
        self.W = W
        self.b = b
        self.x = None
        self.dW = None
        self.db = None
    def forward(self, x):
        self.x = x
        out = np.dot(x, self.W) + self.b
        return out
    
    def backward(self,dout):
        dx = np.dot(dout,self.W.T)
        self.dW = np.dot(self.x.T,dout)
        self.dB = np.sum(dout,axis = 0)
        
        return dx
    

class SoftmaxWithLoss:
    def __init__(self):
        self.loss = None
        self.y = None
        self.t = None
    
    def forward(self,x,t):
        self.t = t
        self.y = softmax(x)
        self.loss = cross_entropy_error(self.y,self.t)
        return self.loss
    
    def backward(self,dout=1):
        batch_size = self.t.shape[0]
        dx = (self.y - self.t) / batch_size # 역전파 때는 전파하는 값을 배치의 수로 나눠 데이터 1개당 오차를 앞 계층으로 전파
        