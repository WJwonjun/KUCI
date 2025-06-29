class MulLayer:
    def __init__(self):
        self.x = None
        self.y = None
        
    def forward(self,x,y):
        self.x = x
        self.y = y
        out = x*y
        return out
    def backward(self,dout):
        dx = dout * self.y
        dy = dout * self.x
        return dx,dy
class AddLayer:
    def __init__(self):
        pass
    def forward(self,x,y):
        out = x+y
        return out
    def backward(self,dout):
        dx = dout*1
        dy = dout*1
        return dx,dy

#buy_orange
apple  =100
apple_num  =2
orange = 150
orange_num  =3
tax = 1.1

mul_apple_layer = MulLayer()
mul_orange_layer = MulLayer()
add_fruit_later = AddLayer()
mul_tax_layer = MulLayer()

apple_price = mul_apple_layer.forward(apple,apple_num)
orange_price = mul_orange_layer.forward(orange,orange_num)
fruit_price  = add_fruit_later.forward(apple_price,orange_price)
price = mul_tax_layer.forward(fruit_price,tax)

dprice = 1
dfruit_price, dtax  = mul_tax_layer.backward(dprice)
dapple_price, dorange_price = add_fruit_later.backward(dfruit_price)
dapple,dapple_num = mul_apple_layer.backward(dapple_price)
dorange,dorange_num = mul_orange_layer.backward(dorange_price)

print(price)
print(dapple_num,dapple,dorange_num,dorange,dtax)   
