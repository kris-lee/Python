# code for getting news subtitle from Excel 
# auth : Li zhichao
# data : 2016-11-16


# -*- coding: utf-8 -*-
import xlrd
import xlwt
import os
from datetime import date,datetime

def get_info(excel_path):
	news_list = []
	nt = open(news_info_txt, 'wb')
	for root, dir, files in os.walk(excel_path):
		for news_excel in files:
			filename = os.path.join(root, news_excel)
			news_list.append(filename)
	
	for news_excel in news_list:
		workbook = xlrd.open_workbook(news_excel)		
		for sheet_name in workbook.sheet_names():
			sheet = workbook.sheet_by_name(sheet_name)
			# col_values(6) is the column where news subtitles store 
			contents = sheet.col_values(6)
			for i in range(1,len(contents)):
				if contents[i]:
					contents_info = contents[i].replace(' ','')
					print 'line: %s' %  contents_info.encode('utf-8')
					line = '%s\n' % contents_info.encode('utf-8')
					nt.write(line)
	nt.close()


if __name__ == "__main__":
	excel_path = '/data/news_list/'
	news_info_txt = '/data/news_info.txt'
	get_info(excel_path)
