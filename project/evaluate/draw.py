import os
import pandas as pd
import geopandas as gpd
import shapely.geometry as sgeom
import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib.animation import FuncAnimation
import matplotlib.lines as mlines
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import cartopy.mpl.ticker as cticker
from cartopy.io.shapereader import Reader
from PIL import Image

import warnings 
warnings.filterwarnings('ignore')

df_fw = pd.read_excel('/home/mw/project/风乌.xlsx')
df_fx =pd.read_excel('/home/mw/project/伏羲.xlsx')
df_pg = pd.read_excel('/home/mw/project/盘古.xlsx')
df_gc = pd.read_excel('/home/mw/input/abc8438/202305_new.xls')


lat_fw = df_fw['lat']
lon_fw = df_fw['lon']

lat_fx= df_fx['lat']
lon_fx= df_fx['lon']

lat_pg= df_pg['lat']
lon_pg= df_pg['lon']

lat_gc= df_gc['lat']
lon_gc= df_gc['lon']

shp_path='/home/mw/input/map6141/中国_省.geojson'#
proj= ccrs.PlateCarree()  # 简写投影

fig=plt.figure(figsize=(14,10),dpi = 100)
 
reader = Reader(shp_path)
ditu = cfeat.ShapelyFeature(reader.geometries(), proj, edgecolor='k', facecolor='none')

ax1=plt.subplot(111,projection=ccrs.PlateCarree())
extent=[110,130,14,32]#限定绘图范围
ax1.add_feature(ditu, linewidth=1.0)#添加市界细节
ax1.set_extent(extent, crs=proj)


fw,=ax1.plot(lon_fw,lat_fw,color='yellow',lw=2.0,marker='.',markersize=10,label='fw')
fx,=ax1.plot(lon_fx,lat_fx,color='green',lw=2.0,marker='.',markersize=10,label='fx')
pg,=ax1.plot(lon_pg,lat_pg,color='red',lw=2.0,marker='.',markersize=10,label='pg')
gc,=ax1.plot(lon_gc,lat_gc,color='blue',lw=2.0,marker='.',markersize=10,label='gc')

plt.legend((fw,fx,pg,gc),('fw','fx','pg','gc'),loc='upper right',frameon=False,framealpha=0.4)

ax1.set_xticks(np.arange(110,130+1,2), crs=ccrs.PlateCarree())
ax1.set_yticks(np.arange(14,32+1,2), crs=ccrs.PlateCarree())
lon_formatter = cticker.LongitudeFormatter()
lat_formatter = cticker.LatitudeFormatter()
ax1.xaxis.set_major_formatter(lon_formatter)
ax1.yaxis.set_major_formatter(lat_formatter)