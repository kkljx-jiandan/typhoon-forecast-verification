import os
from datetime import datetime
from forecast_decode_functions import surface, upper

# The directory for results forecast
results_dir = '/home/mw/temp/fengwu/'
# The results for output
outputs_dir = '/home/mw/temp/fengwu/'

# get all files that need to be decoded
for file in os.listdir(results_dir):
    print(file)
    if file.endswith(".npy") and file.startswith("output_"):
        # decode surface data
        surface(os.path.join(results_dir, file),file[:-4]+"_surface.nc",outputs_dir)
        # decode upper data
        upper(os.path.join(results_dir, file),file[:-4]+"_upper.nc",outputs_dir)