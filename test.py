import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define the function you want to fit
def common_function(x, a, b, c):
    return a * np.exp(b * x) + c

# Combine all the data into one array
x_data = np.array([1, 2, 3, 4, 5])
y_data_1 = np.array([2.3, 4.1, 6.0, 8.2, 9.8])
y_data_2 = np.array([1.8, 3.5, 5.2, 7.0, 8.5])

# Combine y_data_1 and y_data_2 into one array
y_data_combined = np.concatenate((y_data_1, y_data_2))

# Perform curve fitting on the combined data
params, covariance = curve_fit(common_function, x_data, y_data_combined)

a, b, c = params

# Plot the original data and the fitted curve
plt.scatter(x_data, y_data_1, label='Data 1')
plt.scatter(x_data, y_data_2, label='Data 2')
plt.plot(x_data, common_function(x_data, a, b, c), label='Fitted Curve')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
