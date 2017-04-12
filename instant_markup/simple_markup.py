# -*- coding: utf-8 -*-
# build in 2017/4/11 by QianYuanJing
import sys,re
from util import *

print ('<html><head><title>...</title><body>')

#f = open("E:/Python-Project/instant markup/text_input.txt")

title = True
for block in blocks(sys.stdin):
    block = re.sub(r'\*(.+?)\*',r'<em>\1</em>',block)
    if title:
        print('<hl>')
        print(block)
        print('</hl>')
        title = False
    else:
        print('<p>')
        print(block)
        print('</p>')
    
print('</body></html>')