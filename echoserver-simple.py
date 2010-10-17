#!/usr/bin/env python

"""
A simple echo server
"""

import socket
import json

host = ''
port = 5000
backlog = 5
size = 2048
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
while 1:
    client, address = s.accept()
    data="asda"
    while data:
        print data
        try:
            a = json.loads(data)
            print a['executable']
        except ValueError, e:
            print
            print data
        data = client.recv(size)
    client.close()
