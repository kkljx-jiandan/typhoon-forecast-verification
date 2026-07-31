import os
from datetime import datetime
from forecast_decode_functions import surface, upper

# The date and time of the initial field
date_time = datetime(
    year=2026, 
    month=7, 
    day=06,
    hour=6,
    minute=0)
date_time_final = datetime(
    year=2026,
    month=7,
    day=19,
    hour=6,
    minute=0)
 
# The directory for results forecast
results_dir = '/home/mw/temp/'
# The results for output
outputs_dir = '/home/mw/temp/'

# get all files that need to be decoded
for file in os.listdir(results_dir):
    print(file)
    if file.endswith(".npy"):
        if file.startswith("output_surface"):
            # decode surface data
            surface(os.path.join(results_dir, file),file[:-4]+".nc",outputs_dir)
        elif file.startswith("output_upper"):
            # decode upper data
            upper(os.path.join(results_dir, file),file[:-4]+".nc",outputs_dir)

# surface(os.path.join(results_dir,"output_surface.npy"),"output_surface_2023-07-29-06-00.nc",outputs_dir)
# surface(os.path.join(results_dir,"output_upper.npy"),"output_upper_2023-07-29-06-00.nc",outputs_dir)
