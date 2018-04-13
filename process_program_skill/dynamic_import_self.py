import os
import sys

def load_modules():

    modules = []
    # 获取当前目录下所有.py文件
    for filename in os.listdir("."):
        if filename.endswith(".py") and not filename.startswith("dynamic_import_self"):
            # 拆分扩展名
            name = os.path.splitext(filename)[0]
            if name.isidentifier():
                fh = None
                try:
                    fh = open(filename, "r", encoding="utf8")
                    code = fh.read()
                    # 得到一个模块对象,并通过传入的name新建一个模块对象
                    # type()方法返回参数对应类型的对象，如type(2)返回一个int对象
                    module = type(sys)(name)
                    # 将新创建的module添加到sys.modules中，sys.modules是一字典，存储已加载的模块，以模块名为key，模块为值
                    sys.modules[name] = module
                    # 通过exec()动态执行代码,并将生成的属性、对象和所需模块放在module.__dict中
                    # 每个module对象都有一个特殊属性__dict,用于存储对象属性的字典
                    exec(code, module.__dict__)
                    modules.append(module)
                except (EnvironmentError, SyntaxError) as err:
                    # 如果发生异常，从sys.modules字典中移除该module对象
                    sys.modules.pop(name, None)
                    print(err)
                finally:
                    if fh is not None:
                        fh.close()
    return modules





