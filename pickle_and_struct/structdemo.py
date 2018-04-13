import struct
import sys
import os


class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        assert isinstance(age, int), "age must be integer"
        self.__age = age

    #  将对象写入二进制文件中
    def export_binary(self, filename):

        # 对于str类型，如果不进行该步骤，则会出现export error:argument for 's' must be a bytes object
        def packing_string(name):
            return name.encode("utf8")

        fh = None
        try:
            # 指定文件操作为二进制写操作
            fh = open(filename, "wb")
            # self.name为str类型，使用struct.pack8()时，必须将str类型转换为bytes类型，因此使用一个局部方法进行转换
            data = packing_string(self.name)
            data_len = len(data)
            fh.write(struct.pack("<{0}si".format(data_len), data, self.age))
            return True
        except Exception as err:
            print("{0}:export error:{1}".format(os.path.basename(sys.argv[0]), err))
            return False
        finally:
            if fh is not None:
                fh.close()

    def import_binary(self, filename):
        fh = None
        try:
            # 二进制文件读操作
            fh = open(filename, "rb")
            if fh is not None:
                s = fh.read()
                ss = struct.unpack("<{0}si".format(len(s)-4), s)
                print(ss)  # (b'zhangsan', 21)
                return True
        except Exception as err:
            print("{0}:export error:{1}".format(os.path.basename(sys.argv[0]), err))
            return False
        finally:
            if fh is not None:
                fh.close()


if __name__ == "__main__":
    s1 = Student("zhangsan", 21)
    s2 = Student("Lisi", 23)
    s1.export_binary("s1.bin")
    s1.import_binary("s1.bin")

