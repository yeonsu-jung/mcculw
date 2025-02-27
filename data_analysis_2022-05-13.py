# %%
import numpy as np
from matplotlib import pyplot as plt
# %%
class data_analyzer:
    def __init__(self,paths):
        self.pull1 = np.loadtxt(paths[0],delimiter=',')
        self.pull2 = np.loadtxt(paths[1],delimiter=',')
        self.push1 = np.loadtxt(paths[2],delimiter=',')
        self.push2 = np.loadtxt(paths[3],delimiter=',')

        # self.backward_data1 = np.loadtxt(paths[4],delimiter=',') # 0.1 mm/s
        # self.backward_data2 = np.loadtxt(paths[5],delimiter=',') # 0.1 mm/s
        # self.backward_data3 = np.loadtxt(paths[6],delimiter=',') # 0.1 mm/s

        self.zeros = np.array([2.15488281,0.49443359])

    def get_zeros(self):
        self.zeros = np.mean(self.zeroing_data,axis=0)

    def show_raw_data(self):
        # plt.plot(self.zeroing_data)
        fig, axs = plt.subplots(2)
        axs[0].plot(self.push1[:,0] - self.zeros[0],label='push')
        axs[1].plot(self.push2[:,0] - self.zeros[0])

        axs[0].plot(self.pull1[:,0] - self.zeros[0],label='pull')
        axs[1].plot(self.pull2[:,0] - self.zeros[0])

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
exp_id_30mm = ['21-55','21-59','21-34','21-39']
exp_id_45mm = ['22-22','22-26','22-10','22-16']
exp_id_60mm = ['16-32','16-37','16-45','16-50']
exp_id_90mm = ['22-36','22-41','22-46','22-51']

paths_30mm = []
paths_45mm = []
paths_60mm = []
paths_90mm = []
for i in range(4):
    paths_30mm.append(f'examples/console/LoadCellLog_2022-05-12_{exp_id_30mm[i]}.csv')
    paths_45mm.append(f'examples/console/LoadCellLog_2022-05-12_{exp_id_45mm[i]}.csv')
    paths_60mm.append(f'examples/console/LoadCellLog_2022-05-12_{exp_id_60mm[i]}.csv')
    paths_90mm.append(f'examples/console/LoadCellLog_2022-05-12_{exp_id_90mm[i]}.csv')

# %%
da30 = data_analyzer(paths_30mm)
da30.show_raw_data()
da45 = data_analyzer(paths_45mm)
da45.show_raw_data()
da60 = data_analyzer(paths_60mm)
da60.show_raw_data()
da90 = data_analyzer(paths_90mm)
da90.show_raw_data()
# %%
from scipy.fft import fft, ifft
# %%
import numpy as np

# %%
t = np.arange(0,1000*0.25,0.25)

# %%
xx = da90.pull2[:,0]
sp = np.fft.fft(xx - np.mean(xx))
freq = np.fft.fftfreq(1000,0.25)

xx = da90.pull2[:,0]
sp = np.fft.fft(xx - np.mean(xx))
freq = np.fft.fftfreq(1000,0.25)

xx = da90.pull2[:,0]
sp = np.fft.fft(xx - np.mean(xx))
freq = np.fft.fftfreq(1000,0.25)

xx = da90.pull2[:,0]
sp = np.fft.fft(xx - np.mean(xx))
freq = np.fft.fftfreq(1000,0.25)

plt.plot(freq,sp.real)
# %%
t = np.arange(256)
freq = np.fft.fftfreq(t.shape[-1])


freq = np.fft.fftfreq(da30.pull1[:,0])
plt.plot(freq, sp.real, freq, sp.imag)

plt.show()

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