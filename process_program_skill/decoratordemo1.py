
# 方式一，使用functool.wrap()函数
# functools模块用于高阶函数：作用于或返回其他函数的函数
from functools import wraps
# functools.wraps()函数常用于在定义一个修饰函数时作为函数修饰器调用functool.update_wrapper()方法
# functools.wraps修饰器进行包裹，确保了wrapper()函数的__name__和__doc__相等
def my_decorator(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print("Calling decorator function---1")
        return function(*args, **kwargs)
    return wrapper

@my_decorator
def example():
    """DocString:This is a decorator by functool.wrapper """
    print("Calling example function---1")


# 方式二，自定义修饰器
def my_decorator2(function):
    def wrapper(*args, **kwargs):
        print("called my_decorator2 function-----2")
        return function(*args, **kwargs)
    # 将名称和docstring设置为原来函数的
    wrapper.__name__ = function.__name__
    wrapper.__doc__ = function.__doc__
    return wrapper


@my_decorator2
def example_2():
    """DocString:This is a decorator by custome """
    print("called example2 function----2")


example()
print(example.__name__)
print(example.__doc__)
print("=================")
example_2()
print(example_2.__name__)
print(example_2.__doc__)
"""
输出结果：
Calling decorator function---1
Calling example function---1
example
DocString:This is a decorator by functool.wrapper 
=================
called my_decorator2 function-----2
called example2 function----2
example_2
DocString:This is a decorator by custome 
"""

