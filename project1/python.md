**魔法方法**

让自己定义的类能和原生类一样顺滑

```python
print(f'{1+2=}') #3
print(f"{'a'+'b'=}")#'ab'

print((x:=1).__add__(2))#3
print('a'.__add__('b'))#ab
#有点像cpp里的重载，数字里调用+和字符串里调用+是不一样的


class ShoppingCart:
  def __init__(self,items:List[str]):
    self.items=items
    
  def __add__(self,another_cart):
    new_cart=ShoppingCart(self.items+another_cart.items)
    
  def __str__(self):
    return f'Cart({self.items})'
      
    
class add:
    def __init__(self,num):
        self.num=num

    def __add__(self,another_num):
        new_add=add(self.num+another_num)
        return new_add
    
    def __str__(self):
        return f"{self.num}"
    
    def __call__(self,antoher_num):
        return self.num+antoher_num #希望能够像调用函数一样去调用实例
    
    

print(add(2)(3))
```

```
__init__.py的作用

当我们import一个package时，会调用里面的__init__.py
在里面可以写包的初始化
管理包接口（公共接口，from packageA import x,那个x要在__init__.py里面引入 from .moduleA import x
包的信息 __version__, __author__
```

