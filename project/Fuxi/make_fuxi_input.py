
"""
本脚本适合做HRES 的输入,下载数据均为分析场的零场,sfc,pl单独下载的情况,支持netcdf与grib格式;
FuXi模型的输入变量:
    5个气压层变量: ['Z', 'T', 'U', 'V', 'R'], 
    每个变量包含13层: [50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000], 
    5个地面变量: ['T2M', 'U10', 'V10', 'MSL', 'TP'];
    
注意事项:
    1. 输入是连续的两个历史时刻, 间隔6小时, 分辨率是0.25; eg: [00, 06]做为输入那么起报时刻是06点;
    2. Z不是Geopential Height, 是 Geopential;
    3. 降水是6小时累积单位mm, 第一个时刻的降水可以置0;
    4. 温度是开尔文单位;
    5. R表示相对湿度;
    6. 纬度方向是90 ~ -90;
    7. 气压层的顺序是从高空到地面50 ~ 1000; eg: Z50, Z100, ... , Z1000;
    8. 数据中不能有NAN;
    9.严格按照此顺序做输入输入模型；
    levels = ['Z50', 'Z100', 'Z150', 'Z200', 'Z250', 'Z300', 'Z400', 'Z500', 'Z600', 'Z700', 'Z850', 'Z925', 'Z1000',
          'T50', 'T100', 'T150', 'T200', 'T250', 'T300', 'T400', 'T500', 'T600', 'T700', 'T850', 'T925', 'T1000',
         'U50', 'U100', 'U150', 'U200', 'U250', 'U300', 'U400', 'U500', 'U600', 'U700', 'U850', 'U925', 'U1000',
          'V50', 'V100', 'V150', 'V200', 'V250', 'V300', 'V400', 'V500', 'V600', 'V700', 'V850', 'V925', 'V1000',
          'R50', 'R100', 'R150', 'R200', 'R250', 'R300', 'R400', 'R500', 'R600', 'R700', 'R850', 'R925', 'R1000',
           'T2M', 'U10', 'V10', 'MSL', 'TP']

"""

"""
本脚本适合做HRES 的输入,下载数据均为分析场的零场,sfc,pl单独下载的情况;
"""

"""
Created on Wed Jun  12 13:15:07 2023

@author: Jun Liu
"""

import os
import numpy as np
import pandas as pd
import pygrib as pg
import xarray as xr

def print_level_info(ds):
    # Assuming 'ds' is the object you want to check
    if isinstance(ds, xr.DataArray):
        print("The object is a DataArray")
    elif isinstance(ds, xr.Dataset):
        ds=ds.to_array()
        print("The object is a DataSet")
    else:
        print("The object is neither a DataArray nor a DataSet")
    check_names = [
        'Z500', 'Z850',
        'T500', 'T850',
        'U500', 'U850',
        'V500', 'V850',
        'R500', 'R850',
        'T2M', 'U10', 'V10', 'MSL', 'TP'
    ]
    for lvl in ds.level.values:
        if lvl.upper() in check_names:
            v = ds.sel(level=lvl).values
            print(f'{lvl}: {v.shape}, {v.min():.3f} ~ {v.max():.3f}')

import time as tm

class ExecutionTimer:
    def __init__(self):
        self.last_time = tm.perf_counter()
    def format_time(self, seconds):
        """将秒数转换为时分秒和毫秒格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours} hours, {minutes} minutes, {int(seconds)} seconds and {milliseconds} milliseconds"

    def print_elapsed_time(self, message=""):
        """打印从上次记录时间到当前的经过时间，并更新时间戳"""
        current_time = tm.perf_counter()
        execution_time = current_time - self.last_time
        formatted_time = self.format_time(execution_time)
        print(f"{message} - Time elapsed: {formatted_time}.")
        self.last_time = current_time



def make_hres_input_zero_field_grib_format(sfc_path,pl_path,tpsetzero=True):
    
    assert os.path.exists(sfc_path)
    assert os.path.exists(pl_path)
    
    levels = [50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000]
    pl_names = ['z', 't', 'u', 'v', 'r']
    sf_names = ['2t', '10u', '10v', 'msl','tp']

    try:
        ds_pl = pg.open(pl_path)
        ds_sfc=pg.open(sfc_path)
    except:
        print(f"\033[92m Failed to open file!\033[0m")
    

    print("\033[92m***********pl数据信息************\033[0m")
    for i, item in enumerate(ds_pl,1):
        print("item.date-->:",item.date)
        print("item.time-->:",item.validDate)
        print("item.level-->:",item.level)
        print("item.step-->:",item.step)
        print("item.shortName-->:",item)
    print("\033[92m***********pl数据信息************\033[0m")

    print("***************************************************") 

    print("\033[92m***********sfc数据信息************\033[0m")
    for i, item in enumerate(ds_sfc,1):
        print("item.date-->:",item.date)
        print("item.time-->:",item.validDate)
        print("item.level-->:",item.level)
        print("item.step-->:",item.step)
        print("item.shortName-->:",item)
    print("\033[92m***********sfc数据信息************\033[0m")

    input = []
    level = []

    for name in pl_names + sf_names :
        print("name:",name)
        if name in pl_names:
            try:
                data = ds_pl.select(shortName=name, level=levels)
        
            except:
                print("\033[92m pl wrong,can't found!\033[0m")

            data = data[:len(levels)]

            if len(data) != len(levels):

                print("\033[92m pl wrong,level wrong!\033[0m")

            for v in data:
                if v.step==0:
                    print("v.date:",v.date)
                    print("v.time:",v.validDate)
                    init_time = v.validDate
                    lat = v.distinctLatitudes
                    lon = v.distinctLongitudes
                    img, _, _ = v.data()
                    input.append(img)
                    level.append(f'{name}{v.level}')
                    # if (f'{name}{v.level}')=="z500":
                    #     np.save("z500.npy",v.values)
                    print(f"{v.name}: {v.level}, {img.shape}, {img.min()} ~ {img.max()}")

        if name in sf_names:
            try:
                data_sfc = ds_sfc.select(shortName=name)
                print("len(data_sfc):",len(data_sfc))
            except:
                print(f"\033[92m sfc{name} wrong,can't found!\033[0m")
              
            name_map = {'2t': 't2m', '10u': 'u10', '10v': 'v10','msl':'msl','tp':'tp'}
            name = name_map[name]

            for v in data_sfc:
                if v.step==0:
                    img, _, _ = v.data()
                    if name == "tp" and (tpsetzero==True):
                        tp = img * 0
                        input.append(tp)
                        level.append("tp")
                        print("***************go into***************")
                    else:
                        input.append(img)
                        level.append(name)
                    print(f"{v.name}: {img.shape}, {img.min()} ~ {img.max()}")
    
    input = np.stack(input)
    print("input.shape:",input.shape)
    assert input.shape[-3:] == (70, 721, 1440)
    assert input.max() < 1e10

    level = [lvl.upper() for lvl in level]
    times = [pd.to_datetime(init_time)]
    input = xr.DataArray(
        data=input[None],
        dims=['time', 'level', 'lat', 'lon'],
        coords={'time': times, 'level': level, 'lat': lat, 'lon': lon},
    )
    if np.isnan(input).sum() > 0:
        print("\033[92mField has nan value\033[0m")  
    print("input:",input)
    return input


def make_hres_input_zero_field_netcdf_format(sfc_path,pl_path,tpsetzero=True):
    
    assert os.path.exists(sfc_path)
    assert os.path.exists(pl_path)
    
    levels = [50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000]
    pl_names = ['z', 't', 'u', 'v', 'r']
    sf_names = ['t2m', 'u10', 'v10', 'msl','tp']

    try:
        ds_pl = xr.open_dataset(pl_path)
        ds_sfc=xr.open_dataset(sfc_path)
    except:
        print(f"\033[92m Failed to open file!\033[0m")
    
    input = []
    level = []

    for name in pl_names + sf_names :
        print("name:",name)
        if name in pl_names:
            try:
                data = ds_pl[name].sel(level=levels)
            except:
                print("\033[92m pl wrong,can't found!\033[0m")

            if len(data.level.values) != len(levels):

                print("\033[92m pl wrong,level wrong!\033[0m")

            for lvl in levels:
                print("data.time.values:",data.time.values)
                init_time = data.time
                lat = data.latitude
                lon = data.longitude

                img0= data.sel(level=lvl).values
                img=np.squeeze(img0)
                input.append(img)
                level.append(f'{name}{lvl}')
                # if (f'{name}{lvl}')=="z500":
                #     np.save("z500_nc.npy",img)
                # print(f"{img0.name}: {img0.level}, {img.shape}, {img.min()} ~ {img.max()}")
        print("\033[92m ************\033[0m")
        if name in sf_names:
            try:
                data_sfc = ds_sfc[name].sel().values
                # print("len(data_sfc):",len(data_sfc))
            except:
                print(f"\033[92m sfc{name} wrong,can't found!\033[0m")
              
            # name_map = {'2t': 't2m', '10u': 'u10', '10v': 'v10','msl':'msl','tp':'tp'}
            # name = name_map[name]

            for v in data_sfc:
                img= v
                if name == "tp" and (tpsetzero==True):
                    tp = img * 0
                    input.append(tp)
                    level.append("tp")
                    print("\033[92m***************go into***************\033[0m")
                else:
                    input.append(img)
                    level.append(name)
                # print(f"{v.name}: {img.shape}, {img.min()} ~ {img.max()}")
    # print("\033[92m input:\033[0m",input)
    input = np.stack(input)
    print("input.shape:",input.shape)
    assert input.shape[-3:] == (70, 721, 1440)
    assert input.max() < 1e10

    lat=np.arange(90,-90.25,-0.25)
    lon=np.arange(0,360,0.25)

    level = [lvl.upper() for lvl in level]
    times = pd.to_datetime(init_time)
    input = xr.DataArray(
        data=input[None],
        dims=['time', 'level', 'lat', 'lon'],
        coords={'time': times, 'level': level, 'lat': lat, 'lon': lon},
    )
    if np.isnan(input).sum() > 0:
        print("\033[92mField has nan value\033[0m")  
    print("input:",input)
    return input


def make_gfs_input_merge(file_hist_sfc,file_hist_pl,file_init_sfc,file_init_pl,save_dir,tpsetzero,raw_data_format_type):
    os.makedirs(save_dir, exist_ok=True)
    os.chmod(save_dir, 0o777)
    if raw_data_format_type=="grib":

        d1 = make_hres_input_zero_field_grib_format(file_hist_sfc,file_hist_pl,tpsetzero=tpsetzero)
        d2 = make_hres_input_zero_field_grib_format(file_init_sfc,file_init_pl,tpsetzero=tpsetzero)
    if raw_data_format_type=="netcdf":
        d1 = make_hres_input_zero_field_netcdf_format(file_hist_sfc,file_hist_pl,tpsetzero=tpsetzero)
        d2 = make_hres_input_zero_field_netcdf_format(file_init_sfc,file_init_pl,tpsetzero=tpsetzero)

    if d1 is not None and d2 is not None:
        # print("Start saving two-step data")
        ds = xr.concat([d1, d2], 'time')
        ds = ds.assign_coords(time=ds.time.astype(np.datetime64))
        ds = ds.astype(np.float32)
        save_name = pd.to_datetime(d2.time.values[0]).strftime(f"%Y%m%d-%H_input_{raw_data_format_type}.nc")
        ds.to_netcdf(os.path.join(save_dir, save_name))
        print("\033[92m Input data saved successfully\033[0m")
        print("input-ds:",ds)
        print("ds.level.values:",ds.level.values)
    return ds,save_name


if __name__ == "__main__":
    import argparse
    import xarray as xr
    timer = ExecutionTimer()
    
    parser = argparse.ArgumentParser(description="Process EC data.")
    parser.add_argument("--tpsetzero", default=True, type=bool, help="Zero field data is no precipitation, at this time, the parameter can\
                                                                      be ignored, if the download EC for the forecast moment,\
                                                                      need to zero precipitation, the parameter needs to be set to True")
    parser.add_argument("--init_time", default="20231012", help="Initial time")
    parser.add_argument("--raw_data_root_path", default="./hres_input_grib_raw/hres", help="Root path for raw data")
    parser.add_argument("--init_time_type", default="case1", help="Type of initial time")
    parser.add_argument("--save_dir", default="./", help="Directory for saving data")
    parser.add_argument("--raw_data_format_type", default="grib", help="Raw data dataset type")

    args = parser.parse_args()

    init_time_type_dict = {"case1": (0, 6), "case2": (6, 12), "case3": (12, 18), "case4": (18, 0)}
    

    # Build file paths
    if args.raw_data_format_type=="grib":
        file_suffix="grib"
    if args.raw_data_format_type=="netcdf":
        file_suffix="nc"

    file_hist_sfc = f"{args.raw_data_root_path}/2D/era5_2D_{args.init_time}{init_time_type_dict[args.init_time_type][0]:02d}.{file_suffix}"
    file_hist_pl = f"{args.raw_data_root_path}/3D/era5_3D_{args.init_time}{init_time_type_dict[args.init_time_type][0]:02d}.{file_suffix}"
    file_init_sfc = f"{args.raw_data_root_path}/2D/era5_2D_{args.init_time}{init_time_type_dict[args.init_time_type][1]:02d}.{file_suffix}"
    file_init_pl = f"{args.raw_data_root_path}/3D/era5_3D_{args.init_time}{init_time_type_dict[args.init_time_type][1]:02d}.{file_suffix}"
    print(file_hist_sfc)
    data, _ = make_gfs_input_merge(file_hist_sfc, file_hist_pl, file_init_sfc, file_init_pl, args.save_dir, args.tpsetzero,args.raw_data_format_type)

    print("data.level.values:", data.level.values)
    print("data.time.values:", data.time.values)
    print("data:", data)
    print_level_info(data)
    timer.print_elapsed_time("processing time")





