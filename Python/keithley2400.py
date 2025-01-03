# keithley2400.py
# Controls Keithley 2400 SourceMeter through RS232
#
# TO DO: Message boundaries for recv over TCP.

import serial
import time

try:
    import thread
except ModuleNotFoundError:
    import _thread as thread

try:
    import Queue
except ModuleNotFoundError:
    import queue as Queue

import atexit
import socket
import traceback
import ast

class keithley2400:

    def __init__(self, com_port='COM3', max_voltage=100, listen_port=None, increment=None, read_before_write=True, baud_rate=9600, timeout=0.1):
        self.keithley = serial.Serial(com_port, baud_rate, timeout = timeout)
        self.lock = thread.allocate_lock()
        self.emergency_lock = 0
        self.MAXVOLTAGE = abs(max_voltage)
        self.listen_port = listen_port
        self.error_list = []
        self._halt = False
        
        self._default_increment = 0.1 if increment is None else increment
        self._default_increment_time = 0.01
        self.increment = increment
        self.increment_time = self._default_increment_time
        
        self._header_error_time = 0.1
        self._exception_time = 0.5
        self._print = True
        self._read_before_write = read_before_write
        
        if self.listen_port is not None:
            self._listen_flag = True
            self.queue = Queue.Queue()
            thread.start_new_thread(self._listen,())
            thread.start_new_thread(self._execute,())

        @atexit.register
        def exit_handler():
            self.keithley.close()
            if self.listen_port is not None:
                try:
                    self._listen_flag = False
                    self.lis_sock.close()
                except:
                    pass

    def _listen(self):
        try:
            host = '127.0.0.1'
            port = self.listen_port
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.lis_sock = s
            s.bind((host, port))
            s.listen(0)
        except Exception:
            err = traceback.format_exc()
            print('ERROR in LISTEN thread:')
            print(err)
            self.error_list.append(err)
        while self._listen_flag:
            try:
                conn, _ = s.accept()
                listen_string = conn.recv(1024).decode()
                if 'QUIT' in listen_string:
                    print('QUIT in listen_string')
                    conn.sendall('OK\n'.encode())
                    conn.close()
                    s.close()
                    self._listen_flag = False
                    break
                elif 'HALT' in listen_string:
                    print('HALT in listen_string')
                    conn.sendall('OK\n'.encode())
                    conn.close()
                    time.sleep(0.05)
                    self._halt = True
                else:
                    self.queue.put((listen_string, conn))
            except Exception:
                err = traceback.format_exc()
                print('ERROR in LISTEN thread:')
                print(err)
                self.error_list.append(err)
                while len(self.error_list) > 20:
                    self.error_list.pop(0)
                time.sleep(self._exception_time)
    
    def _execute(self):
        while self._listen_flag:
            try:
                listen_string, conn = self.queue.get()
                listen_commands = listen_string.split()
                listenArgs = [ast.literal_eval(argument) for argument in listen_commands[1:]]
                if listen_commands[0] in dir(self)[3:]:
                    try:
                        result = getattr(self, listen_commands[0])(*listenArgs)
                        if result is not None:
                            send_string = str(result) + '\n'
                            conn.sendall(send_string.encode())
                        else:
                            conn.sendall('NO DATA\n'.encode())
                    except (TypeError, AttributeError):
                        conn.sendall('ERROR: COMMAND ERROR\n'.encode())
                else:
                    conn.sendall('ERROR: COMMAND ERROR\n'.encode())
            except Exception:
                err = traceback.format_exc()
                print('ERROR in EXECUTE thread:')
                print(err)
                self.error_list.append(err)
                while len(self.error_list) > 20:
                    self.error_list.pop(0)
                time.sleep(self._exception_time)
            finally:
                try:
                    conn.close()
                except:
                    pass

    def write(self, command):
        self.keithley.write(command.encode())

    def read(self, size=1):
        '''Read bytes from buffer'''
        return self.keithley.read(size).decode()

    def readline(self):
        line = self.keithley.readline().decode()
        # Sometimes readline is called before the keithley has time to give a full response and an incomplete string is read.
        # The while loop here will keep calling readline() until a line feed character '\n' is received and concatenate the
        # result with the old string.
        while not '\n' in str(line):
            time.sleep(.001)
            temp = self.keithley.readline().decode()
            if not not temp: # If temp is not empty
                line = line + temp # Concatenate with original meas_array to get entire line
            if not self.keithley.in_waiting:
                break
        
        return line
    
    def read_until(self, expected='\n', size=None):
        line = self.keithley.read_until(expected=expected, size=size).decode()
        return line
    
    def set_increment(self, increment):
        if increment == 0:
            self.increment = self._default_increment
        else:
            self.increment = increment

    def set_increment_time(self, increment_time):
        if increment_time == 0:
            self.increment_time = self._default_increment_time
        else:
            self.increment_time = increment_time

    def set_max_voltage(self, max_voltage):
        self.MAXVOLTAGE = abs(max_voltage)

    def get_max_voltage(self):
        return self.MAXVOLTAGE

    def _stop_listen(self):
        self._listen_flag = False
        host = '127.0.0.1'
        port = self.listen_port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall('QUIT'.encode())
        s.close()
    
    def force_set_voltage(self, num):
        if abs(num) <= abs(self.MAXVOLTAGE):
            self.write(':SOUR:VOLT:LEV ' + str(num) + '\n')
            self.write(':SYST:KEY 23\n')
        else:
            print('For safety, I cannot allow voltages greater than ' + str(self.MAXVOLTAGE) + ' V.')

    def set_voltage(self, num, increment = None):
        self._halt = False
        if increment is None:
            increment = self.increment
            if increment is None:
                increment = 0.1
        if (num < -self.MAXVOLTAGE) or (num > self.MAXVOLTAGE):
            print('For safety, I cannot allow voltages greater than ' + str(self.MAXVOLTAGE) + ' V.')
            return
        if (increment < 0.000095):
            print('Please choose a larger increment value.')
            return
        self.lock.acquire()
        try:
            while not self._halt:
                if self.emergency_lock:
                    return
                if self._read_before_write:
                    voltage = self.force_read_voltage()
                else:
                    try:
                        voltage = next_voltage
                    except NameError:
                        voltage = self.force_read_voltage()
                if abs(num - voltage) < 1.1 * increment:
                    self.force_set_voltage(num)
                    if self._print:
                        print('VOLTAGE: ' + str(self.force_read_voltage()) + ' V')
                        print('CURRENT: ' + str(self.force_read_current()) + ' uA')
                        print('DONE')
                    break
                elif voltage > num:
                    next_voltage = voltage - increment
                    self.force_set_voltage(next_voltage)
                    if self._print:
                        print('VOLTAGE: ' + str(self.force_read_voltage()) + ' V')
                        print('CURRENT: ' + str(self.force_read_current()) + ' uA')
                    time.sleep(self.increment_time)
                elif voltage < num:
                    next_voltage = voltage + increment
                    self.force_set_voltage(next_voltage)
                    if self._print:
                        print('VOLTAGE: ' + str(self.force_read_voltage()) + ' V')
                        print('CURRENT: ' + str(self.force_read_current()) + ' uA')
                    time.sleep(self.increment_time)
        except:
            raise
        finally:
            try:
                self.write(':SYST:KEY 23\n')
            except:
                pass
            finally:
                self._halt = False
                self.lock.release()

    def force_read_voltage(self):
        counter = 0
        while True:
            try:
                self.write(':READ?\n')
                meas_array = self.readline()     
                voltage = float(meas_array.split(',')[0])
                self.write(':SYST:KEY 23\n')
                break
            except (ValueError, IndexError) as e:
                print(f"Error in force_read_voltage: {e}")
                print('HEADER ERROR DETECTED: ' + meas_array)
                if counter > 100:
                    self.force_set_voltage(0)
                    print('EMERGENCY SET VOLTAGE TO 0 V')
                    break
                counter += 1
                time.sleep(self._header_error_time)
        return voltage

    def read_voltage(self):
        self.lock.acquire()
        try:
            return self.force_read_voltage()
        except:
            raise
        finally:
            self.lock.release()

    def force_read_current(self):
        counter = 0
        while True:
            try:
                self.write('\n')
                self.write(':READ?\n')
                meas_array = self.readline()
                current = float(meas_array.split(',')[1])*1E6
                self.write(':SYST:KEY 23\n')
                break
            except (ValueError, IndexError) as e:
                print(f"Error in force_read_current: {e}")
                print('HEADER ERROR DETECTED: ' + meas_array)
                if counter > 100:
                    self.force_set_voltage(0)
                    print('EMERGENCY SET VOLTAGE TO 0 V')
                    break
                counter += 1
                time.sleep(self._header_error_time)
        return current

    def read_current(self):
        self.lock.acquire()
        try:
            return self.force_read_current()
        except:
            raise
        finally:
            self.lock.release()

    #Run voltage to 0 V in the event of an emergency.
    def run_to_zero(self):
        self.emergency_lock = 1
        self.lock.acquire()
        try:
            time.sleep(0.1)
            voltage = self.force_read_voltage()
            while not (-0.00001 < voltage < 0.00001):
                if -1 < voltage < 1:
                    self.force_set_voltage(0)
                elif voltage >= 1:
                    self.force_set_voltage(voltage - 0.1)
                    time.sleep(0.01)
                elif voltage <= -1:
                    self.force_set_voltage(voltage + 0.1)
                    time.sleep(0.01)
                voltage = self.force_read_voltage()
            self.write(':SYST:KEY 23\n')
            print('Run to 0 V complete.')
            print('Keithley SourceMeter output is now 0 V.')
        except:
            raise
        finally:
            self.lock.release()
            self.emergency_lock = 0

    def output_on(self):
        self.lock.acquire()
        try:
            self.write('OUTPUT ON\n')
            self.write(':SYST:KEY 23\n')
        except:
            raise
        finally:
            self.lock.release()

    def output_off(self):
        self.lock.acquire()
        try:
            self.write('OUTPUT OFF\n')
            self.write(':SYST:KEY 23\n')
        except:
            raise
        finally:
            self.lock.release()
