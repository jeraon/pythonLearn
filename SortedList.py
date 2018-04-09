
_identify = lambda x: x


class SortedList:
    def __init__(self,sequence=None,key=None):
        """初始化SortedList(参考list的创建方式)
        :param sequence:
        :param key:
        """
        # key用于指定排序规则，如果没有指定，则通过Lambda函数指定自身作为排序规则
        self.__key = key or _identify
        # 如果key是可调用对象，则返回True
        assert hasattr(self.__key, "__call__")
        # SortList()形式
        if sequence is None:
            self.__list = []
        # SortList(SortList)形式
        elif (isinstance(sequence, SortedList) and
              sequence.key == self.__key):
            self.__list = sequence.__list[:]
        # SortList(tuple)形式
        else:
            self.__list = sorted(list(sequence), key=self.__key)

    @property
    def key(self):
        """将传入的key函数作为私有属性，提供只读权限
        """
        return self.__key

    def add(self, value):
        """添加元素
        :param value:
        """
        # 获取插入值的索引
        index = self.__bisect_left(value)
        print("----index:",index)
        if index == len(self.__list):
            self.__list.append(value)
        else:
            self.__list.insert(index, value)

    def __bisect_left(self, value):
        """使用二分法
        """
        # 如果没指定key,则调用_identify(value),如果指定，则调用对应key的方法，相当于回调
        key = self.__key(value)
        left, right = 0, len(self.__list)
        while left < right:
            middle = (left+right) // 2
            if self.__key(self.__list[middle]) < key:
                left = middle+1
            else:
                right = middle

        return left

    def remove(self, value):
        index = self.__bisect_left(value)
        if index < len(self.__list) and self.__list[index] == value:
            del self.__list[index]
        else:
            raise ValueError("{0}.remove(x):x not in list".format(self.__class__.__name__))

    def count(self, value):
        count = 0
        index = self.__bisect_left(value)
        while(index < len(self.__list) and
              self.__list[index] == value):
            index += 1
            count += 1

        return count

    def index(self, value):
        index = self.__bisect_left(value)
        if index < len(self.__list) and self.__list[index] == value:
            return index
        else:
            raise ValueError("{0}.index(x):x not in list.".format(self.__class__.__name__))

    # 支持del L[xx]
    def __delitem__(self, key):
        del self.__list[key]

    # 支持 x = L[k]
    def __getitem__(self, index):
        return self.__list[index]

    def __iter__(self):
        return iter(self.__list)

    def __reversed__(self):
        return reversed(self.__list)

    def __contains__(self, value):
        index = self.__bisect_left(value)
        return index < len(self.__list) and self.__list[index] == value

    def pop(self, index=-1):
        return self.__list.pop(index)

    def clear(self):
        self.__list.clear()

    def __len__(self):
        return len(self.__list)

    def __str__(self):
        return str(self.__list)

    def copy(self):
        return SortedList(self, self.key)


if __name__ == "__main__":
    s = SortedList(("J","S","N","L","I","P"))  # ['I', 'J', 'L', 'N', 'P', 'S']
    s1 = SortedList(s)
    s1.add("M")

    def key(value):
        return value
    s3 = SortedList(s1, key)
    print(s1)  # ['I', 'J', 'L', 'M', 'N', 'P', 'S']
