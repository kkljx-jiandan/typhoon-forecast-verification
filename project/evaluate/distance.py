from geopy.distance import geodesic
import pandas as pd
import matplotlib.pyplot as plt

df_fw = pd.read_excel('/home/mw/project/风乌.xlsx')
df_fx =pd.read_excel('/home/mw/project/伏羲.xlsx')
df_pg = pd.read_excel('/home/mw/project/盘古.xlsx')
df_gc = pd.read_excel('/home/mw/input/202606.xls')
# 提取观测的台风巴威海平面最低气压、经纬度数据


lat_gc= df_gc['lat']
lon_gc= df_gc['lon']

# 提取风乌大模型预报的台风海平面最低气压、经纬度数据
lat_fw = df_fw['lat']
lon_fw = df_fw['lon']



# 提取伏羲大模型预报的台风海平面最低气压、经纬度数据


lat_fx= df_fx['lat']
lon_fx= df_fx['lon']



# 提取盘古大模型预报的台风海平面最低气压、经纬度数据


lat_pg= df_pg['lat']
lon_pg= df_pg['lon']



# 计算风乌大模型预报的台风路径偏差
fw_wucha = []


for latfw, lonfw, latgc,longc in zip(lat_fw, lon_fw, lat_gc,lon_gc):
     #print(f"item1: {lat_fw}, item2: {lon_fw}")
     #print(f"item3: {lat_gc},item4:{lon_gc}")
     Afw = (latfw, lonfw)
     Bfw = (latgc, longc)
     fw_juli = geodesic(Afw, Bfw).km
     fw_wucha.append(fw_juli)

fw_wucha

# 计算盘古大模型预报的台风路径偏差

pg_wucha = []


for latpg, lonpg, latgc,longc in zip(lat_pg, lon_pg, lat_gc,lon_gc):
     #print(f"item1: {lat_pg}, item2: {lon_pg}")
     #print(f"item3: {lat_gc},item4:{lon_gc}")
     Apg = (latpg, lonpg)
     Bpg = (latgc, longc)
     pg_juli = geodesic(Apg, Bpg).km
     pg_wucha.append(pg_juli)

pg_wucha
# 计算伏羲大模型预报的台风路径偏差
fx_wucha = []


for latfx, lonfx, latgc,longc in zip(lat_fx, lon_fx, lat_gc,lon_gc):
     #print(f"item1: {lat_fx}, item2: {lon_fx}")
     #print(f"item3: {lat_gc},item4:{lon_gc}")
     Afx = (latfx, lonfx)
     Bfx = (latgc, longc)
     fx_juli = geodesic(Afx, Bfx).km
     fx_wucha.append(fx_juli)

fx_wucha

# 绘制风乌、伏羲和盘古气象AI大模型预报的台风路径误差

time_wc = df_fw['time']


fig=plt.figure(figsize=(14,5),dpi = 100)

ax1=plt.subplot(111)

ax1.set_ylim(0,1200)

fw,=ax1.plot(time_wc,fw_wucha,color='yellow',lw=2.0,marker='.',markersize=10,label='fw')
fx,=ax1.plot(time_wc,fx_wucha,color='green',lw=2.0,marker='.',markersize=10,label='fx')
pg,=ax1.plot(time_wc,pg_wucha,color='red',lw=2.0,marker='.',markersize=10,label='pg')


plt.legend((fw,fx,pg),('fw','fx','pg'),loc='upper left',frameon=False,framealpha=0.4)
