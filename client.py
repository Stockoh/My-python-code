#!/usr/bin/env python3

import socket
import sys

HOST = 'localhost'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = bytes(input("S>"), "utf-8")
        s.sendall(data)
        data2 = str(s.recv(1024), "utf-8")
        if not data or data.lower() == "end":
            sys.exit()
        if not data2 or data2.lower() == "end":
            sys.exit()
        print(f"C>{data2}")
