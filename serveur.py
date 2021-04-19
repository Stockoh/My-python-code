#!/usr/bin/env python3

import socket
import sys

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = str(conn.recv(1024), "utf-8")
            if not data or data.lower() == "end":
                sys.exit()
            print(f"S>{data}")
            conn.sendall(bytes(input("C>"), "utf-8"))
