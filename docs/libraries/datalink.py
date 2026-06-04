# Library for exchanging data with other PI Pico boats

# Author: Andrew Merrill, May 2026
# Version: 1.0

import usb_cdc
import time
import struct

'''
packet format: 1 byte source idnum, 1 byte packet kind, 1 byte length of payload, then payload

keys are strings (in utf-8)
values are integers (4 byte little endian signed)

kinds of packets sent by clients:

1 : HELLO  (no payload)
10 : STORE value (payload is key and value), given value replaces existing value for this key
11 : ADD value (payload is key and value to add), given value is added to existing value for this key
12 : MULTIPLY value (payload is key and value to multiply), given value is multiplied by existing value for this key
20 : REQUEST value (payload is key), server will respond with response packet containing current value of key
21 : WATCH key (payload is key), server will send response packet with current value of key whenever the value is set or changed
30 : SEND a message to another client (payload is destination, key, and value)
31 : BROADCAST a message to all clients (payload is key and value)

kinds of packets sent by server:

1 : HELLO  (no payload)
100 : RESPONSE sent by server in response to REQUEST or WATCH (payload is key and value)
101 : MESSAGE forwarded by server from a SEND or BROADCAST packet (payload is key and value)

'''

class Packet:

    def __init__(self, kind, sender, key, value):
        self.kind = kind
        self.sender = sender
        self.key = key
        self.value = value

    def __repr__(self):
        return f"packet kind {self.kind} from {self.sender} with key {self.key} value {self.value}"

class DataLink:

    # message types
    HELLO = 1
    STORE = 10
    ADD = 11
    MULTIPLY = 12
    REQUEST = 20
    WATCH = 21
    SEND = 30
    BROADCAST = 31
    RESPONSE = 100
    MESSAGE = 101

    def __init__(self, idnum):
        self.serialdata = usb_cdc.data
        if idnum < 1 or idnum > 255:
            raise ValueError(f"idnum {idnum} must be between 1 and 255")
        self.idnum = idnum
        self.payload = bytes([])
        self.hello()

    def hello(self):
        self._sendOutgoingPacket(self.HELLO)

    def store(self, key, value):
        self._addStringPayload("key", key)
        self._addIntegerPayload("value", value)
        self._sendOutgoingPacket(self.STORE)

    def add(self, key, value):
        self._addStringPayload("key", key)
        self._addIntegerPayload("value", value)
        self._sendOutgoingPacket(self.ADD)

    def multiply(self, key, value):
        self._addStringPayload("key", key)
        self._addIntegerPayload("value", value)
        self._sendOutgoingPacket(self.MULTIPLY)

    def request(self, key):
        self._addStringPayload("key", key)
        self._sendOutgoingPacket(self.REQUEST)

    def watch(self, key):
        self._addStringPayload("key", key)
        self._sendOutgoingPacket(self.WATCH)

    def send(self, destination, key, value):
        self._addBytePayload("destination", destination)
        self._addStringPayload("key", key)
        self._addIntegerPayload("value", value)
        self._sendOutgoingPacket(self.SEND)

    def broadcast(self, key, value):
        self._addStringPayload("key", key)
        self._addIntegerPayload("value", value)
        self._sendOutgoingPacket(self.BROADCAST)

    ##########################################################

    def hasPacket(self):
        return self.serialdata.in_waiting > 0

    def getPacket(self):
        if self.serialdata.in_waiting == 0:
            return None
        else:
            header = self.serialdata.read(3)
            sender = header[0]
            packet_kind = header[1]
            payload_length = header[2]
            if payload_length > 0:
                payload = self.serialdata.read(payload_length)
                key_length = payload_length - 4
                key = payload[0:key_length].decode('utf-8')
                #value = int.from_bytes(payload[-4:], byteorder='little', signed=True)  # signed=True not supported in CircuitPython, ugh!
                value = struct.unpack('<i', payload[-4:])[0]  # replacement for the unimplemented from_bytes with signed=True
            else:
                key = None
                value = None
            if packet_kind == self.HELLO:
                self._sendOutgoingPacket(self.HELLO)

            return Packet(packet_kind, sender, key, value)

    ##########################################################


    def _addStringPayload(self, label, string):
        if type(string) is not str:
            raise TypeError(f"{label} {string} must be a string")
        self.payload += string.encode("utf-8")

    def _addIntegerPayload(self, label, number):
        if type(number) is not int:
            raise TypeError(f"{label} {number} must be an integer")
        self.payload += number.to_bytes(4, byteorder='little', signed=True)

    def _addBytePayload(self, label, number):
        if type(number) is not int:
            raise TypeError(f"{label} {number} must be an integer")
        if number < 0 or number > 255:
            raise ValueError(f"{label} {number} must be between 0 and 255")
        self.payload += bytes([number])

    def _sendOutgoingPacket(self, packet_kind):
        packet = bytes([self.idnum, packet_kind, len(self.payload)]) + self.payload
        self.payload = bytes([])
        self.serialdata.write(packet)

