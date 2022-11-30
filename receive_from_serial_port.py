#!/usr/bin/python3

import serial
import time
import json
import pymongo
from pymongo import MongoClient

# Connect to the mongoDB sever local network to store database
def MongoDB_Connection(hostname_strval, username_strval, password_strval, port_val):
    client_connection = None
    try:
        client_connection = MongoClient(
            host = hostname_strval, #establishes connection to the host and port (27017), from docker
            username = username_strval,
            password = password_strval,
            port= port_val)
    except Error as err:
        return (f"Error: '{err}'")
    return client_connection

# Serial Port STM32 receibe dataset
def Serial_Connection(port_stval, baudrate_val, bytesize_par, parity_par, stopbits_par, rtscts_bool, timeout_val):
    serial_port = None
    try:
        serial_port = serial.Serial(port= port_stval,
                            baudrate= baudrate_val,
                            bytesize= bytesize_par,
                            parity= parity_par,
                            stopbits= stopbits_par,
                            rtscts= rtscts_bool,
                            timeout= timeout_val)
    except Error as err:
        return (f"Error: '{err}'")
    return serial_port

client = MongoDB_Connection("192.168.1.60","CAMMS","labserverpass",27017)

# Connect to a particular db
my_db = client["nasa-sr-camms-db"] # Important ---> In MongoDB, a database is not created until it gets content!
# To create a collection in MongoDB
my_col = my_db["MassSpectrometerCollection"] # Important ---> In MongoDB, a collection is not created until it gets content!


serial_port = Serial_Connection("/dev/ttyACM0", 115200, serial.SEVENBITS, serial.PARITY_ODD, serial.STOPBITS_TWO, True, 40.0)
print("Port Status:", serial_port.is_open)

while (serial_port.is_open):
    received_raw_data = serial_port.readline()  # raw data we receive
    json_string = received_raw_data[3:-3] # clear duffer data b'\x00jsonSTRINGDATA \r\n'
    json_string = json_string.replace("'", "\"") # we send json as single quotes we need double quotes in order for json package to function
    json_data = json.loads(json_string) # parse json_string with datatype dict
    #To insert a record, or document as it is called in MongoDB, into a collection, we use the insert_one() method.
    insert_result = my_col.insert_one(json_data)
    print(insert_result.inserted_id)

serial_port.close()
