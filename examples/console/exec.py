# %%
from mcculw_module import *
# %%
# set_speed(speed = 0.1) # mm/s
# %%
set_speed(speed = 0.1) # mm/s
scan_and_average(rate = 20000, points_per_channel=1000, chunk_size = 5000,offset=(0,0))

# %%
# set_speed(speed = 0.1) # mm/s
# scan_and_average(rate = 20000, points_per_channel=1000, chunk_size = 100,offset=(1.7380,0.5081))

# # %%
# set_speed(speed = 0.1) # mm/s
# # %%
# from datetime import datetime

# now = datetime.now()
# date_time = now.strftime("%Y-%m-%d_%H-%M")
# print("date and time:",date_time)	
# # %%
# file_name = f"LoadCellLog_{date_time}.csv."
# print(file_name)
# # %%
# scan_and_average(rate = 20000, points_per_channel=1000, chunk_size = 1,offset=(1.7380,0.5081))

# # %%
# set_speed(speed = 1) # mm/s