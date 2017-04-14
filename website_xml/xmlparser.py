#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build in 2017/4/14 by QianYuanJing
from xml.sax.handler import ContentHandler
from xml.sax import parse

class headlineHandler(ContentHandler):
    in_headline = False
    def __init__(self,headlines):
        ContentHandler.__init__(self)
        self.headlines = headlines
        self.data = []
        
    def startElement(self,name,attrs):
        if name == 'h1':
            self.in_headline = True
            
    def endElement(self,name):
        if name == 'h1':
            text = ''.join(self.data)
            self.data = []
            self.headlines.append(text)
            self.in_headline = False
         
    def characters(self,string):
        if self.in_headline:
            self.data.append(string)
           
headlines = []
parse('website.xml',headlineHandler(headlines))

print('The following <h1> elements were found')
for h in headlines:
    print(h)