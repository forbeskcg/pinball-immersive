
# Server program to handle communicate between multiple microcontrollers
#
# Author: Andrew Merrill
# Version: 0.9,  May 2026

'''
Usage:
    Run this program on a host computer (running Linux or MacOS) 
    Attach each client board to the host via a USB cable
    
    We maintain a dictionary of keys and values stored this server
    Clients can store values for different keys
    Clients can ask for the current value of a key
    Clients can also send messages to each other

    Each client is identified by a 1 byte ID number, chosen by the client (who is responsible for avoiding duplicates)

    When this program starts up, it will automatically send a HELLO packet to each client
    Each client will automatically reply with a HELLO as well, so the server can tell which client is on which port

Packet format: 1 byte source idnum, 1 byte packet kind, 1 byte length of payload, then payload

keys are strings (in utf-8), no more than 250 bytes (and usually much shorter than that!)
values are integers (4 byte, little endian, signed)

packet types sent by clients:

1 : HELLO  (no payload)
10 : STORE value (payload is key and value), given value replaces existing value for this key
11 : ADD value (payload is key and value to add), given value is added to existing value for this key
12 : MULTIPLY value (payload is key and value to multiply), given value is multiplied by existing value for this key
20 : REQUEST value (payload is key), server will respond with response packet containing current value of key
21 : WATCH key (payload is key), server will send response packet with current value of key whenever the value is set or changed
30 : SEND a message to another client (payload is destination, key, and value)
31 : BROADCAST a message to all clients (payload is key and value)

packet types sent by server:

1 : HELLO  (no payload)
100 : RESPONSE sent by server in response to REQUEST or WATCH (payload is key and value)
101 : MESSAGE forwarded by server from a SEND or BROADCAST packet (payload is key and value)

'''

#########################################################################

import serial  # pip3 install pyserial
import time
import os.path
import select
import platform
import pathlib

###########################################################################################

# Find all data serial ports

if platform.system() == 'Darwin':  # MacOS
    dev_dir = pathlib.Path('/dev')
    serial_devices = list(dev_dir.glob('cu.usbmodem*3'))
    serial_devices = [str(p) for p in serial_devices]
    print(serial_devices)
elif platform.system() == 'Linux':  # Linux
    dev_dir = pathlib.Path('/dev')
    serial_devices = list(dev_dir.glob('ttyACM*[13579]'))
    serial_devices = [str(p) for p in serial_devices]
    print(serial_devices)

#ports = ['/dev/cu.usbmodem11403', '/dev/cu.usbmodem11103']

###########################################################################################

# packet_kind
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

serial_data_list = []
for device in serial_devices:
    if os.path.exists(device):
        serial_port = serial.Serial(device)
        serial_data_list.append(serial_port)

        # say hello to each client, so they know the server is up and running
        hello_packet = bytes([0, HELLO, 0])
        serial_port.write(hello_packet)

source_ids = {}  

stored_values = {}  # key is a KEY string, value is a VALUE integer

watchers = {}  # key is a KEY string, value is a set of id numbers of clients watching this key

#################################################################################################

# Sends a packet to a client
# arguments:
#   packet_kind: a one-byte number (should be either HELLO, RESPONSE, or MESSAGE)
#   destination: the id number of the client that should receive this message
#   key: a string
#   value: an integer

def sendOutgoingPacket(packet_kind, destination, key, value):
    print(f"sending packet kind {packet_kind} to {destination} key {key} has value {value}")
    if destination in source_ids:
        payload = key.encode("utf-8") + value.to_bytes(4, byteorder='little', signed=True)
        packet = bytes([0, packet_kind, len(payload)]) + payload
        serial_data = source_ids[destination]
        serial_data.write(packet)
    else:
        print(f"destination {destination} is unknown")

#################################################################################################

def run() -> None:
    while True:

        # wait for incoming data
        (readable, writeable, exceptional) = select.select(serial_data_list, [], [], None)
        for indata in readable:
            header = indata.read(3)
            sender = header[0]
            packet_kind = header[1]
            payload_length = header[2]
            if payload_length > 0:
                payload = indata.read(payload_length)
            else:
                payload = None

            print(f"received from {sender} packet kind {packet_kind} length {payload_length} payload {payload}")

            source_ids[sender] = indata

            if packet_kind == HELLO:
                print(f"client {sender} says hello")
            
            elif packet_kind == STORE or packet_kind == ADD or packet_kind == MULTIPLY:
                key_length = payload_length - 4
                key = payload[0:key_length].decode('utf-8')
                value = int.from_bytes(payload[-4:], byteorder='little', signed=True)
                if packet_kind == STORE or key not in stored_values:
                    stored_values[key] = value
                    print(f"client {sender} says to set '{key}' to {value}")
                elif packet_kind == ADD:
                    stored_values[key] += value
                    print(f"client {sender} says to add {value} to '{key}', new value is {stored_values[key]}")
                elif packet_kind == MULTIPLY:
                    stored_values[key] *= value
                    print(f"client {sender} says to multiply '{key}' by {value}, new value is {stored_values[key]}")
                if key in watchers:
                    for watcher_id in watchers[key]:
                        sendOutgoingPacket(RESPONSE, watcher_id, key, stored_values[key])

            elif packet_kind == REQUEST:
                key = payload.decode('utf-8')
                print(f"client {sender} is requesting value of '{key}'")
                if key in stored_values:
                    sendOutgoingPacket(RESPONSE, sender, key, stored_values[key])

            elif packet_kind == WATCH:
                key = payload.decode('utf-8')
                print(f"client {sender} is watching '{key}'")
                if key not in watchers:
                    watchers[key] = set()
                watchers[key].add(sender)
                if key in stored_values:
                    sendOutgoingPacket(RESPONSE, sender, key, stored_values[key])

            elif packet_kind == SEND:
                destination = payload[0]
                key_length = payload_length - 5
                key = payload[1:key_length+1].decode('utf-8')
                value = int.from_bytes(payload[-4:], byteorder='little', signed=True)
                print(f"client {sender} says send '{key}' is {value} to client {destination}")
                sendOutgoingPacket(MESSAGE, destination, key, value)

            elif packet_kind == BROADCAST:
                key_length = payload_length - 4
                key = payload[0:key_length].decode('utf-8')
                value = int.from_bytes(payload[-4:], byteorder='little', signed=True)
                print(f"client {sender} says broadcast '{key}' is {value} to everyone")
                for destination in source_ids:
                    sendOutgoingPacket(MESSAGE, destination, key, value)

        #time.sleep(0.05)
