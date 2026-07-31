import cdsapi


def download_hourly_2D_file(year, month, day, hour):
    '''
    下载ERA5的2D变量数据：
    '10m_u_component_of_wind', 
    '10m_v_component_of_wind', 
    'mean_sea_level_pressure', 
    '2m_temperature', 
    'total_precipitation'
    '''
    filename = 'era5_2D_'+str(year).zfill(4)+str(month).zfill(2)+str(day).zfill(2)+str(hour).zfill(2)+'.nc'
    c = cdsapi.Client()
    c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type'  : 'reanalysis',
                'format'        : 'netcdf', 
                'variable'      : ['10m_u_component_of_wind', '10m_v_component_of_wind', 
                                   'mean_sea_level_pressure', '2m_temperature', 'total_precipitation'], 
                'year'          : str(year).zfill(4),
                'month'         : str(month).zfill(2),
                'day'           : [str(day).zfill(2)],
                'time'          : [str(hour).zfill(2) + ':00'],
        },
        filename)



def download_hourly_3D_file(year, month, day, hour):
    '''
    下载ERA5的3D变量数据：
    'geopotential', 
    'specific_humidity', 
    'relative_humidity',
    'temperature',
    'u_component_of_wind', 
    'v_component_of_wind'
    '''
    filename = 'era5_3D_'+str(year).zfill(4)+str(month).zfill(2)+str(day).zfill(2)+str(hour).zfill(2)+'.nc'
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type'  : 'reanalysis',
            'format'        : 'netcdf', 
            'variable'      : ['geopotential', 'specific_humidity', 'relative_humidity', 'temperature',
                               'u_component_of_wind', 'v_component_of_wind',],
            'pressure_level': ['1000', '925', '850', '700', '600', '500', '400', 
                               '300', '250', '200', '150', '100', '50'],
            'year'          : str(year).zfill(4),
            'month'         : str(month).zfill(2),
            'day'           : [str(day).zfill(2)],
            'time'          : [str(hour).zfill(2) + ':00'],
        },
        filename)

for day in range(6, 20):
    for hour in [0,6,12,18]:
        download_hourly_2D_file('2026', '07', str(day).zfill(2), str(hour).zfill(2))
        download_hourly_3D_file('2026', '07', str(day).zfill(2), str(hour).zfill(2))