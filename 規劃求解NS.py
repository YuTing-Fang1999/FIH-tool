import numpy as np
from scipy import interpolate, optimize

# Given data
low_X = np.array([-1500, -1000,  -500,   300,   800,  1800,  2400,  2800,  3200,  4000.])
low_Y = np.array([-4500, -4000, -3400, -3000, -2500, -2000, -1000,     0,  1000,  2000.])
low_Z = np.array([[720, 720, 691, 650, 650, 720, 720, 820, 820, 820.],
                [720, 720, 791, 768, 700, 720, 720, 720, 791, 791.],
                [720, 720, 891, 868, 750, 625, 625, 691, 720, 720.],
                [720, 720, 891, 891, 720, 585, 625, 650, 720, 720.],
                [720, 720, 820, 820, 761, 625, 650, 691, 720, 720.],
                [720, 720, 720, 720, 730, 650, 650, 720, 720, 720.],
                [720, 720, 720, 720, 720, 720, 720, 720, 720, 720.],
                [720, 720, 720, 720, 720, 720, 720, 720, 720, 720.],
                [720, 720, 720, 720, 720, 720, 720, 720, 720, 720.],
                [720, 720, 720, 720, 720, 720, 720, 720, 720, 720.]])


low_DR = np.array([1917,2382,1558, 797.])
low_BV = np.array([ 3301,682,-1110,-3823.])

target_day = np.array([720, 720, 714, 715])

# Objective function for optimization
def objective_function(z_values):
    z_values = z_values.reshape(low_Z.shape)
    # Interpolate function
    low_f = interpolate.interp2d(low_X, low_Y, z_values, kind='linear')

    # Calculate the new low_day
    low_day = []
    for i in range(4):
        low_day.append(low_f(low_DR[i], low_BV[i])[0].astype(int))
    
    low_day = np.array(low_day)
    
    # Calculate the difference between low_day and target_day
    diff = low_day - target_day
    
    # Sum of squared differences
    sum_of_squared_diff = np.sum(diff**2)
    return sum_of_squared_diff

# 定義約束函數，將變數限制為整數值
def integer_constraint(x):
    return x - x.astype(int)

# Initial guess for optimization (all zeros, no change)
initial_guess = np.zeros(low_Z.size)
initial_guess = low_Z.reshape(low_Z.size)
# 約束設置
constraints = {'type': 'eq', 'fun': integer_constraint}
# Bounds for optimization
bounds = [(0, 2000)] * low_Z.size
# Optimization process zero:Powell,  low_Z:Nelder-Mead
result = optimize.minimize(objective_function, initial_guess, method='Nelder-Mead', bounds=bounds)
print(result)
# Updated low_Z with optimized values
updated_low_Z = result.x.reshape(low_Z.shape).astype(int)

print("Updated low_Z:")
print(updated_low_Z)
print(objective_function(result.x))

low_f = interpolate.interp2d(low_X, low_Y, updated_low_Z, kind='linear')

# Calculate the new low_day
low_day = []
for i in range(4):
    low_day.append(low_f(low_DR[i], low_BV[i])[0].astype(int))

low_day = np.array(low_day)
print(low_day)