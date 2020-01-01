#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
sys.path.append("/home/aman/.local/lib/python3.7/site-packages")

import bitstring
import pygatt
import numpy as np
from time import time, sleep
from sys import platform


class Muse():
    """Muse 2016 headband"""

    def __init__(self, address=None, callback=None,acc_data=None,gyro_data=None, eeg=True, accelero=False,
                 giro=False, backend='auto', interface=None, time_func=time,
                 name=None):
        """Initialize"""
        self.address = address
        self.name = name
        self.callback = callback
        self.acc_data = acc_data
        self.gyro_data = gyro_data
        self.eeg = eeg
        self.accelero = accelero
        self.giro = giro
        self.interface = interface
        self.time_func = time_func
        self.last_tm = 0
        self.device = None
        self.adapter = None

        if backend in ['auto', 'gatt', 'bgapi']:
            if backend == 'auto':
                if platform == "linux" or platform == "linux2" or platform == "darwin":
                    self.backend = 'gatt'
                else:
                    self.backend = 'bgapi'
            else:
                self.backend = backend
        else:
            raise(ValueError('Backend must be auto, gatt or bgapi'))

    def connect(self, interface=None, backend='auto'):
        """Connect to the device"""
 
        if self.backend == 'gatt':
            self.interface = self.interface or 'hci0'
            self.adapter = pygatt.GATTToolBackend(self.interface)
        else:
            self.adapter = pygatt.BGAPIBackend(serial_port=self.interface)

        self.adapter.start()

        if self.address is None:
            address = self.find_muse_address(self.name)
            if address is None:
                raise(ValueError("Can't find Muse Device"))
            else:
                self.address = address
        self.device = self.adapter.connect(self.address)

        # subscribes to EEG stream
        if self.eeg:
            self._subscribe_eeg()

        # subscribes to Accelerometer
        if self.accelero:
            self._subscribe_acc()
            # raise(NotImplementedError('Accelerometer not implemented'))

        # subscribes to Giroscope
        if self.giro:
            self._subscribe_gyro()
            # raise(NotImplementedError('Giroscope not implemented'))

    def find_muse_address(self, name=None):
        """look for ble device with a muse in the name"""
        list_devices = self.adapter.scan(timeout=10)
        print("All devices seen: ")
        print(list_devices)

        for device in list_devices:
            print(device)

            if name:
                if device['name'] == name:
                    print('Found device %s : %s' % (device['name'], device['address']))
                    return device['address']

            elif isinstance(device.get('name', ''), str):
                if 'Muse' in device.get('name', ''):
                    print('Found device %s : %s' % (device['name'],  device['address']))
                    return device['address']

        return None

    def start(self):
        """Start streaming."""
        self._init_timestamp_correction()
        self._init_sample()
        self.last_tm = 0
        self.device.char_write_handle(0x000e, [0x04, 0x70, 0x32, 0x30, 0x0a], False)
        self.device.char_write_handle(0x000e, [0x02, 0x64, 0x0a], False)

    def stop(self):
        """Stop streaming."""
        self.device.char_write_handle(0x000e, [0x02, 0x68, 0x0a], False)

    def disconnect(self):
        """disconnect."""
        self.device.disconnect()
        self.adapter.stop()

    def _subscribe_eeg(self):
        """subscribe to eeg stream."""
        self.device.subscribe("273e0007-4c4d-454d-96be-f03bac821358", callback=self._handle_eeg)
        self.device.subscribe('273e0003-4c4d-454d-96be-f03bac821358', callback=self._handle_eeg)
        self.device.subscribe('273e0004-4c4d-454d-96be-f03bac821358', callback=self._handle_eeg)
        self.device.subscribe('273e0005-4c4d-454d-96be-f03bac821358', callback=self._handle_eeg)
        self.device.subscribe('273e0006-4c4d-454d-96be-f03bac821358', callback=self._handle_eeg)

    def _subscribe_acc(self):
        self.device.subscribe('273e000a-4c4d-454d-96be-f03bac821358',callback=self._handle_acc)

    def _subscribe_gyro(self):
        self.device.subscribe('273e0009-4c4d-454d-96be-f03bac821358', callback=self._handle_gyro)

    def _unpack_acc_channel(self, packet):
        a = bitstring.Bits(bytes=packet)
        pattern = "uint:16,uint:16,uint:16,uint:16,uint:16,uint:16,uint:16,uint:16,uint:16,uint:16"
        res = a.unpack(pattern)  # Transforma los datos en 16bit y 12 bit
        return res

    def _unpack_gyro_channel(self, packet):
        a = bitstring.Bits(bytes=packet)
        pattern = "uint:16,uint:16,uint:16,uint:16,uint:16,uint:16,uint:16,uint:16,uint:16,uint:16"
        res = a.unpack(pattern)  # Transforma los datos en 16bit y 12 bit
        return res

    def _unpack_eeg_channel(self, packet):
        """Decode data packet of one eeg channel.

        Each packet is encoded with a 16bit timestamp followed by 12 time
        samples with a 12 bit resolution.
        """
        aa = bitstring.Bits(bytes=packet)
        pattern = "uint:16,uint:12,uint:12,uint:12,uint:12,uint:12,uint:12, \
                   uint:12,uint:12,uint:12,uint:12,uint:12,uint:12"
        res = aa.unpack(pattern)
        packetIndex = res[0]
        data = res[1:]
        # 12 bits on a 2 mVpp range
        data = 0.48828125 * (np.array(data) - 2048)
        return packetIndex, data

    def _init_sample(self):
        """initialize array to store the samples"""
        self.timestamps = np.zeros(5)
        self.data = np.zeros((5, 12))

    def _init_timestamp_correction(self):
        """Init IRLS params"""
        # Initial params for the timestamp correction
        # The time it started + the inverse of sampling rate
        self.sample_index = 0
        self.reg_params = np.array([self.time_func(), 1./256])

    def _update_timestamp_correction(self, x, y):
        """Update regression for dejittering

        use stochastic gradient descent
        """
        pass

    def _handle_acc(self, handle, data):
        # Print handle,data
        if handle == 23:
            d_acc = self._unpack_acc_channel(data)
            # print
            self.acc_data(d_acc)

    def _handle_gyro(self, handle, data):
        # Print handle,data
        if handle == 20:
            d_gyro = self._unpack_gyro_channel(data)
            # Print d_acc
            self.gyro_data(d_gyro)

    def _handle_eeg(self, handle, data):
        """Calback for receiving a sample.

        sample are received in this oder : 44, 41, 38, 32, 35
        wait until we get 35 and call the data callback
        """

        timestamp = self.time_func()
        index = int((handle - 32) / 3)
        tm, d = self._unpack_eeg_channel(data)

        if self.last_tm == 0:
            self.last_tm = tm - 1

        self.data[index] = d
        self.timestamps[index] = timestamp
        # Last data received
        if handle == 35:
            if tm != self.last_tm + 1:
                print("missing sample %d : %d" % (tm, self.last_tm))
            self.last_tm = tm

            # Calculate index of time samples
            idxs = np.arange(0, 12) + self.sample_index
            self.sample_index += 12

            # Affect as timestamps
            timestamps = self.reg_params[1] * idxs + self.reg_params[0]

            # Push data
            self.callback(self.data, timestamps)
            self._init_sample()
