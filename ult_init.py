#Run execfile("ult_init.py")

from nanonis_load import didv

import sys

sys.path.append(r'C:\Users\ULT\Desktop')
sys.path.append(r'C:\Users\ULT\Documents\Python Library')

import ult_instruments.Python.triton_monitor
import ult_instruments.Python.keithley2400
import ult_instruments.Python.impedance_heater

import ult_instruments.Python.mercuryIPS

# print("Please select the appropriate command:")
# print("init_lockin()")
# print("init_gate()")
# print("init_second_gate()")
# print("init_triton()")
# print("init_magnet()")
# print("init_temperature()")

def init_lockin():
    global lockin
    import ult_instruments.Python.sr830_lockin
    lockin = ult_instruments.Python.sr830_lockin.lockin()
    print("Object lockin is now available.\nExample commands:")
    print("lockin.set_amplitude(FLOAT)")
    print("lockin.set_frequency(FLOAT)")

def init_gate():
    global gate_source
    gate_source = ult_instruments.Python.keithley2400.keithley2400(com_port = 'COM6', max_voltage = 10, listen_port = 65432, increment = 0.1)
    gate_source._print = False
    gate_source.header_error_time = 2
    print("Object gate_source is now available.")
    print("This module can be controlled via LabVIEW.")

def init_second_gate():
    global second_gate
    second_gate = ult_instruments.Python.keithley2400.keithley2400(com_port = 'COM4', max_voltage = 2, listen_port = 61112, increment = 0.5)
    second_gate._print = False
    second_gate.header_error_time = 2
    print("Object second_gate is now available.")
    print("This module can be controlled via LabVIEW.")

def init_temperature():
    global triton_monitor
    try:
        triton_monitor
    except NameError:
        triton_monitor = ult_instruments.Python.triton_monitor.triton_monitor(IP_address, port)
        print("Starting temperature monitor...")
    triton_monitor.listen(32541)

def init_triton(get_user_input=False):
    print("Starting the automatic 1K pot monitor...")
    global triton_monitor
    global heater_keithley
    global impedance_heater
    global triton_stop
    try:
        triton_monitor
    except NameError:
        triton_monitor = ult_instruments.Python.triton_monitor.triton_monitor(IP_address, port)
    try:
        heater_keithley
    except NameError:
        heater_keithley = ult_instruments.Python.keithley2400.keithley2400(com_port = 'COM3', max_voltage = 15, listen_port = None)
    try:
        impedance_heater
    except:
        impedance_heater = ult_instruments.Python.impedance_heater.impedance_heater(triton_monitor, heater_keithley, log_directory)
    impedance_heater.start(get_user_input=get_user_input)
    try:
        triton_stop
    except:
        def triton_stop():
            impedance_heater.stop_loop()

def init_magnet():
    global magnet
    try:
        magnet
    except NameError:
        magnet = ult_instruments.Python.mercuryIPS.mercuryIPS()
    magnet.start_listen()
    print("Remote magnet controller enabled")
    print("Example commands:")
    print("magnet.z.hold()")
    print("magnet.z.switch_heater_on()")
    print("magnet.z.set_target_field(1.0)")

IP_address = '128.112.85.130'
port = 33576
log_directory = 'C:\\Log\\'
