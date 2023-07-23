import numpy as np
from scipy import interpolate

# # 数据转换为数值类型
# X = np.array([-1500, -800, 0, 1000, 1800, 2400, 2800, 3200, 3500, 4200])
# Y = np.array([-2000, -1000, 0, 1500, 3000, 4500, 6000, 7500, 8500, 9500])
# Z = np.array([[880, 980, 856, 750, 660, 637, 620, 660, 660, 660],
#               [880, 980, 875, 761, 757, 637, 641, 641, 687, 687],
#               [980, 1192, 980, 821, 777, 612, 641, 641, 668, 668],
#               [1080, 1380, 1077, 871, 721, 668, 668, 668, 668, 668],
#               [1155, 1427, 1227, 1025, 833, 712, 668, 668, 768, 768],
#               [1188, 1458, 1308, 1125, 933, 720, 768, 768, 868, 868],
#               [1088, 1282, 1182, 1025, 867, 739, 723, 868, 968, 987],
#               [999, 1182, 1082, 1085, 868, 739, 768, 887, 887, 887],
#               [985, 1185, 1068, 1068, 868, 768, 787, 787, 787, 787],
#               [968, 1168, 1039, 939, 768, 668, 639, 687, 687, 687]])

# # 创建二维插值函数
# f = interpolate.interp2d(X, Y, Z, kind='linear')

# # 求取[120, 300]这个点的内插值
# x_interp = 10
# y_interp = 10


# z_interp = f(x_interp, y_interp)

# print(z_interp)
# print(f"The interpolated value is: {int(z_interp[0])}")

# lower_bound = -1600
# upper_bound = 10
# indices = np.argwhere((X <= lower_bound)).flatten()
# print(indices[-1])

# 数据转换为数值类型
X = np.array([1800, 2400])
Y = np.array([0, 1500])
Z = np.array([[777, 612],
              [721, 668]])

# 创建二维插值函数
f = interpolate.interp2d(X, Y, Z, kind='linear')

x_interp = 2382
y_interp = 682
z_interp = f(x_interp, y_interp)

print(f"The interpolated value is: {int(z_interp[0])}")

