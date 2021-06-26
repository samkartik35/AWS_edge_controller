# File name: ecc_parser_main.py
# Revision:1.A.ECC.2.IN.POWERHF

# Description: This file contains the main parser function.
# This file is run on EC2 cloud instance. It receives connectio
# from gateway devices, which are hosting sensors controller
# Gateway has different types of interfaces with sensor controller
# Sensors send messages in different message format, which is specific for 
# a controller. We are introducing this parser to read these non-standard message types
# and convert it to standard MQTT messages and send it to cloud AWS IoT core

#!/usr/bin/python3
import sys
import socket
import argparse
import threading
import time
import select

from datetime import datetime


import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import socket
import os
import datetime

PORT=8080
WAITING_FOR_DATA=1900
# Function started as a new thread for a client. 
# We listen to the client port for data. If we dont get datafor 15 minutes we close
# cleint connection gracefully
def on_new_client(client, connection, configfile, mqtt_client,end_point, debug):
        ip = connection[0]      # IP address
        port = connection[1]    # Port number
        print(f"The new connection was made from IP: {ip}, and port: {port}!")
        # A time out of 15 minutes is setup. If we dont get data within that time
        # then we close the client
        #client.settimeout(WAITING_FOR_DATA)
        mqttclientid = ""
        # Starting a timer for 10 minutes, if we dont receivve data from a socket 
        # then we will close that clinet
        while True:
            try:
                msg = client.recv(FRAME_SIZE).decode()   # Receive frame from client
                if not msg : break
                time.sleep(3)
               # below will detect if client disconnects during sleep
                r, w, e = select.select([client], [], [], 0)      # more data waiting?
               # print("select: r=%s w=%s e=%s" % (r,w,e))        # debug output to command line
                if r:                                           # yes, data avail to read.
                    t = client.recv(1024, socket.MSG_PEEK)        # read without remove from queue
                    print ("peek: len=%d, data=%s" % (len(t),t))  # debug output
                    if len(t)==0:                               # length of data peeked 0?
                        print ("Client disconnected.")            # client disconnected
                        break                                   # quit program


                # msg = client.recv(1024)   # Receive frame from client

                print("Raw Data received from Client time:",get_time_stamp())
                print(msg)
                
                
            except socket.timeout as e:
                if(debug == True):
                    print(e,':no data within timeout period: ',WAITING_FOR_DATA)
                client.close()
                mqttclientid.disconnect()
                break

        print(f"The client from ip: {ip}, and port: {port}, has gracefully diconnected!")
        client.close()

# Main function to create a socket and bind it to the host IP address.
# main loop where we wait for a client to send connection request
# We get a connection request and start a new thread to handle that client
def main():

    parser = argparse.ArgumentParser(description = "This is the server for the multithreaded socket demo!")
    parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = "")
    parser.add_argument('--port', metavar = 'port', type = int, nargs = '?', default = PORT)
    parser.add_argument('--configfile', metavar = 'configfile', type = str, nargs = '?', default = "ecc_config.txt")
    parser.add_argument('--clientid', metavar = 'clientid', type = str, nargs = '?', default = "clientid-0001")
    parser.add_argument('--endpoint', metavar = 'endpoint', type = str, nargs = '?', default ="a1jblcy2osi0b6-ats.iot.ap-south-1.amazonaws.com")
    parser.add_argument('--debug', metavar = 'debug', type = bool, nargs = '?', default = False)
    args = parser.parse_args()

    print(f"Running the server on: {args.host} and port: {args.port}")
    config_file = args.configfile
    mqtt_client = args.clientid
    debug = args.debug
    end_point = args.endpoint
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
            sck.bind((args.host, args.port))
            sck.listen(SOCK_BACKLOG)
    except Exception as e:
            raise SystemExit(f"We could not bind the server on host: {args.host} to port: {args.port}, because: {e}")
    while True:
            try:
                    client, ip = sck.accept()       # Accepting connection from client
                    threading._start_new_thread(on_new_client,(client, ip, config_file,mqtt_client,end_point, debug)) # Creating a new thread for handling client data
            except KeyboardInterrupt:
                    print(f"Gracefully shutting down the server!")
            except Exception as e:
                    print(f"Well I did not anticipate this: {e}")

    sck.close()

if __name__ == "__main__":
    main()


