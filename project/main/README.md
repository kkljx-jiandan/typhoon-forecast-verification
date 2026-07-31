# 1.配置要求
盘古：需要32GB以上内存，可使用8C 32G CPU算力 或 V100 GPU算力
伏羲和风乌：需要使用GPU算力

# 2.准备工作
2.1 下载ERA5的数据

pip install cdsapi

After installing the library, you need to configure it with your personal access token. You can obtain this token from your profile on the CDS portal at https://cds.climate.copernicus.eu/profile. Create a configuration file named .cdsapirc in your home directory and add the following content:

```python
url: https://cds.climate.copernicus.eu/api/v2
key: <PERSONAL-ACCESS-TOKEN>
```
python download_ERA5.py
下载目录：/home/mw/input/meteo4553/ERA5

2.2 下载盘古、伏羲、风乌三大模型

# 3.模型推理
## 1.2 
输入：
/home/mw/input/xxx
最终输出结果：
盘古大模型预报数据路径：/home/mw/input/evaluate7266/pangu/
伏羲大模型预报数据路径：/home/mw/input/evaluate7266/fuxi/
风乌大模型预报数据路径：/home/mw/input/evaluate7266/fengwu/

### HOW TO RUN FUXI?
cd Fuxi && python make_fuxi_input.py --init_time '20260706' --init_time_type 'case1' --raw_data_root_path '/home/mw/input/meteo4553/ERA5' --raw_data_format_type 'netcdf' --save_dir '/home/mw/temp' 

cd Fuxi && python fuxi.py --model /home/mw/input/weather1778/FuXi_EC --input /home/mw/temp/20230723-06_input_netcdf.nc --save_dir /home/mw/temp/Fuxi --num_steps 20 20 20


### HOW TO RUN PANGU?
1.下载所需模型，放在input目录
model_24 = '/home/mw/input/pangu5747/pangu_weather_24.onnx' # 24h
model_6  = '/home/mw/input/pangu5747/pangu_weather_6.onnx'  # 6h
model_3  = '/home/mw/input/pangu5747/pangu_weather_3.onnx'  # 3h
model_1  = '/home/mw/input/pangu5747/pangu_weather_1.onnx'  # 1h

2.将nc格式数据转换为npy数据
cd Pangu && python make_pangu_input.py

3.运行命令
以下三种任选其一

cd Pangu && python inference_iterative.py

cd Pangu && python inference_iterative_v2.py

cd Pangu && python inference_iterative_v3.py

4.将盘古模型预测的npy数据转为nc数据，方便后续继续分析
cd Pangu && python forecast_decode.py

output_surface_2023-07-26-06-00.npy
output_upper_2023-07-24-06-00.npy
output_surface_2023-07-27-06-00.npy
output_upper_2023-07-26-06-00.npy
output_surface_2023-07-25-06-00.npy
output_upper_2023-07-29-06-00.npy
output_upper_2023-07-25-06-00.npy
output_upper_2023-07-28-06-00.npy
output_surface_2023-07-28-06-00.npy
input_upper.npy
output_surface_2023-07-29-06-00.npy
input_surface.npy
output_upper_2023-07-27-06-00.npy
output_surface_2023-07-24-06-00.npy
数据将会保存到某个神秘文件夹？？？

### HOW TO RUN FENGWU?
1.准备数据
cd Fengwu && python make_fengwu_input.py
会在TEMP目录生成fengwu_input1.npy fengwu_input2.npy两个文件

2.模型进行推理计算
cd Fengwu && python inference.py

3.将风乌模型预测的npy数据转为nc数据，方便后续继续分析
cd Fengwu && python forecast_decode.py

### 为什么不合并为一个python文件？这样可以一键运行？
因为推理计算的过程十分耗时，如果把所有的过程合并为一个文件，那么一旦卡住就需要从头来过

## 分析比较
导出xlsx路径图
cd evaluate && python nc2xlsx.py
绘制气象AI大模型预报的台风路径
cd evaluate && python draw.py

距离计算
cd evaluate && python evalute.py

评估气象AI大模型预报的台风强度误差
cd evaluate && python eval_typhoon_intensity_bias.py