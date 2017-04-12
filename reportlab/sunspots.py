# -*- coding: utf-8 -*-
# build in 2017/4/12 by QianYuanJing
#from urllib import urlopen
from ftplib import FTP
from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label

drawing = Drawing(400,200)
data = []
COMMENT_CHARS = '#:'
'''
ftp = FTP('ftp.swpc.noaa.gov')
ftp.login()
ftp.cwd('pub/weekly')
fp = open('E:/Python-Project/reportlab/predict.txt','wb+')

for line in ftp.storlines('STOR Predict.txt',fp):
    if not line.isspace() and not line[0] in COMMENT_CHARS:
        data.append([float(n) for n in line.split()])
        print(data[0])
		
ftp.close()
		
'''
fp = open('E:/Python-Project/reportlab/predict.txt','r')
for line in fp.readlines():
    if not line.isspace() and not line[0] in COMMENT_CHARS:
        data.append([float(n) for n in line.split()])
#        print(data[0]) 
 
pred = [row[2] for row in data]
high = [row[3] for row in data]
low = [row[4] for row in data]
times = [(row[0] + row[1] / 12.0) for row in data]

tp = [(tp[0],tp[1]) for tp in zip(times,pred)]
th = [(tp[0],tp[1]) for tp in zip(times,high)]
tl = [(tp[0],tp[1]) for tp in zip(times,low)]

lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp.data = (tp,th,tl)
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.green

drawing.add(lp)
drawing.add(String(250,150,'Sunspots',fontSize = 14, fillColor = colors.red))
 
renderPDF.drawToFile(drawing,'report2.pdf','Sunspots')

