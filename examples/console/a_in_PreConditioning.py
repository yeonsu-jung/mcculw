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

import numpy as np
from matplotlib import pyplot as plt

try:
    from console_examples_util import config_first_detected_device
except ImportError:
    from .console_examples_util import config_first_detected_device


def run_example(rate = 10000,points_per_channel = 2000):
    # By default, the example detects and displays all available devices and
    # selects the first device listed. Use the dev_id_list variable to filter
    # detected devices by device ID (see UL documentation for device IDs).
    # If use_device_detection is set to False, the board_num variable needs to
    # match the desired board number configured with Instacal.
    use_device_detection = True
    dev_id_list = []
    board_num = 0    
    memhandle = None

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
        # high_chan = min(3, ai_info.num_chans - 1)
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

        # Start the scan
        ul.a_in_scan(
            board_num, low_chan, high_chan, total_count,
            rate, ai_range, memhandle, scan_options)

        print('Scan completed successfully. Data:')

        # Create a format string that aligns the data in columns
        row_format = '{:>5}' + '{:>10}' * num_chans

        # Print the channel name headers
        labels = ['Index']
        for ch_num in range(low_chan, high_chan + 1):
            labels.append('CH' + str(ch_num))
        print(row_format.format(*labels))

        # Print the data
        data_index = 0
        data_all = []
        data_all_num = np.zeros((points_per_channel,2))
        for index in range(points_per_channel):
            display_data = [index]
            for k in range(num_chans):
                if ScanOptions.SCALEDATA in scan_options:
                    # If the SCALEDATA ScanOption was used, the values
                    # in the array are already in engineering units.
                    eng_value = ctypes_array[data_index]
                else:
                    # If the SCALEDATA ScanOption was NOT used, the
                    # values in the array must be converted to
                    # engineering units using ul.to_eng_units().
                    eng_value = ul.to_eng_units(
                        board_num, ai_range, ctypes_array[data_index])
                data_index += 1
                display_data.append('{:.3f}'.format(eng_value))
                data_all_num[index][k] = eng_value
            # Print this row
            # print(row_format.format(*display_data))
            # data_all.append(row_format.format(*display_data))            

        # Write a file
        file_name = 'test.csv'

        with open(file_name, 'w') as f:
            print('Writing data to ' + file_name, end='')

            # Write a header to the file
            for chan_num in range(low_chan, high_chan + 1):
                f.write('Channel ' + str(chan_num) + ',')
            f.write(u'\n')

            for index in range(points_per_channel):                
                for k in range(num_chans):
                    f.write('%s'%data_all[k])
                    f.write(u'\n')

        plt.plot(data_all_num)
        plt.show()
        
    except Exception as e:
        print('\n', e)
    finally:
        if memhandle:
            # Free the buffer in a finally block to prevent a memory leak.
            ul.win_buf_free(memhandle)
        if use_device_detection:
            ul.release_daq_device(board_num)
    
    print(np.mean(data_all_num,axis=0))

    return data_all_num
# %%
import tkinter as tk
from tkinter import messagebox
from mcculw.ul import ULError

import sys
sys.path.append("../ui")

try:
    from ui_examples_util import UIExample, show_ul_error
except ImportError:
    from .ui_examples_util import UIExample, show_ul_error

class ULAI06(UIExample):
    def __init__(self, master=None):
        super(ULAI06, self).__init__(master)
        # By default, the example detects all available devices and selects the
        # first device listed.
        # If use_device_detection is set to False, the board_num property needs
        # to match the desired board number configured with Instacal.
        use_device_detection = True
        self.board_num = 0

        try:
            if use_device_detection:
                self.configure_first_detected_device()

            self.device_info = DaqDeviceInfo(self.board_num)
            self.ai_info = self.device_info.get_ai_info()
            if self.ai_info.is_supported:
                self.create_widgets()
            else:
                self.create_unsupported_widgets()
        except ULError:
            self.create_unsupported_widgets(True)
    
    def create_widgets(self):
        '''Create the tkinter UI'''
        self.device_label = tk.Label(self)
        self.device_label.pack(fill=tk.NONE, anchor=tk.NW)
        self.device_label["text"] = ('Board Number ' + str(self.board_num)
                                     + ": " + self.device_info.product_name
                                     + " (" + self.device_info.unique_id + ")")

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.X, anchor=tk.NW)

        curr_row = 0
        if self.ai_info.num_chans > 1:
            channel_vcmd = self.register(self.validate_channel_entry)

            low_channel_entry_label = tk.Label(main_frame)
            low_channel_entry_label["text"] = "Low Channel Number:"
            low_channel_entry_label.grid(
                row=curr_row, column=0, sticky=tk.W)

            self.low_channel_entry = tk.Spinbox(
                main_frame, from_=0,
                to=max(self.ai_info.num_chans - 1, 0),
                validate='key', validatecommand=(channel_vcmd, '%P'))
            self.low_channel_entry.grid(
                row=curr_row, column=1, sticky=tk.W)

            curr_row += 1
            high_channel_entry_label = tk.Label(main_frame)
            high_channel_entry_label["text"] = "High Channel Number:"
            high_channel_entry_label.grid(
                row=curr_row, column=0, sticky=tk.W)

            self.high_channel_entry = tk.Spinbox(
                main_frame, from_=0, validate='key',
                to=max(self.ai_info.num_chans - 1, 0),
                validatecommand=(channel_vcmd, '%P'))
            self.high_channel_entry.grid(
                row=curr_row, column=1, sticky=tk.W)
            initial_value = min(self.ai_info.num_chans - 1, 3)
            self.high_channel_entry.delete(0, tk.END)
            self.high_channel_entry.insert(0, str(initial_value))

            curr_row += 1

        self.results_group = tk.LabelFrame(
            self, text="Results", padx=3, pady=3)
        self.results_group.pack(fill=tk.X, anchor=tk.NW, padx=3, pady=3)

        self.results_group.grid_columnconfigure(1, weight=1)

        curr_row = 0
        status_left_label = tk.Label(self.results_group)
        status_left_label["text"] = "Status:"
        status_left_label.grid(row=curr_row, column=0, sticky=tk.W)

        self.status_label = tk.Label(self.results_group)
        self.status_label["text"] = "Idle"
        self.status_label.grid(row=curr_row, column=1, sticky=tk.W)

        curr_row += 1
        index_left_label = tk.Label(self.results_group)
        index_left_label["text"] = "Index:"
        index_left_label.grid(row=curr_row, column=0, sticky=tk.W)

        self.index_label = tk.Label(self.results_group)
        self.index_label["text"] = "-1"
        self.index_label.grid(row=curr_row, column=1, sticky=tk.W)

        curr_row += 1
        count_left_label = tk.Label(self.results_group)
        count_left_label["text"] = "Count:"
        count_left_label.grid(row=curr_row, column=0, sticky=tk.W)

        self.count_label = tk.Label(self.results_group)
        self.count_label["text"] = "0"
        self.count_label.grid(row=curr_row, column=1, sticky=tk.W)

        curr_row += 1
        self.inner_data_frame = tk.Frame(self.results_group)
        self.inner_data_frame.grid(
            row=curr_row, column=0, columnspan=2, sticky=tk.W)

        self.data_frame = tk.Frame(self.inner_data_frame)
        self.data_frame.grid()

        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, side=tk.RIGHT, anchor=tk.SE)

        self.start_button = tk.Button(button_frame)
        self.start_button["text"] = "Start"
        self.start_button["command"] = self.start
        self.start_button.grid(row=0, column=0, padx=3, pady=3)

        self.quit_button = tk.Button(button_frame)
        self.quit_button["text"] = "Quit"
        self.quit_button["command"] = self.master.destroy
        self.quit_button.grid(row=0, column=1, padx=3, pady=3)
# %%
ULAI06(master=tk.Tk()).mainloop()           

# %%
# need to control motion from here

data_all = run_example()

# %%
avg_values = np.mean(data_all,axis=0)
print(avg_values)

# %%
plt.plot(data_all - avg_values)
plt.show()
# %%
data_all = run_example(rate=10000,points_per_channel=20000)

plt.plot(data_all - avg_values)
plt.show()
# %%
