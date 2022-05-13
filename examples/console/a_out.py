"""
File:                       ULAO01.py

Library Call Demonstrated:  mcculw.ul.a_out()

Purpose:                    Writes to a D/A Output Channel.

Demonstration:              Sends a digital output to D/A 0.

Other Library Calls:        mcculw.ul.from_eng_units()

Special Requirements:       Device must have a D/A converter.
"""
from __future__ import absolute_import, division, print_function
from builtins import *  # @UnusedWildImport


from mcculw import ul
from mcculw.device_info import DaqDeviceInfo

try:
    from console_examples_util import config_first_detected_device
except ImportError:
    from .console_examples_util import config_first_detected_device



def run_example(speed = 0.1):    # speed in mm/s
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
        print(data_value)
        
        raw_value = ul.from_eng_units(board_num, ao_range, data_value)
        print(raw_value)
        print('Hello')

        try:
            ul.a_out(board_num, channel, ao_range, raw_value)
        except Exception as e:
            print('\n', e)
        
    except Exception as e:
        print('\n', e)      

    

if __name__ == "__main__":
    run_example(0.5)
    
