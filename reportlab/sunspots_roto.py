# -*- coding: utf-8 -*-
# build in 2017/4/12 by QianYuanJing
from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF

data =[
    # Year Month Predicted High Low
      (2007,8,113.2,114.2,112.2),
	  (2007,9,119.2,184.2,192.2),
	  (2007,10,113.2,154.2,182.2),
	  (2007,11,123.2,114.2,112.2),
	  (2007,12,113.2,114.2,112.2),
	  (2008,1,133.2,164.2,112.2),
	  (2008,2,153.2,114.2,112.2),
	  (2008,3,113.2,114.2,112.2),
      ]

drawing = Drawing(200,150)

pred = [row[2]-40 for row in data]
high = [row[3]-40 for row in data]
low = [row[4]-40 for row in data]
times = [200*((row[0] + row[1] / 12.0) - 2007)-110 for row in data]

tp = [(tp[0],tp[1]) for tp in zip(times,pred)]
th = [(tp[0],tp[1]) for tp in zip(times,high)]
tl = [(tp[0],tp[1]) for tp in zip(times,low)]

drawing.add(PolyLine(tp, strokeColor = colors.blue))
drawing.add(PolyLine(th, strokeColor = colors.red))
drawing.add(PolyLine(tl, strokeColor = colors.green))
drawing.add(String(65,115,'sunspots',fontSize = 18, fillcolor = colors.red))

renderPDF.drawToFile(drawing, 'report1.pdf','sunspots')