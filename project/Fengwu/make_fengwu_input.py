import numpy as np
import pandas as pd
import xarray as xr
import netCDF4 as nc
import os
from glob import glob
from datetime import datetime
import matplotlib.pyplot as plt

'''
模型需要两个连续的间隔6小时的输入数据，依次是input1.npy和input2.npy，input2.npy的时刻是input1.npy时刻+6小时。

每个数据的维度是69x721x1440，69表示通道数，即大气特征。
纬度范围是[90N, 90S]，经度范围是[-180, 180]。前4个变量是地面变量，顺序依次是['u10', 'v10', 't2m', 'msl']；
随后是高空变量，顺序依次是['z', 'q', 'u', 'v', 't']，
高空层共计13层，顺序依次是[50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000]。
因此，69个变量的顺序依次为[u10, v10, t2m, msl, z50, z100, ..., z1000, q50, q100, ..., q1000, t50, t100, ..., t1000]。
'''
# 地面层
data = nc.Dataset('/home/mw/input/meteo4553/ERA5/2D/era5_2D_2023072300.nc')

# 提取nc数据中的变量
u10 = data.variables['u10']
v10 = data.variables['v10']
t2m = data.variables['t2m']
msl = data.variables['msl']
print(msl.shape)
# 高空层
data = nc.Dataset('/home/mw/input/meteo4553/ERA5/3D/era5_3D_2023072300.nc')

# 提取nc数据中的变量
z = data.variables['z'][:,::-1,:,:][0]
q = data.variables['q'][:,::-1,:,:][0]
u = data.variables['u'][:,::-1,:,:][0]
v = data.variables['v'][:,::-1,:,:][0]
t = data.variables['t'][:,::-1,:,:][0]

# 得到输入的地面数据，转为float32格式
input_data = np.concatenate([u10,v10,t2m,msl,z,q,u,v,t]).data.astype(np.float32)

# 保存为npy格式
np.save('/home/mw/temp/fengwu_input1.npy', input_data)

# 查看数据维度
print(input_data.shape)
'''
(1, 721, 1440)
(69, 721, 1440)
'''

# 地面层
data = nc.Dataset('/home/mw/input/meteo4553/ERA5/2D/era5_2D_2026070606.nc')

# 提取nc数据中的变量
u10 = data.variables['u10']
v10 = data.variables['v10']
t2m = data.variables['t2m']
msl = data.variables['msl']

# 高空层
data = nc.Dataset('/home/mw/input/meteo4553/ERA5/3D/era5_3D_2026070606.nc')

# 提取nc数据中的变量
z = data.variables['z'][:,::-1,:,:][0]
q = data.variables['q'][:,::-1,:,:][0]
u = data.variables['u'][:,::-1,:,:][0]
v = data.variables['v'][:,::-1,:,:][0]
t = data.variables['t'][:,::-1,:,:][0]

# 得到输入的地面数据，转为float32格式
input_data = np.concatenate([u10,v10,t2m,msl,z,q,u,v,t]).data.astype(np.float32)

# 保存为npy格式
np.save('/home/mw/temp/fengwu_input2.npy', input_data)
