import numpy as np

a = np.zeros((2,2))
a[0]+=[1,1]
print(a[0])

l = [1,2,3]
print(type(l))
k = list(l)
print(type(k))