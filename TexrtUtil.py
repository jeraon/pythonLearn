import string


def simplify(text, whitspace=string.whitespace, delete=""):

    # 首先定义一个用于存储过滤字符串的list和遍历时暂存字串的str
    result = []
    word=""
    for char in text:
        # 如果遍历字符处于需要删除的字符中，则不添加到过滤list中
        if char in delete:
            continue
        # 如果当前字符是空格，需要删除掉空格，如果word部位空串，先将之气的字符存储到list中，然后将word置为空串
        elif char in whitspace:
            if word:
                result.append(word)
                word=""
        # 如果不是空格，也不是需要删除的字符，使用word暂存
        else:
            word += char
    if word:
        result.append(word)
        # 将list转换成str返回
    return "".join(result)


def is_balance(text, brackets="(){}[]<>"):
    """
    judge whether the brackets is matched
    >>> is_balance("( just do it){}")
    """
    # 定义两个分别存储左括号和有括号的dict
    left_side = {}
    right_side = {}
    '''
    遍历字符串，将字串中的括号分别存储，其中left_side中key为左括号，value为出现次数
    right_side中key为右括号，value为左括号
    '''
    for left, right in zip(brackets[::2], brackets[1::2]):
        left_side[left] = 0
        right_side[right] = left
    # 遍历字串
    for char in text:
        # 如果当前字符处于left_side中，将该字符为key的对应值加1
        if char in left_side:
            left_side[char] += 1
        # 如果当前字符处于right_side中，将该字符为key的值找到，如果该值为0，说明left_side中没有，则不匹配
        # 如果该值不为0，因为上行+1操作，这里-1恢复
        elif char in right_side:
            left = right_side[char]
            if left_side[left] == 0:
                return False
            left_side[left] -= 1
    # 如果left_side中的任一项0都为零，则any()返回false，not any 返回ture
    return not any(left_side.values())


# 单元测试，会执行函数docstring中的示例
if __name__ == "__main__":
    import doctest
    doctest.testmod()

