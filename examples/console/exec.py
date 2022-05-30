# %%
from mcculw_module import *
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
# %%
set_speed(speed = 0.3) # mm/s
scan_and_average(rate=20000, points_per_channel=5000, num_chunks=1,offset=(0,0))
# %%
set_speed(speed = 0.3) # mm/s
# %% zeroing (should change speed?)
set_speed(speed = 0.3) # mm/s
scan_and_average(rate=20000, points_per_channel=5000, num_chunks=100,offset=(0,0))
winsound.Beep(frequency, duration)

# %%
# 0.1 mm/s / num_chunks = 1000
set_speed(speed = 0.1) # mm/s
scan_and_average(rate=20000, points_per_channel=5000, num_chunks=3000,offset=(0,0))
winsound.Beep(frequency, duration)
# %% RUN 0.3
set_speed(speed = 0.3) # mm/s 
scan_and_average(rate=20000, points_per_channel=5000, num_chunks=2000,offset=(0,0))
winsound.Beep(frequency, duration)

# %%
# %%
set_speed(speed = 1) # mm/s
scan_and_average(rate=20000, points_per_channel=5000, num_chunks=600,offset=(0,0))
winsound.Beep(frequency, duration)
# %%
winsound.Beep(frequency, duration)

# %%
set_speed(speed = 0.3) # mm/s

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