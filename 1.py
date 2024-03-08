def sequence(n):
    result = ''
    for i in range(1, n + 1):
        result += str(i) * i
    return result[:n]


n = int(input('Введите количество элементов: '))
print('Первые', n, 'элементов последовательности:')
print(sequence(n))
