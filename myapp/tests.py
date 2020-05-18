import math
import numpy as np


def fft(x, n):
    if n == 2:
        return [x[0] + x[1], x[0] - x[1]]

    f1 = x[0::2]
    f2 = x[1::2]
    even = fft(f1, n // 2)
    odd = fft(f2, n // 2)
    xn2 = [0 for i in x]


    # print(even)
    theta = (2 * math.pi) / n
    w = complex(math.cos(theta), - math.sin(theta))
    for i in range(n // 2):
        print(i,i+n//2)
        xn2[i] = even[i] + (w ** i) * odd[i]

        xn2[i + n // 2] = even[i] - (w ** i) * odd[i]
    return xn2

# xn = list(map(int, input('Enter input signal: ').split()))
xn = [1, 1, 1, 0, 0, 0, 0, 0]
i = 0
flag = 0
while i != 4 :
    if len(xn) % math.pow(2,i) == 0 :
        pass
    else :
        flag = 1
        print("Wrong input length")
        break
    i += 1
if flag != 1 :
    xn2 = fft(xn, len(xn))
    print(xn2)