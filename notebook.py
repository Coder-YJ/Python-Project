'''
1������urlopen��ȡFTP�������е�txt�ļ������Զ������ļ��洢�ģ������ȡ������Ӧ�����ݱ����������'utf-8'�ķ�ʽ��ȡ.
   ����ɲο�Python-Project/reportlab/sunspots
'''
#����url��ftp��������ȡ�ļ�
file = urlopen('ftp://ftp.swpc.noaa.gov/pub/weekly/Predict.txt')
lines = file.readlines()

fp = open('E:/Python-Project/reportlab/predict1.txt','wb')
fp.writelines(lines)
fp.flush()
fp.close()
fp = open('E:/Python-Project/reportlab/predict1.txt','r',encoding = 'utf-8')