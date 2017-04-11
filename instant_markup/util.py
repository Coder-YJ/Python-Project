# -*- coding: utf-8 -*-
# build in 2017/4/11 by QianYuanJing

def lines(file):
    for line in file:yield line
    yield '\n'
        
def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []