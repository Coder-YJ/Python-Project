#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build in 2017/4/14 by QianYuanJing

from xml.sax.handler import ContentHandler
from xml.sax import parse
import os

class Dispathcer:
    def dispatch(self,prefix,name,attrs=None):
        mname = prefix + name.capitalize()
        dname = 'default' + prefix.capitalize()
        method = getattr(self,mname,None)
#        args = ()
        if callable(method):agrs = ()
        else:
            method = getattr(self,dname,None)
            args = name,
        if prefix == 'start': args += attrs,
        if callable(method):method(args)
    def startElement(self,name,attrs):
        self.dispatch('start',name,attrs)
    def endElement(self,name,attrs):
        self.dispatch('end',name)
                
class WebsiteConstructor(Dispathcer,ContentHandler):
    passthrough = False
    def __init__(self,directory):
        self.directory = [directory]
        self.ensureDirectory()    
    def ensureDirectory(self):
        path = os.path.join(*self.directory)
        if not os.path.isdir(path):os.makedirs(path)
    def characters(self,chars):
        if self.passthrough:self.out.write(chars)
    def defaultStart(self,name):
        if self.passthrough:
            self.out.write('<' + name)
            for key,val in attrs.items():
                self.out.write('%s="%s"'%(key,val))
            self.out.write('>')
    def defaultEnd(self,name):
        if self.passthrough:
            self.out.write('</%s>'%name)        
    def startPage(self,attrs):
        print('Beginning Page',attrs['name'])
    def endPage(self):
        print('Ending Page')
    def defaultStart(self,name):
        if self.passthrough:
            self.out.write('<' + name)
            for key,val in attrs.items():
                self.out.write('%s="%s"'%(key,val))
            self.out.write('>')
    def defaultEnd(self,name):
        if self.passthrough:
            self.out.write('</%s>'%name)
    def startDirectory(self,attrs):
        self.directory.append(attrs)
        self.ensureDirectory()
    def endDirectory(self,attrs):
        self.directory.pop()    
    def startPage(self,attrs):
        print(attrs.items())
        filename = os.path.join(*self.directory+[attrs['name']+'.html'])
        self.out = open(filename,'w')
        self.writeHeader(attrs['title'])
        self.passthrough = True
    def endPage(self):
        self.passthrough = False
        self.writFooter()
        self.out.close()        
    def writeHeader(self,title):
        self.out.write('<html>\n <head>\n <title>')
        self.out.write('title')
        self.out.write('</title>\n </head>\n <body>\n')
    def writeFooter(self):
        self.out.write('\n </body>\n</html>\n')

parse('website.xml',WebsiteConstructor('public_html'))        
    
