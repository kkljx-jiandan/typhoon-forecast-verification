import numpy as np
import netCDF4 as nc
import os

## function to process surface data
def surface(file, file_name, outputs_dir):
# Load the saved numpy arrays
    surface_data = np.load(file)[0:4,:,:]
    u_component_of_wind_10m = surface_data[0]
    v_component_of_wind_10m = surface_data[1]
    temperature_2m = surface_data[2]
    mean_sea_level_pressure = surface_data[3]

    with nc.Dataset(
        os.path.join(outputs_dir, file_name), "w", format="NETCDF4_CLASSIC"
    ) as nc_file:
        # Create dimensions
        nc_file.createDimension("longitude", 1440)
        nc_file.createDimension("latitude", 721)

        # Create variables
        nc_lon = nc_file.createVariable("longitude", np.float32, ("longitude",))
        nc_lat = nc_file.createVariable("latitude", np.float32, ("latitude",))
        nc_msl = nc_file.createVariable(
            "mean_sea_level_pressure", np.float32, ("latitude", "longitude")
        )
        nc_u10 = nc_file.createVariable(
            "u_component_of_wind_10m", np.float32, ("latitude", "longitude")
        )
        nc_v10 = nc_file.createVariable(
            "v_component_of_wind_10m", np.float32, ("latitude", "longitude")
        )
        nc_t2m = nc_file.createVariable(
            "temperature_2m", np.float32, ("latitude", "longitude")
        )

        # Set variable attributes
        nc_lon.units = "degrees_east"
        nc_lat.units = "degrees_north"
        nc_msl.units = "Pa"
        nc_u10.units = "m/s"
        nc_v10.units = "m/s"
        nc_t2m.units = "K"

        # Write data to variables
        nc_lon[:] = np.linspace(0.125, 359.875, 1440)
        nc_lat[:] = np.linspace(90, -90, 721)
        nc_msl[:] = mean_sea_level_pressure
        nc_u10[:] = u_component_of_wind_10m
        nc_v10[:] = v_component_of_wind_10m
        nc_t2m[:] = temperature_2m

## function to process upper data
def upper(file,file_name,outputs_dir):
# Load the saved numpy arrays
    upper_data = np.load(file)[4:,:,:]
    geopotential = upper_data[0:13,:,:]
    specific_humidity = upper_data[13:26,:,:]
    u_component_of_wind = upper_data[26:39,:,:]
    v_component_of_wind = upper_data[39:52,:,:]
    temperature = upper_data[52:65,:,:]


    with nc.Dataset(
        os.path.join(outputs_dir, file_name), "w", format="NETCDF4_CLASSIC"
    ) as nc_file:
        # Create dimensions
        nc_file.createDimension("longitude", 1440)
        nc_file.createDimension("latitude", 721)
        nc_file.createDimension("level", 13)

        # Create variables
        nc_lon = nc_file.createVariable("longitude", np.float32, ("longitude",))
        nc_lat = nc_file.createVariable("latitude", np.float32, ("latitude",))
        nc_level = nc_file.createVariable("level", np.float32, ("level",))
        nc_geopotential = nc_file.createVariable(
            "geopotential", np.float32, ("level", "latitude", "longitude")
        )
        nc_specific_humidity = nc_file.createVariable(
            "specific_humidity", np.float32, ("level", "latitude", "longitude")
        )
        nc_temperature = nc_file.createVariable(
            "temperature", np.float32, ("level", "latitude", "longitude")
        )
        nc_u_component_of_wind = nc_file.createVariable(
            "u_component_of_wind", np.float32, ("level", "latitude", "longitude")
        )
        nc_v_component_of_wind = nc_file.createVariable(
            "v_component_of_wind", np.float32, ("level", "latitude", "longitude")
        )

        # Set variable attributes
        nc_lon.units = "degrees_east"
        nc_lat.units = "degrees_north"
        nc_level.units = "hPa"
        nc_geopotential.units = "m"
        nc_specific_humidity.units = "kg/kg"
        nc_temperature.units = "K"
        nc_u_component_of_wind.units = "m/s"
        nc_v_component_of_wind.units = "m/s"
        # Write data to variables
        nc_lon[:] = np.linspace(0.125, 359.875, 1440)
        nc_lat[:] = np.linspace(90, -90, 721)
        nc_level[:] = np.array([50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000])
        nc_geopotential[:] = geopotential
        nc_specific_humidity[:] = specific_humidity
        nc_temperature[:] = temperature
        nc_u_component_of_wind[:] = u_component_of_wind
        nc_v_component_of_wind[:] = v_component_of_wind