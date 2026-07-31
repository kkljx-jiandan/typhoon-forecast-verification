import numpy as np
import pandas as pd
import xarray as xr
import netCDF4 as nc
import os
from datetime import datetime
import matplotlib.pyplot as plt

# 将地表数据（surface data）转为npy格式
# 创建空数组，维度为(4, 721, 1440)
surface_data = np.zeros((4, 721, 1440), dtype=np.float32)
# 打开nc数据，并依次写入msl、u10、v10、t2m变量
with nc.Dataset('/home/mw/input/meteo4553/ERA5/2D/era5_2D_2026070606.nc') as nc_file:
    surface_data[0] = nc_file.variables['msl'][:].astype(np.float32)
    surface_data[1] = nc_file.variables['u10'][:].astype(np.float32)
    surface_data[2] = nc_file.variables['v10'][:].astype(np.float32)
    surface_data[3] = nc_file.variables['t2m'][:].astype(np.float32)
# 保存为npy数据
np.save('/home/mw/temp/input_surface.npy', surface_data)

# 将高空数据（upper air data）转为npy格式
# 创建空数组，维度为(5, 13, 721, 1440)
upper_data = np.zeros((5, 13, 721, 1440), dtype=np.float32)
# 打开nc数据，并依次写入z、q、t、u和v变量
with nc.Dataset('/home/mw/input/meteo4553/ERA5/3D/era5_3D_2026070606.nc') as nc_file:
    upper_data[0] = (nc_file.variables['z'][:]).astype(np.float32)
    upper_data[1] = nc_file.variables['q'][:].astype(np.float32)
    upper_data[2] = nc_file.variables['t'][:].astype(np.float32)
    upper_data[3] = nc_file.variables['u'][:].astype(np.float32)
    upper_data[4] = nc_file.variables['v'][:].astype(np.float32)
# 保存为npy数据
np.save('/home/mw/temp/input_upper.npy', upper_data)
