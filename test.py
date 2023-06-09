import numpy as np
arr = np.array([0.3212, 0.3562, 0.0552, 0.3628, 0.1878, 0.0836, 0.9937])
arr[3:] /= 2
print(arr.tolist())