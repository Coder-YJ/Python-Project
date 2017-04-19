#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build in 2017/4/19 by QianYuanJing
from asyncore import dispatcher
import socket,asyncore

port = 5005
class ChatServer(dispatcher):
    def __init__(self,port):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('',port))
        self.listen(5)
    def handle_accept(self):
        conn,addr = self.accept()
        print('Connection attempt from ',addr[0])
        
if __name__ == '__main__':
    s = ChatServer(port)
    try:asyncore.loop()
    except KeyboardInterrupt:pass

