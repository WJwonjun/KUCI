import numpy as np
import matplotlib.pylab as plt
def num_diff(f,x):
    h = 1e-4
    return (f(x+h)-f(x-h))/(2*h)
def function_1(x):
    return 0.01*x**2+0.1*x
def function_2(x):
    return x[0]**2 + x[1]**2
def function_tmp1(x0):
    return x0*x0 + 4.0**2.0
def function_tmp2(x1):
    return x1*x1 + 3.0**2.0
def num_grad(f,x):
    h = 1e-4
    grad = np.zeros_like(x)
    
    for idx in range(x.size):
        tmp_val = x[idx]
        
        x[idx] = tmp_val+h
        fxh1 = f(x)
        
        x[idx] = tmp_val-h
        fxh2 = f(x)
        
        grad[idx] = (fxh1-fxh2) / (2*h)
        x[idx] = tmp_val
        
    return grad

def grad_descent(f,init_x, lr = 0.01, step_num=100):
    x = init_x
    for i in range(step_num):
        grad = num_grad(f,x)
        x -= lr*grad
    return x
x = np.arange(0.0,20.0,0.1)
y = function_1(x)
plt.xlabel("x")
plt.ylabel("y")
plt.plot(x,y)
plt.show()

print(num_diff(function_1,5))