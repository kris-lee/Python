# code for getting the paopao pictures where store in the Iqiyi LAN based on the form of url stored in excel form
# auth : Li zhichao
# data : 2016-11-30

# excel line: 1357878066	2467734231		2		http://d.yunpan.qiyi.virtual/ext/paopao/?token=eJxjYGBgmCy26DoDGLh4AgAWmgKw&authtype=passport&authtoken=ddFsl6BKJ1j1k6QfrunprnspgbXH8m2RMXbFaWThvm2J6oMm49b&type=photo_1000&face=0


# -*- coding: utf-8 -*
import os
import xlrd
import string
import sys
import urllib
import string

def get_paopao_picture(src_path):
	excel_list = []
	for root, dir, files in os.walk(src_path):
		for file in files:
			filename = os.path.join(root, file)
			excel_list.append(filename)
	url_contents = []
	for excel_path in excel_list:
		dirname = excel_path[:excel_path.rfind('/')]
		new_file = des_path + dirname[dirname.rfind('/')+1:dirname.rfind('_')] + '/'
		if not os.path.exists(new_file):
			os.mkdir(new_file)
		workbook = xlrd.open_workbook(excel_path)
		# URL stored in the sheet 0 in the col of 5
		sheet_table = workbook.sheets()[0]
		picture_url_table = sheet_table.col_values(5)[2:]
		url_contents.extend(picture_url_table)
	url_count = 0
	file_count = 0
	if not os.path.exists(new_file + str(file_count)):
		os.mkdir(new_file + str(file_count))
	for i in range(1, len(url_contents)):
		url = url_contents[i]
		# handle exception
		try:
			# read the url and download the paopao picture with the tool of urllib
			picture = urllib.urlopen(url).read()
			url_count = url_count + 1
			f = open(new_file + '%d/%d.jpg' % (file_count, url_count),'wb')
			f.write(picture)
			f.close()
			# 2000 pictures store in a documents
			if url_count % 2000 == 0:
				file_count = file_count + 1
				os.mkdir(new_file + str(file_count))
		except Exception as err:
			print err,url

if __name__ == '__main__':
	base_path = '/data/'
	src_path = base_path + 'paopao_picture_excel/'
	des_path = base_path + 'paopao_picture_download/'
	get_paopao_picture(src_path)
