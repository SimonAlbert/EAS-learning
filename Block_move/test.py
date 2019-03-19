# 等差等比数列合成一个数列（切片应用）
listi = []

for i in range(100):
    listi += [2*i+3, 3*i+4, 2**i]
print(listi)

# numpy的常用操作
import numpy as np


a = np.random.rand(4, 3)
print(a)
print(a.shape)

b = a.reshape(1, 3*4)
print(a, '\n', b)

b = np.arange(3*4)

print(b)
b = b.reshape(3, 4)

c = a*a
print(c)
print(c.shape)

c = np.matmul(a, b)
print(c)
print(c.shape)

print(np.random.rand(3, 2))
size = [3, 2]
print(np.zeros(size))
print(np.ones(size))


# 灵活的切片操作start:stop:step
a = np.arange(15)
print(a)
print(a[0:15:3])

# 高级索引，大量数据索引更方便
a = np.arange(15)
a = a.reshape(3, 5)
print(a)
print(a.shape)
x = np.array([[0, 0], [2, 2]])
y = np.array([[0, 4], [0, 4]])
print(a[x, y])

# 布尔索引，数据筛选

a = np.random.uniform(-1, 1,[1, 10])
print(a[a > 0])


