## 输入数组和数字，返回数字匹配数组的某个位置
def find_position(num, numbers):
    for i, n in enumerate(numbers[:-1]):
        if num < n:
            return i - 1
        elif num <= numbers[i + 1]:
            return i
    return len(numbers) - 1

numbers = [2, 3, 4, 5]
print(find_position(2.5, numbers))  # 1
print(find_position(6, numbers))
