'''
1、利用urlopen读取FTP服务器中的txt文件后是以二进制文件存储的，若想读取数据则应将数据保存后重新以'utf-8'的方式读取.
   具体可参考Python-Project/reportlab/sunspots
'''
#利用url从ftp服务器读取文件
file = urlopen('ftp://ftp.swpc.noaa.gov/pub/weekly/Predict.txt')
lines = file.readlines()

fp = open('E:/Python-Project/reportlab/predict1.txt','wb')
fp.writelines(lines)
fp.flush()
fp.close()
fp = open('E:/Python-Project/reportlab/predict1.txt','r',encoding = 'utf-8')