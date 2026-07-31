import pandas as pd
import matplotlib.pyplot as plt

df_fw = pd.read_excel('/home/mw/project/风乌.xlsx')
df_fx =pd.read_excel('/home/mw/project/伏羲.xlsx')
df_pg = pd.read_excel('/home/mw/project/盘古.xlsx')
df_gc = pd.read_excel('/home/mw/input/abc8438/202305_new.xls')

gc_hpa = df_gc['pressure']
# 计算风乌大模型预报的台风杜苏芮强度偏差
fw_hpa = df_fw['slp_min']
fw_hpa_wc = fw_hpa-gc_hpa
#fw_hpa_wc

time_wc = df_fw['time']

# 计算盘古大模型预报的台风杜苏芮强度偏差
pg_hpa = df_pg['slp_min']
pg_hpa_wc = pg_hpa-gc_hpa

# 计算伏羲大模型预报的台风杜苏芮强度偏差
fx_hpa = df_fx['slp_min']
fx_hpa_wc = fx_hpa-gc_hpa

# 绘制风乌、伏羲和盘古气象AI大模型预报的台风强度误差

fig=plt.figure(figsize=(14,5),dpi = 100)

ax1=plt.subplot(111)



fw,=ax1.plot(time_wc,fw_hpa_wc,color='yellow',lw=2.0,marker='.',markersize=10,label='fw')
fx,=ax1.plot(time_wc,fx_hpa_wc,color='green',lw=2.0,marker='.',markersize=10,label='fx')
pg,=ax1.plot(time_wc,pg_hpa_wc,color='red',lw=2.0,marker='.',markersize=10,label='pg')
ax1.set_yticks(np.arange(0,60+1,20))#设置Y1的刻度

plt.legend((fw,fx,pg),('fw','fx','pg'),loc='upper left',frameon=False,framealpha=0.4)