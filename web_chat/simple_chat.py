#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build in 2017/4/19 by QianYuanJing
from asyncore import dispatcher
from asynchat import async_chat
import socket,asyncore

PORT = 5005
NAME = 'TestChat'

class ChatSession(async_chat):
    '''
    处理服务器和一个用户之间连接的类
    '''
    def __init__(self,server,sock):
        #标准设置任务
        
        async_chat.__init__(self,sock)
        self.server = server
        self.set_terminator("\r\n")  #以换行符作为结束符
        self.data = []
        #问候用户
        print('ChatSession -- __init__  befor self.push')
#        self.push('Welecome to %s\r\n')#% self.server.name)
        print('ChatSession -- __init__')
        
    def collect_incoming_data(self,data):
        self.data.append(data)
        print('ChatSession -- collect_incoming_data')
        
    def found_terminator(self):
        '''
        如果发现一个终止对象，那就意味着读入了一个完整的行，将其广播给每个人
        '''
        line = ''.join(self.data)
        self.data = []
        self.server.broadcast(line)
        print(line)
        print('ChatSession -- found_terminator')
    
    def handle_close(self):
        async_chat.handle_close(self)
        self.server.disconnect(self)
        
class ChatServer(dispatcher):
    '''
    接受连接并产生单个会话的类，它还会处理到其他会话的广播
    '''
    def __init__(self,port,name):
        #standard setup tasks
        print('ChatServer -- __init__')
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('',port))
        self.listen(5)
        self.name = name
        self.sessions = []
       
    def disconnect(self,session):
        print('ChatServer -- disconnect')
        self.sessions.remove(session)
    
    def broadcast(self,line):
        print('ChatServer -- broadcast')        
        for session in self.sessions:
            session.push(line + '\r\n')
    
    def handle_accept(self):
        print('ChatServer -- handle_accept')                
        conn,addr = self.accept()
        self.sessions.append(ChatSession(self,conn))
        print('Connection attempt from ',addr[0])
        
if __name__ == '__main__':
    s = ChatServer(PORT,NAME)
    try:asyncore.loop()
    except KeyboardInterrupt:print()