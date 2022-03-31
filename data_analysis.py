# %%
import numpy as np
from matplotlib import pyplot as plt

# %%
data_all = np.loadtxt('LoadCellLog_2022-03-30_20-48.csv',delimiter=',')
# %%
plt.plot(data_all)
average = np.mean(data_all,axis=0)
# %%
num_chunks = 5000
# chunk_size = 1000
sample_rate = 20000
# %%
data_all = np.loadtxt('LoadCellLog_2022-03-30_20-59.csv',delimiter=',')

# %%
plt.plot((data_all[:,0] - average[0])/0.0785,'.-')
plt.plot((data_all[:,1] - average[1])/0.0109,'.-')

# %%
# %%
chunk_size = 500
