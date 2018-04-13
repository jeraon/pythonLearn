import functools

"""
该demo展示如何实现修饰器函数带多个参数

"""
def bound(arg1, arg2):
    def wrap(func):
        @functools.wraps(func)
        def wrap_wrap(*args, **kwargs):
            result = func(*args, **kwargs)
            if result < arg1:
                # .....
                pass
            elif result > arg2:
                # ....
                pass
            return result
        return wrap_wrap
    return wrap



@bound(0,100)
def get_percent(account, total):
    return (account / total) * 100


s = get_percent(1, 3000)
print("{0}%".format(s))