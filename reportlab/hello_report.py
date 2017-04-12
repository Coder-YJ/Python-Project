# -*- coding: utf-8 -*-
# build in 2017/4/12 by QianYuanJing
from reportlab.graphics.shapes import Drawing,String
from reportlab.graphics import renderPDF

d = Drawing(100,100)
s = String(50,50,'Hello World!',textAnchor = 'middle')

d.add(s)

renderPDF.drawToFile(d,'hello.pdf','A simple PDF file')
print('done')