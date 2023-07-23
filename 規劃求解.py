import numpy as np
from scipy import interpolate

# normal_X = np.array([-1500,-800,0,1000,1800,2400,2800,3200,3500,4200])
# normal_Y = np.array([-2000,-1000,0,1500,3000,4500,6000,7500,8500,9500])
# normal_Z = np.array([[ 880, 980, 856, 750, 660, 637, 620, 660, 660, 660.],
#                     [ 880, 980, 875, 761, 757, 637, 641, 641, 687, 687.],
#                     [ 980,1192, 980, 821, 777, 612, 641, 641, 668, 668.],
#                     [1080,1380,1077, 871, 721, 668, 668, 668, 668, 668.],
#                     [1155,1427,1227,1025, 833, 712, 668, 668, 768, 768.],
#                     [1188,1458,1308,1125, 933, 720, 768, 768, 868, 868.],
#                     [1088,1282,1182,1025, 867, 739, 723, 868, 968, 987.],
#                     [ 999,1182,1082,1085, 868, 739, 768, 887, 887, 887.],
#                     [ 985,1185,1068,1068, 868, 768, 787, 787, 787, 787.],
#                     [ 968,1168,1039, 939, 768, 668, 639, 687, 687, 687.]])

# normal_f = interpolate.interp2d(normal_X, normal_Y, normal_Z, kind='linear')
# normal_DR = np.array([1917,2382,1558, 797.])
# normal_BV = np.array([ 3301,682,-1110,-3823.])

# normal_day = []
# for i in range(4):
#     normal_day.append(normal_f(normal_DR[i], normal_BV[i])[0].astype(int))

# normal_day = np.array(normal_day)
# print(normal_day)

# low_X = np.array([-1500, -1000,  -500,   300,   800,  1800,  2400,  2800,  3200,  4000.])
# low_Y = np.array([-4500, -4000, -3400, -3000, -2500, -2000, -1000,     0,  1000,  2000.])
# low_Z = np.array([[720, 720, 691, 650, 650, 720, 720, 820, 820, 820.],
#                 [720, 720, 791, 768, 700, 720, 720, 720, 791, 791.],
#                 [720, 720, 891, 868, 750, 625, 625, 691, 720, 720.],
#                 [720, 720, 891, 891, 720, 585, 625, 650, 720, 720.],
#                 [720, 720, 820, 820, 761, 625, 650, 691, 720, 720.],
#                 [720, 720, 720, 720, 730, 650, 650, 720, 720, 720.],
#                 [720, 720, 720, 720, 720, 720, 720, 720, 720, 720.],
#                 [720, 720, 720, 720, 720, 720, 720, 720, 720, 720.],
#                 [720, 720, 720, 720, 720, 720, 720, 720, 720, 720.],
#                 [720, 720, 720, 720, 720, 720, 720, 720, 720, 720.]])

# low_f = interpolate.interp2d(low_X, low_Y, low_Z, kind='linear')
# low_DR = np.array([1917,2382,1558, 797.])
# low_BV = np.array([ 3301,682,-1110,-3823.])

# low_day = []
# for i in range(4):
#     low_day.append(low_f(low_DR[i], low_BV[i])[0].astype(int))

# low_day = np.array(low_day)
# print(low_day)

import numpy as np
from scipy import interpolate, optimize

# Given data
normal_X = np.array([-1500, -800, 0, 1000, 1800, 2400, 2800, 3200, 3500, 4200])
normal_Y = np.array([-2000, -1000, 0, 1500, 3000, 4500, 6000, 7500, 8500, 9500])
normal_Z = np.array([[880, 980, 856, 750, 660, 637, 620, 660, 660, 660.],
                     [880, 980, 875, 761, 757, 637, 641, 641, 687, 687.],
                     [980, 1192, 980, 821, 777, 612, 641, 641, 668, 668.],
                     [1080, 1380, 1077, 871, 721, 668, 668, 668, 668, 668.],
                     [1155, 1427, 1227, 1025, 833, 712, 668, 668, 768, 768.],
                     [1188, 1458, 1308, 1125, 933, 720, 768, 768, 868, 868.],
                     [1088, 1282, 1182, 1025, 867, 739, 723, 868, 968, 987.],
                     [999, 1182, 1082, 1085, 868, 739, 768, 887, 887, 887.],
                     [985, 1185, 1068, 1068, 868, 768, 787, 787, 787, 787.],
                     [968, 1168, 1039, 939, 768, 668, 639, 687, 687, 687.]])

normal_DR = np.array([1917, 2382, 1558, 797])
normal_BV = np.array([3301, 682, -1110, -3823])

target_day = np.array([557, 337, 696, 754])

# Interpolate function
normal_f = interpolate.interp2d(normal_X, normal_Y, normal_Z, kind='linear')

# Objective function for optimization
def objective_function(z_values):
    z_values = z_values.reshape(normal_Z.shape)
    # Interpolate function
    normal_f = interpolate.interp2d(normal_X, normal_Y, z_values, kind='linear')

    # Calculate the new normal_day
    normal_day = []
    for i in range(4):
        normal_day.append(normal_f(normal_DR[i], normal_BV[i])[0].astype(int))
    
    normal_day = np.array(normal_day)
    
    # Calculate the difference between normal_day and target_day
    diff = normal_day - target_day
    
    # Sum of squared differences
    sum_of_squared_diff = np.sum(diff**2)
    return sum_of_squared_diff

# 定義約束函數，將變數限制為整數值
def integer_constraint(x):
    return x - x.astype(int)

# Initial guess for optimization (all zeros, no change)
initial_guess = np.zeros(normal_Z.size)
initial_guess = normal_Z.reshape(normal_Z.size)
# 約束設置
constraints = {'type': 'eq', 'fun': integer_constraint}
# Bounds for optimization
bounds = [(0, 2000)] * normal_Z.size
# Optimization process zero:Powell,  normal_Z:Nelder-Mead
result = optimize.minimize(objective_function, initial_guess, method='Nelder-Mead', bounds=bounds)
print(result)
# Updated normal_Z with optimized values
updated_normal_Z = result.x.reshape(normal_Z.shape).astype(int)

print("Updated normal_Z:")
print(updated_normal_Z)
print(objective_function(result.x))

normal_f = interpolate.interp2d(normal_X, normal_Y, updated_normal_Z, kind='linear')

# Calculate the new normal_day
normal_day = []
for i in range(4):
    normal_day.append(normal_f(normal_DR[i], normal_BV[i])[0].astype(int))

normal_day = np.array(normal_day)
print(normal_day)
