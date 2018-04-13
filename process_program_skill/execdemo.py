
import math
'''
exec()函数可以动态执行表达式、方法或者或函数，但是exec()并不会存取导入的模块、调用时的变量、函数、对象
同时没有途径获取执行后创建的函数或变量，因此需要传入一个字典，该字典提供了存放对象的场所，在执行exec()后，
相关的变量都存放在该字典中，

'''

code = '''
def get_area_circle(radius):
        return math.pi * (radius ** 2)
'''

context = {}
# 由于exec在执行时需要使用math模块，因此将math模块加入到该字典中
context["math"] = math
exec(code, context)
s = context["get_area_circle"](4)
print(s)
name = "sys"
module = __import__("sys")
print(module.path)


