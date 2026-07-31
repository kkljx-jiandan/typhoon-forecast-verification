
# Step1：读取气象AI大模型预报结果

import xarray as xr

# 读取风乌大模型预报的地面层气象要素
ds = xr.open_dataset('/home/mw/input/evaluate7266/fengwu/output_5_surface.nc')

# Step2：筛选台风周边区域的海平面气压值
# 提取110° ~ 140°E，10° ~ 30°N范围内的海平面气压值
data = ds.mean_sea_level_pressure.sel(longitude=slice(110,140),latitude=slice(30,10))
data.plot()

# Step3：获取最低海平面气压值
# 计算110° ~ 140°E，10° ~ 30°N范围内的海平面气压值的最低值
data_min = data.min()

# Step4：提取海平面气压最低值的经纬度
# 提取110° ~ 140°E，10° ~ 30°N范围内的海平面气压值最低值的经纬度
lat_coord = data.latitude.values[data.argmin() // data.longitude.size]
lon_coord = data.longitude.values[data.argmin() % data.longitude.size]
print('海平面气压最低值的纬度:', lat_coord)
print('海平面气压最低值的经度:', lon_coord)

# 根据经纬度来检验提取的海平面气压结果，此处的结果与之前海平面气压最低值一致，说明提取结果正确
data.sel(longitude=lon_coord, latitude=lat_coord)

# Step5：按上述步骤提取逐小时台风预报路径

###(风乌)

import numpy as np
import pandas as pd
import xarray as xr
import netCDF4 as nc
import os
from datetime import datetime
import re
from glob import glob
import warnings
warnings.filterwarnings('ignore')


# 获取文件路径，并按时间顺序排序

def add_time_dim(da):
    da = da.expand_dims(time=[datetime.now()])
    return da


filelist_fw = sorted(glob('/home/mw/input/evaluate7266/fengwu/*_surface.nc'), 
                  key=lambda x: int(x.split('_')[1]))
# 合并读取多个nc数据
#ds_surface = xr.open_dataset(filelist)
fw_surface = xr.open_mfdataset(filelist_fw, preprocess = add_time_dim)
time_list_fw = pd.date_range(start='2026-07-06 6:00:00', end='2026-08-01 06:00:00', freq='6h')



fw_surface['time'] = time_list_fw

# 筛选台风巴威附近区域数据
slp_fw =  fw_surface.mean_sea_level_pressure.loc['2026-07-06 6:00:00':'2026-07-20 06:00:00',30:10,110:140]/100


# 提取风乌大模型预报的台风数据

#遍历时间步长，选出每个时间最低海平面气压中心值的经纬度

min_list_fw = []
lon_list_fw = []
lat_list_fw = []



for time in slp_fw.time:
    time_slice_fw = slp_fw.sel(time=time)
    min_value_fw = time_slice_fw.min().values
    #min_indices = time_slice.argmin(dim=['longitude','latitude'])
    lat_coord_fw = time_slice_fw.latitude.values[time_slice_fw.argmin() // time_slice_fw.longitude.size]
    lon_coord_fw = time_slice_fw.longitude.values[time_slice_fw.argmin() % time_slice_fw.longitude.size]
    min_list_fw.append(min_value_fw)
    lon_list_fw.append(lon_coord_fw)
    lat_list_fw.append(lat_coord_fw)


# 创建DataFrame表格格式

hour8 = pd.Timedelta(hours=8)
new_time_fw = slp_fw.time+hour8



fw_message_data = {'time':new_time_fw,'lon':lon_list_fw,'lat':lat_list_fw ,'slp_min': min_list_fw}

fw_message = pd.DataFrame(fw_message_data)

print(fw_message)

# 保存为xlsx文件

fw_message.to_excel('风乌.xlsx', index=False)



#伏羲
#all_files = (glob('/home/mw/input/evaluate7266/fuxi/*.nc'))
# 选择列表中的前N个文件
#file_list = all_files[:25]  
                
# 合并读取多个nc数据

fx =xr.open_mfdataset('/home/mw/input/evaluate7266/fuxi/*.nc',
                       concat_dim='step',combine='nested')


#fx =xr.open_mfdataset('/home/mw/input/evaluate7266/fuxi/*.nc',
#concat_dim='step',combine='by_coords')


#fx = fx.drop_dims(['time','step'])

#time_list_fx = pd.date_range(start='2023-07-23 12:00:00', end='2023-08-07 06:00:00', freq='6h')

#fx['time'] =  time_list_fx

#slp_fx =  fx.__xarray_dataarray_variable__.loc['MSL',6:144,30:10,110:140,:]

slp_fx = fx['__xarray_dataarray_variable__'].sel(step=slice(6,144),level='MSL',lon=slice(110,140),lat=slice(30,10))/100

min_list_fx = []
lon_list_fx = []
lat_list_fx = []



for step in slp_fx.step:
    time_slice_fx = slp_fx.sel(step=step)
    min_value_fx = time_slice_fx.min().values
    #min_indices = time_slice.argmin(dim=['longitude','latitude'])
    lat_coord_fx = time_slice_fx.lat.values[time_slice_fx.argmin() // time_slice_fx.lon.size]
    lon_coord_fx = time_slice_fx.lon.values[time_slice_fx.argmin() % time_slice_fx.lon.size]
    min_list_fx.append(min_value_fx)
    lon_list_fx.append(lon_coord_fx)
    lat_list_fx.append(lat_coord_fx)


time_list_fx = pd.date_range(start='2026-07-06 6:00:00', end='2023-07-20 06:00:00', freq='6h')
hour8 = pd.Timedelta(hours=8)
new_time_fx = time_list_fx+hour8

fx_message_data = {'time':new_time_fx,'lon':lon_list_fx,'lat':lat_list_fx ,'slp_min':min_list_fx}

fx_message = pd.DataFrame(fx_message_data)

print(fx_message)

fx_message.to_excel('伏羲.xlsx', index=False)


#盘古
filelist_pg = sorted(glob('/home/mw/input/evaluate7266/pangu/output_surface_*.nc'))
# 合并读取多个nc数据
#ds_surface = xr.open_dataset(filelist)
pg_surface = xr.open_mfdataset(filelist_pg, preprocess = add_time_dim)
time_list_pg = pd.date_range(start='2023-07-23 12:00:00', end='2023-07-31 06:00:00', freq='6h')



pg_surface['time'] = time_list_pg

# 筛选台风杜苏芮附近区域数据
slp_pg =  pg_surface.mean_sea_level_pressure.loc['2023-07-23 12:00:00':'2023-07-29 06:00:00',30:10,110:140]/100


# 提取盘古大模型预报的台风杜苏芮数据

#遍历时间步长，选出每个时间最低海平面气压中心值的经纬度

min_list_pg = []
lon_list_pg = []
lat_list_pg = []



for time in slp_pg.time:
    time_slice_pg = slp_pg.sel(time=time)
    min_value_pg = time_slice_pg.min().values
    #min_indices = time_slice.argmin(dim=['longitude','latitude'])
    lat_coord_pg = time_slice_pg.latitude.values[time_slice_pg.argmin() // time_slice_pg.longitude.size]
    lon_coord_pg = time_slice_pg.longitude.values[time_slice_pg.argmin() % time_slice_pg.longitude.size]
    min_list_pg.append(min_value_pg)
    lon_list_pg.append(lon_coord_pg)
    lat_list_pg.append(lat_coord_pg)


# 创建DataFrame表格格式

hour8 = pd.Timedelta(hours=8)
new_time_pg = slp_pg.time+hour8

pg_message_data = {'time':new_time_pg,'lon':lon_list_pg,'lat':lat_list_pg ,'slp_min':min_list_pg}

pg_message = pd.DataFrame(pg_message_data)

pg_message

# 保存为xlsx文件

pg_message.to_excel('盘古.xlsx', index=False)
