# %%
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from pathlib import Path
# %% Windows path
note_path = Path('C:/Users/yjung/Dropbox (Harvard University)/Stick-slip/Experiment-data/ExpNote.xlsx')
data_folder_path = Path('C:/Users/yjung/Dropbox (Harvard University)/Stick-slip/Experiment-data')

# %% OSX Path
note_path = Path('/Users/yeonsu/Dropbox (Harvard University)/Stick-slip/Experiment-data/ExpNote.xlsx')
data_folder_path = Path('/Users/yeonsu/Dropbox (Harvard University)/Stick-slip/Experiment-data')
# %%
exp_date = '2022-05-29'
config = pd.read_excel(note_path, sheet_name=exp_date,nrows=1)
time_step = config['TimeStep'][0]
offset_N = config['N-offset'][0]
offset_T = config['T-offset'][0]

# %%
data_table = pd.read_excel(note_path, skiprows = 9,sheet_name=exp_date)
data_table = data_table.dropna()
print(data_table)
# %%
diameter_list = data_table['Diameter'].drop_duplicates().to_numpy()
speed_list = data_table['Speed'].drop_duplicates().to_numpy()
thickness_list = data_table['Speed'].drop_duplicates().to_numpy()
time_list = data_table['Time'].drop_duplicates().to_numpy()
dir_list = data_table['Direction'].drop_duplicates().tolist()

print(dir_list)
# %%
data_path = []
for t in time_list:
    # data_path.append(f'examples/console/LoadCellLog_{exp_date}_{t}.csv')    
    data_path.append(data_folder_path.joinpath(f'{exp_date}/LoadCellLog_{exp_date}_{t}.csv'))
# %%
data_path[0]
# %%
exp_no = 2

# data_table['Direction'][exp_no]
test = np.loadtxt(data_path[exp_no],delimiter=',')
t_points = np.arange(0,test.shape[0]*time_step,time_step)

direction = data_table['Direction'].tolist()[exp_no]

if direction == 'Push':
    dir_sign = 1
elif direction == 'Pull':
    dir_sign = -1

print(dir_sign)

# %%
fig, ax = plt.subplots(2,figsize=(20,5))

ax[0].plot(t_points,dir_sign*(offset_T - test[:,0])/0.0785)
ax[1].plot(t_points,-(test[:,1] - offset_N)/0.0109)

fig.text(0.5, 0.04, 'Time (s)', ha='center')
fig.text(0.04, 0.5, 'Force (gf)', va='center', rotation='vertical')
# %%
friction = dir_sign*(offset_T - test[:,0])/0.0785
friction.shape
# frequency
# energy release
# %%
friction_data = [None]*len(data_table)
normal_data = [None]*len(data_table)

data_table['Friction'] = friction_data
data_table['Normal'] = normal_data

print(data_table)

# %%
friction_conversion = 0.0785
normal_conversion = 0.0109

DiaQuery = 30.0
DirQuery = 'Push'
exp_no_list = np.array(data_table[(data_table['Diameter'] == DiaQuery) & (data_table['Direction'] == DirQuery)].index)
# data_table[(data_table['Diameter'] == DiaQuery) & (data_table['Direction'] == DirQuery)].index

num_repeat = len(exp_no_list)
fig, ax = plt.subplots(num_repeat*2,figsize=(20,5*num_repeat))
# %%

for i,exp_no in enumerate(exp_no_list):
    t = data_table['Time'][exp_no]
    data_path = data_folder_path.joinpath(f'{exp_date}/LoadCellLog_{exp_date}_{t}.csv')

    data_in = np.loadtxt(data_path,delimiter=',')
    t_points = np.arange(0,data_in.shape[0]*time_step,time_step)

    direction = data_table['Direction'][exp_no]

    if direction == 'Push':
        dir_sign = 1
    elif direction == 'Pull':
        dir_sign = -1

    friction = dir_sign*(offset_T - data_in[:,0])/friction_conversion
    normal = -(data_in[:,1] - offset_N)/normal_conversion

    ax[i].plot(t_points,friction)
    ax[i+num_repeat].plot(t_points,normal)

fig.text(0.5, 0.04, 'Time (s)', ha='center')
fig.text(0.04, 0.5, 'Force (gf)', va='center', rotation='vertical')
# %%
for exp_no in range(len(data_table)):
    t = data_table['Time'][exp_no]
    data_path = data_folder_path.joinpath(f'{exp_date}/LoadCellLog_{exp_date}_{t}.csv')

    data_in = np.loadtxt(data_path,delimiter=',')
    t_points = np.arange(0,data_in.shape[0]*time_step,time_step)

    direction = data_table['Direction'][exp_no]

    if direction == 'Push':
        dir_sign = 1
    elif direction == 'Pull':
        dir_sign = -1

    friction = dir_sign*(offset_T - data_in[:,0])/friction_conversion
    normal = -(data_in[:,1] - offset_N)/normal_conversion

    data_table['Friction'][exp_no] = friction
    data_table['Normal'][exp_no] = normal

# %%
print(data_table)
# %%
exp_no = 2
print(data_table.iloc[exp_no])
data_sample = data_table['Normal'][exp_no]

plt.figure(figsize=(20,5))
plt.plot(data_sample,'.-')
# %%
diff_sample = np.diff(data_sample)
plt.figure(figsize=(20,5))
plt.plot(diff_sample,'o-')

tt = np.arange(len(data_sample))*0.25

ipt = np.where(np.abs(diff_sample) > 5)[0]
plt.figure(figsize=(20,5))
plt.plot(tt,data_sample,'.-')
plt.plot(0.25*ipt,data_sample[ipt],'o')
plt.xlabel('Time (sec)')
plt.ylabel('Friction (gf)')

# %%
plt.hist(np.diff(ipt))

# %%
# Set a clean upper y-axis limit.
clr_list = ['#e41a1c','#377eb8','#4daf4a','#984ea3']

mean_interval = np.zeros((4,1))
std_interval = np.zeros((4,1))
i = 0
for exp_no in [5, 3, 7, 1]:
    data_sample = data_table['Friction'][exp_no]
    diff_sample = np.diff(data_sample)
    ipt = np.where(np.abs(diff_sample) > 5)[0]
    n, bins, patches = plt.hist(0.25*np.diff(ipt),
        bins=range(0,50,2),
        label=data_table['Diameter'][exp_no],
        alpha=0.5,
        density=True,
        stacked=True,
        color=clr_list[i])
    plt.plot(np.linspace(1,47,24),n,'o-',color=clr_list[i])
    mean_interval[i] = np.mean(0.25*np.diff(ipt))
    std_interval[i] = np.std(0.25*np.diff(ipt))

    i = i + 1

plt.legend()
plt.xlabel('Interval (sec)')
plt.ylabel('Occurrence')
# data_folder_path = Path('/Users/yeonsu/Dropbox (Harvard University)/Stick-slip/Experiment-data')

# fig_label = '%s_%s.png'%(data_table['Diameter'][exp_no],data_table['Direction'][exp_no])
plt.savefig(data_folder_path/exp_date/'Histogram_Push.png',dpi=300)
# %%
plt.plot([30,45,60,90],mean_interval,'o-')
plt.xlabel('Shell diameter (mm)')
plt.ylabel('Average interval between slips (sec)')
plt.savefig(data_folder_path/exp_date/'MeanInt_Push.png',dpi=300)
# %%
plt.plot([30,45,60,90],std_interval,'o-')
plt.xlabel('Shell diameter (mm)')
plt.ylabel('STD of interval between slips (sec)')
plt.savefig(data_folder_path/exp_date/'STDInt_Push.png',dpi=300)
# %%
i = 0
for exp_no in [6, 4, 8, 2]:
    data_sample = data_table['Friction'][exp_no]
    diff_sample = np.diff(data_sample)
    ipt = np.where(np.abs(diff_sample) > 10)[0]
    n, bins, patches = plt.hist(0.25*np.diff(ipt),
        bins=range(0,50,2),
        label=data_table['Diameter'][exp_no],
        alpha=0.5,
        density=True,
        stacked=True,
        color=clr_list[i])
    plt.plot(np.linspace(1,47,24),n,'o-',color=clr_list[i])
    i = i + 1

plt.legend()
plt.xlabel('Interval (sec)')
plt.ylabel('Occurrence')
plt.savefig(data_folder_path/exp_date/'Histogram_Pull.png',dpi=300)
# %%
plt.plot([30,45,60,90],mean_interval,'o-')
plt.xlabel('Shell diameter (mm)')
plt.ylabel('Average interval between slips (sec)')
plt.savefig(data_folder_path/exp_date/'MeanInt_Push.png',dpi=300)
# %%
plt.plot([30,45,60,90],std_interval,'o-')
plt.xlabel('Shell diameter (mm)')
plt.ylabel('STD of interval between slips (sec)')
plt.savefig(data_folder_path/exp_date/'STDInt_Push.png',dpi=300)
# %% Energy release
clr_list = ['#e41a1c','#377eb8','#4daf4a','#984ea3']

i = 0
for exp_no in [5, 3, 7, 1]:
    data_sample = data_table['Friction'][exp_no]
    diff_sample = np.diff(data_sample)
    ipt = np.where(np.abs(diff_sample) > 5)[0]
    energy_release = diff_sample[ipt]

    # n, bins, patches = plt.hist(0.25*np.diff(ipt),
    #     bins=range(0,50,2),
    #     label=data_table['Diameter'][exp_no],
    #     alpha=0.5,
    #     density=True,
    #     stacked=True,
    #     color=clr_list[i])
    # plt.plot(np.linspace(1,47,24),n,'o-',color=clr_list[i])

    i = i + 1

plt.legend()
plt.xlabel('Interval (sec)')
plt.ylabel('Occurrence')
# data_folder_path = Path('/Users/yeonsu/Dropbox (Harvard University)/Stick-slip/Experiment-data')

# fig_label = '%s_%s.png'%(data_table['Diameter'][exp_no],data_table['Direction'][exp_no])
plt.savefig(data_folder_path/exp_date/'Histogram_Push.png',dpi=300)

# %%
data_table.iloc[3]


# %%
# import matlab
import matlab.engine
eng = matlab.engine.start_matlab()
# %%
b = matlab.double(data_sample.tolist())
# ipt = eng.findchangepts()

# %%
ipt = eng.findchangepts(b,'MaxNumChanges',10)
eng.size(ipt)

ipt_py = np.array(ipt)[0].astype('int') + 1
# %%
plt.figure(figsize=(20,5))
plt.plot(data_sample,'.-')
plt.plot(ipt_py,data_sample[ipt_py],'o')



# %% Slip event
import ruptures as rpt

algo = rpt.Dynp(model="l2").fit(data_sample)
result = algo.predict(n_bkps=100)

print(result)
# %%
ipt_rupture = np.array(result)-1
# %%
plt.figure(figsize=(20,5))
plt.plot(data_sample)
plt.plot(ipt_rupture,data_sample[ipt_rupture],'o')

# %%
# examples
# generate signal
n_samples, dim, sigma = 1000, 3, 4
n_bkps = 100  # number of breakpoints
signal, bkps = rpt.pw_constant(n_samples, dim, n_bkps, noise_std=sigma)
# detection
algo = rpt.Pelt(model="rbf").fit(signal)
result = algo.predict(pen=10)
# display
rpt.display(signal, bkps, result)
plt.show()


# %%
t_points
friction_data


# The onset
# frequency
# Energe release (we didn't measure distance...)