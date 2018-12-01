#!/usr/bin/env python3

import serial
import serial.tools.list_ports
import sys
from Edaq530Constants import ChannelTypes
from Edaq530Constants import Edaq530Converters

class Edaq530(object):

    def __init__(self, channels):
        self.port = None
        self.channels = channels

    def findDevice(self):
        ser = serial.tools.list_ports.comports()
        for item in ser:
            print(item.vid)
            if item.vid is not None and item.pid is not None:
                if hex(item.vid) == hex(0x0403) and hex(item.pid) == hex(0x6001):
                    print('Device is connected')
                    self.port = item.device

        try:
            if self.port is None:
                raise DeviceIsNotFoundError()
            return 1
        except DeviceIsNotFoundError as e:
            print(e.msg)
            sys.exit(1)

    def makeConnection(self):
        self.device = serial.Serial(port=self.port, baudrate=230400, timeout=1,
        bytesize=8, parity=serial.PARITY_NONE, stopbits=1)

    def closeConnection(self):
        self.device.close()

    """
        Az elkuldott karakternek meg kell egyeznie az erkezonek
        innen tudjuk, hogy az eszkoz csatlakoztatva van-e
        :param char elkuldendo karakter
    """
    def sendAndReceived(self, char):
        self.device.write(char.encode())
        received = self.device.read(1).decode()
        try:
            if char != received:
                raise WrongCharReceivedError(char, received)
            return received
        except WrongCharReceivedError as e:
            print(e.msg)
            print("The program stops sampling, disconnects the device and exit...")
            self.closeConnection()
            sys.exit(1)

    def setChannel(self, channels):
        self.sendAndReceived("Q")
        self.sendAndReceived("C")
        self.sendAndReceived(chr(channels[0]))
        self.sendAndReceived(chr(channels[1]))
        self.sendAndReceived(chr(channels[2]))

        self.sendAndReceived("@")
        self.sendAndReceived("E")

        if ChannelTypes.photo in channels:
            self.sendAndReceived(chr(1))
        else:
            self.sendAndReceived(chr(0))

        self.sendAndReceived("@")
        self.sendAndReceived("P")

        c = 0

        if channels[0] != ChannelTypes.resistor:
            c += 1
        if channels[1] != ChannelTypes.resistor:
            c += 2
        if channels[2] != ChannelTypes.resistor:
            c += 4
        self.sendAndReceived(chr(c))

    def measure(self):
        self.sendAndReceived("@")
        self.sendAndReceived("M")
        self.sendAndReceived("#")
        data = []
        for i in range(0, 3):
            c = self.device.read(1)
            data.append(ord(c) * 256)
            c = self.device.read(1)
            data[i] += ord(c)
        return data

    def getMesurementInCelsius(self):
        data = self.measure()
        converters = Edaq530Converters()
        dataInCelsius = converters.adcCodeToTempCelsius(data[0])
        return dataInCelsius

    def getMesurements(self):
        data = self.measure()
        return data

    def __enter__(self):
        print('Find device...')
        self.findDevice()
        print('Make connection...')
        self.makeConnection()
        print('Set channels')
        self.setChannel(self.channels)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closeConnection()


class WrongCharReceivedError(Exception):
    def __init__(self, sent, received):
        self.msg = received + " (" + str(ord(received)) + ") received instead of " + sent + " (" + str(
            ord(sent)) + ")"

class DeviceIsNotFoundError(Exception):
    def __init__(self):
        self.msg = "Device is not found, please connect or reconnect the device"
