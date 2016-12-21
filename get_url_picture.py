# code for downloading the paopao picture from LAN with the tool of urllib
# auth : Li zhichao
# data : 2016-9-19

# -*- coding:utf-8 -*-
import os
import sys
import urllib
import xdrlib ,sys
import xlrd

def get_picture(allfile):
	count = 0
	for file in allfile:
		xls = xlrd.open_workbook(file)
		sheet = xls.sheets()[0]
		col = sheet.col_values(5)
		for line in col:
			if line.strip():
				file_path = save_path + '%d.jpg' % count
				try:
					picture = urllib.urlopen(line).read()
					count = count + 1
					f = open(file_path,'wb')
					f.write(picture)
					f.close()
				except Exception as err:
					print err,line

def getfile(src_path):  
	filelist = os.listdir(src_path)  
	allfile = []
	for filename in filelist:  
		filepath = os.path.join(src_path,filename)  
		allfile.append(filepath)
	get_picture(allfile)




if __name__ == '__main__':
	src_path = 'data/documents/'
	save_path = '/data/Download_Picture/'
	getfile(src_path)
