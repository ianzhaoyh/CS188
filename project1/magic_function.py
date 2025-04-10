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



        

