# %%
import numpy as np
from matplotlib import pyplot as plt
# %%
class data_analyzer:
    def __init__(self,paths):
        self.zeroing_data = np.loadtxt(paths[0],delimiter=',')
        self.forward_data1 = np.loadtxt(paths[1],delimiter=',') # 0.1 mm/s
        self.forward_data2 = np.loadtxt(paths[2],delimiter=',') # 0.3 mm/s
        self.forward_data3 = np.loadtxt(paths[3],delimiter=',') # 1 mm/s

        self.backward_data1 = np.loadtxt(paths[4],delimiter=',') # 0.1 mm/s
        self.backward_data2 = np.loadtxt(paths[5],delimiter=',') # 0.1 mm/s
        self.backward_data3 = np.loadtxt(paths[6],delimiter=',') # 0.1 mm/s

        self.zeros = np.mean(self.zeroing_data,axis=0)

    def get_zeros(self):
        self.zeros = np.mean(self.zeroing_data,axis=0)        

    def show_raw_data(self):
        # plt.plot(self.zeroing_data)
        fig, axs = plt.subplots(2)
        axs[0].plot(self.forward_data1[:,0] - self.zeros[0],label='0.1 mm/s')
        axs[1].plot(self.backward_data1[:,0] - self.zeros[0])

        axs[0].plot(self.forward_data2[:,0] - self.zeros[0],label='0.3 mm/s')
        axs[1].plot(self.backward_data2[:,0] - self.zeros[0])

        axs[0].plot(self.forward_data3[:,0] - self.zeros[0],label='1 mm/s')
        axs[1].plot(self.backward_data3[:,0] - self.zeros[0])

        fig.legend()

    def find_slips(self,threshold=-0.05):
        # diff = np.where(np.abs(np.diff(self.backward_data1[:,0])) > 0.1)
        diff = np.where(np.diff(self.backward_data1[:,0]) < threshold)
        xx = np.linspace(0,0.25*3000,len(self.backward_data1[:,0]))
        # print(diff)
        fig,axs = plt.subplots(2)
        axs[0].plot(xx,(self.backward_data1[:,0] - self.zeros[0])/0.0785 ,label='Friction')
        axs[0].plot(xx[diff[0]], (self.backward_data1[diff[0],0] - self.zeros[0])/0.0785,'o')

        axs[1].plot(xx,(-self.backward_data1[:,1] + self.zeros[1])/0.0109 ,label='Normal')
        axs[1].plot(xx[diff[0]],(-self.backward_data1[diff[0],1] + self.zeros[1])/0.0109,'o')

        plt.xlabel('Time (sec)')
        plt.ylabel('Force (gf)')

        slip_amplitude = ((self.backward_data1[diff[0],0] - self.backward_data1[diff[0]+1,0]))/0.0785
        emitted_energy = 1

        return slip_amplitude

    def find_slips2(self,threshold=-0.05):
        # diff = np.where(np.abs(np.diff(self.backward_data1[:,0])) > 0.1)
        diff = np.where(np.diff(self.backward_data1[:,0]) < threshold)
        xx = np.linspace(0,0.25*3000,len(self.backward_data1[:,0]))
        # print(diff)
        fig,axs = plt.subplots(2)
        axs[0].plot(xx,(self.backward_data1[:,0] - self.zeros[0])/0.0785 ,label='Friction')
        axs[0].plot(xx[diff[0]], (self.backward_data1[diff[0],0] - self.zeros[0])/0.0785,'o')

        axs[1].plot(xx,(-self.backward_data1[:,1] + self.zeros[1])/0.0109 ,label='Normal')
        axs[1].plot(xx[diff[0]],(-self.backward_data1[diff[0],1] + self.zeros[1])/0.0109,'o')

        plt.xlabel('Time (sec)')
        plt.ylabel('Force (gf)')

        slip_amplitude = ((self.backward_data1[diff[0],0]- self.zeros[0]))/0.0785
        emitted_energy = 1

        return slip_amplitude
    
    def find_slips3(self,threshold=-0.05):
        # diff = np.where(np.abs(np.diff(self.backward_data1[:,0])) > 0.1)
        diff = np.where(np.diff(self.forward_data1[:,0]) < threshold)
        xx = np.linspace(0,0.25*3000,len(self.forward_data1[:,0]))
        # print(diff)
        fig,axs = plt.subplots(2)
        axs[0].plot(xx,(self.forward_data1[:,0] - self.zeros[0])/0.0785 ,label='Friction')
        axs[0].plot(xx[diff[0]], (self.forward_data1[diff[0],0] - self.zeros[0])/0.0785,'o')

        axs[1].plot(xx,(-self.forward_data1[:,1] + self.zeros[1])/0.0109 ,label='Normal')
        axs[1].plot(xx[diff[0]],(-self.forward_data1[diff[0],1] + self.zeros[1])/0.0109,'o')

        plt.xlabel('Time (sec)')
        plt.ylabel('Force (gf)')

        slip_amplitude = ((self.backward_data1[diff[0],0] - self.backward_data1[diff[0]+1,0]))/0.0785
        emitted_energy = 1

        return slip_amplitude

    def show_data1(self):
        # plt.plot(self.zeroing_data)
        fig, axs = plt.subplots(2)
        axs[0].plot(-self.forward_data1[:,0] + self.zeros[0],label='Forward')
        axs[1].plot(self.backward_data1[:,0] - self.zeros[0],label='Backward')

        # axs[0].set_ylim((0, 0.35))
        # axs[1].set_ylim((0, 0.35))
        fig.legend()
    
    

    
# %%
exp_id_30mm = ['09-58','10-08','10-13','10-32','10-25','10-19','10-28']
exp_id_45mm = ['11-34','12-27','11-45','12-40','12-08','11-51','12-43']
exp_id_60mm = ['10-38','10-47','10-52','11-08','10-58','11-03','11-12']
exp_id_90mm = ['12-46','13-16','12-55','13-42','13-33','13-00','13-45']

paths_30mm = []
paths_45mm = []
paths_60mm = []
paths_90mm = []
for i in range(7):
    paths_30mm.append(f'examples/console/LoadCellLog_2022-04-01_{exp_id_30mm[i]}.csv')
    paths_45mm.append(f'examples/console/LoadCellLog_2022-04-01_{exp_id_45mm[i]}.csv')
    paths_60mm.append(f'examples/console/LoadCellLog_2022-04-01_{exp_id_60mm[i]}.csv')
    paths_90mm.append(f'examples/console/LoadCellLog_2022-04-01_{exp_id_90mm[i]}.csv')

# %%
da = data_analyzer(paths_60mm)
da.get_zeros()
da.show_raw_data()
da.show_data1()

# %%
da30 = data_analyzer(paths_30mm)
da30.show_data1()
da45 = data_analyzer(paths_45mm)
da45.show_data1()
da60 = data_analyzer(paths_60mm)
da60.show_data1()
da90 = data_analyzer(paths_90mm)
da90.show_data1()
# %%
da30 = data_analyzer(paths_30mm)
da30.show_data1()
da30.find_slips()
# %%
amp30 = da30.find_slips(threshold=-0.05)
amp45 = da45.find_slips(threshold=-0.05)
# amp60 = da60.find_slips(threshold=-0.1)
amp90 = da90.find_slips(threshold=-0.05)

print(np.mean(amp30),np.mean(amp45),np.mean(amp90))
# %%
amp30 = da30.find_slips3(threshold=-0.05)
amp45 = da45.find_slips3(threshold=-0.05)
amp90 = da90.find_slips3(threshold=-0.05)

print(np.mean(amp30),np.mean(amp45),np.mean(amp90))
# %%
print(amp30)
# %%
tmp = np.where([0, 0, 1])
tmp[0]
# %%
test = 'examples/console/LoadCellLog_2022-03-31_16-42.csv'
test_data = np.loadtxt(test,delimiter=',')
# %%
plt.plot(test_data)

# %%
plt.plot(zeroing_data)
average = np.mean(zeroing_data,axis=0)

plt.plot(forward_data)
plt.plot(backward_data)

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

# %%
xx = [30, 45, 90]
yy = [1.5321195373784777, 2.5219853850607987, 1.2526677459306441]

plt.plot(xx,yy,'o-')
plt.xlabel('Diameter (mm)')
plt.ylabel('Slip amplitude (gf)')