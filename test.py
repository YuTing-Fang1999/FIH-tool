import numpy as np
arr = np.array([0.0927, 0.5928, 0.0964, 0.8743, 0.168, 0.0212, 0.9929])
arr[3:] /= 2
print(arr.tolist())