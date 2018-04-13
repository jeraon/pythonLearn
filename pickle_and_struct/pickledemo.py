import struct
import sys
import os
import pickle


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

    def export_binary(self,filename):
        fh = None
        try:
            fh = open(filename, "wb")
            pickle.dump(self, fh, pickle.HIGHEST_PROTOCOL)
            return True
        except(EnvironmentError, pickle.PicklingError) as err:
            print("{0}: export err:{1}".format(
                os.path.basename(sys.argv[0]), err
            ))
            return False
        finally:
            if fh is not None:
                fh.close()

    def import_binary(self, filename):
        fh = None
        try:
            fh = open(filename, "rb")
            s = pickle.load(fh)
            print(s.name, s.age)   # zhangsan 21
            return True
        except(EnvironmentError,pickle.UnpicklingError) as err:
            print("{0}: export err:{1}".format(
                os.path.basename(sys.argv[0]), err
            ))
            return False
        finally:
            if fh is not None:
                fh.close()



if __name__ == "__main__":
    s1 = Student("zhangsan", 21)
    s2 = Student("Lisi", 23)
    s1.export_binary("s1.bin")
    s1.import_binary("s1.bin")


