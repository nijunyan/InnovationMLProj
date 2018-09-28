import numpy as np

a = np.array([0, 0])
if np.all(a==0):
    a = a + 1
print(a)