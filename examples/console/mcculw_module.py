# %%
"""
File:                       a_in_scan_foreground.py

Library Call Demonstrated:  mcculw.ul.a_in_scan() in Foreground mode

Purpose:                    Scans a range of A/D Input Channels and stores
                            the sample data in an array.

Demonstration:              Displays the analog input on up to four channels.

Other Library Calls:        mcculw.ul.win_buf_alloc()
                                or mcculw.ul.win_buf_alloc_32
                                or mcculw.ul.scaled_win_buf_alloc()
                            mcculw.ul.win_buf_free()
                            mcculw.ul.to_eng_units()
                            mcculw.ul.release_daq_device()

Special Requirements:       Device must have an A/D converter.
                            Analog signals on up to four input channels.
"""
from __future__ import absolute_import, division, print_function
from builtins import *  # @UnusedWildImport

from ctypes import cast, POINTER, c_double, c_ushort, c_ulong

from mcculw import ul
from mcculw.enums import ScanOptions
from mcculw.device_info import DaqDeviceInfo

import time

try:
    from console_examples_util import config_first_detected_device
except ImportError:
    from .console_examples_util import config_first_detected_device

from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime

class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        if self.name:
            print('[%s]' % self.name,)
        print('Elapsed: %s' % (time.time() - self.tstart))

def scan_and_average(rate = 20000, points_per_channel = 1000, num_chunks = 100,offset=(0.,0.)):
    # By default, the example detects and displays all available devices and
    # selects the first device listed. Use the dev_id_list variable to filter
    # detected devices by device ID (see UL documentation for device IDs).
    # If use_device_detection is set to False, the board_num variable needs to
    # match the desired board number configured with Instacal.
    use_device_detection = True
    dev_id_list = []
    board_num = 0    
    memhandle = None
    now = datetime.now()
    exp_date = now.strftime("%Y-%m-%d")
    exp_time = now.strftime("%H-%M")
    print(f'Experiment date: {exp_time}')

    try:
        if use_device_detection:
            config_first_detected_device(board_num, dev_id_list)
        daq_dev_info = DaqDeviceInfo(board_num)
        if not daq_dev_info.supports_analog_input:
            raise Exception('Error: The DAQ device does not support '
                            'analog input')
        print('\nActive DAQ device: ', daq_dev_info.product_name, ' (',
              daq_dev_info.unique_id, ')\n', sep='')
        ai_info = daq_dev_info.get_ai_info()


        low_chan = 0
        high_chan = 1
        num_chans = high_chan - low_chan + 1
        total_count = points_per_channel * num_chans
        ai_range = ai_info.supported_ranges[0]
        scan_options = ScanOptions.FOREGROUND
        if ScanOptions.SCALEDATA in ai_info.supported_scan_options:
            # If the hardware supports the SCALEDATA option, it is easiest to
            # use it.
            scan_options |= ScanOptions.SCALEDATA
            memhandle = ul.scaled_win_buf_alloc(total_count)
            # Convert the memhandle to a ctypes array.
            # Use the memhandle_as_ctypes_array_scaled method for scaled
            # buffers.
            ctypes_array = cast(memhandle, POINTER(c_double))
        elif ai_info.resolution <= 16:
            # Use the win_buf_alloc method for devices with a resolution <= 16
            memhandle = ul.win_buf_alloc(total_count)
            # Convert the memhandle to a ctypes array.
            # Use the memhandle_as_ctypes_array method for devices with a
            # resolution <= 16.
            ctypes_array = cast(memhandle, POINTER(c_ushort))
        else:
            # Use the win_buf_alloc_32 method for devices with a resolution > 16
            memhandle = ul.win_buf_alloc_32(total_count)
            # Convert the memhandle to a ctypes array.
            # Use the memhandle_as_ctypes_array_32 method for devices with a
            # resolution > 16
            ctypes_array = cast(memhandle, POINTER(c_ulong))

        # Note: the ctypes array will no longer be valid after win_buf_free is
        # called.
        # A copy of the buffer can be created using win_buf_to_array or
        # win_buf_to_array_32 before the memory is freed. The copy can be used
        # at any time.

        # Check if the buffer was successfully allocated
        if not memhandle:
            raise Exception('Error: Failed to allocate memory')
        
        data_index = 0
        data_all = []        
        data_all_num = np.zeros((points_per_channel,2))
        averaged_data = np.zeros((num_chunks,num_chans))
        iter = 0
        
        with Timer('Scan'):
            while iter < num_chunks:                     
                ul.a_in_scan(
                board_num, low_chan, high_chan, total_count,
                rate, ai_range, memhandle, scan_options)
                
                for index in range(points_per_channel):
                    for data_index in range(num_chans):
                        eng_value = ul.to_eng_units(
                            board_num, ai_range, ctypes_array[data_index])

                        data_all_num[index][data_index] = eng_value - offset[data_index]
                
                averaged_data[iter,:] = np.mean(data_all_num,axis=0)
                iter = iter + 1

        # print(np.mean(averaged_data,axis=0))
        
        date_time = now.strftime("%Y-%m-%d_%H-%M")                
        folder_name = f"C:/Users/yjung/Dropbox (Harvard University)/Stick-slip/Experiment-data/{exp_date}"        

        file_name = f"{folder_name}/LoadCellLog_{date_time}.csv"
        try:
            np.savetxt(file_name, averaged_data, delimiter=",",fmt='%.8f')
        except:
            import os
            os.mkdir(folder_name)
            np.savetxt(file_name, averaged_data, delimiter=",",fmt='%.8f')

        print(f'Data saved in {file_name}')

        fig, axs = plt.subplots(2)
        axs[0].plot(averaged_data[:,0])
        axs[1].plot(averaged_data[:,1])
        plt.show()
        plt.savefig(f"{folder_name}/LoadCellLog_{date_time}.png")

        print(np.mean(averaged_data,axis=0))
        # with open(file_name, 'w') as f:
        #     print('Writing data to ' + file_name, end='')            
        
    except Exception as e:
        print('\n', e)
    finally:
        if memhandle:
            # Free the buffer in a finally block to prevent a memory leak.
            ul.win_buf_free(memhandle)
        if use_device_detection:
            ul.release_daq_device(board_num)
# %%
def set_speed(speed = 0.1):
    # By default, the example detects all available devices and selects the
    # first device listed.
    # If use_device_detection is set to False, the board_num property needs
    # to match the desired board number configured with Instacal.
    use_device_detection = True
    dev_id_list = []
    board_num = 0    
    memhandle = None

    try:
        if use_device_detection:
            config_first_detected_device(board_num, dev_id_list)

        device_info = DaqDeviceInfo(board_num)

        if not device_info.supports_analog_output:
            raise Exception('Error: The DAQ device does not support '
                            'analog output')

        print('\nActive DAQ device: ', device_info.product_name, ' (',
              device_info.unique_id, ')\n', sep='')        
        
        ao_info = device_info.get_ao_info()

        low_chan = 0        
        high_chan = 0
        # num_chans = high_chan - low_chan + 1
        ao_range = ao_info.supported_ranges[0]        

        channel = low_chan
        ao_range = ao_info.supported_ranges[0]
        
        T = 1000/speed # microseconds
        data_value = 4*(T-12000)/(400-12000) # volts    
        
        raw_value = ul.from_eng_units(board_num, ao_range, data_value)
       

        try:
            ul.a_out(board_num, channel, ao_range, raw_value)
        except Exception as e:
            print('\n', e)
        
    except Exception as e:
        print('\n', e)      

def fast_carry():
    # By default, the example detects all available devices and selects the
    # first device listed.
    # If use_device_detection is set to False, the board_num property needs
    # to match the desired board number configured with Instacal.
    use_device_detection = True
    dev_id_list = []
    board_num = 0    
    memhandle = None

    try:
        if use_device_detection:
            config_first_detected_device(board_num, dev_id_list)

        device_info = DaqDeviceInfo(board_num)

        if not device_info.supports_analog_output:
            raise Exception('Error: The DAQ device does not support '
                            'analog output')

        print('\nActive DAQ device: ', device_info.product_name, ' (',
              device_info.unique_id, ')\n', sep='')        
        
        ao_info = device_info.get_ao_info()

        low_chan = 0        
        high_chan = 0
        # num_chans = high_chan - low_chan + 1
        ao_range = ao_info.supported_ranges[0]        

        channel = low_chan
        ao_range = ao_info.supported_ranges[0]
        
        T = 1000/speed # microseconds
        data_value = 4*(T-12000)/(400-12000) # volts    
        
        raw_value = ul.from_eng_units(board_num, ao_range, data_value)
       

        try:
            ul.a_out(board_num, channel, ao_range, raw_value)
        except Exception as e:
            print('\n', e)
        
    except Exception as e:
        print('\n', e)      
# %%
