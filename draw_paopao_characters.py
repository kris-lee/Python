# code for drawing retangles in the paopao pictures which contain characters according the ROI stored in txt in the form of json 
# auth : Li zhichao
# data : 2016-9-29

# 1.解析json语言，获取ROI值和字符内容
# 2.根据ROI值，画出矩形框
# 3.将所有的字符内容保存至txt文件中


# -*- coding:utf-8 -*-
import os
import json
import sys
import os,shutil
from PIL import Image, ImageDraw


def get_information(txt_path):
	lines = open(txt_path).readlines()
	invaid_img_list = []
	sp = open(save_path, 'wb')
	for line in lines:
		python_line = json.loads(line)
		boxs_info = python_line['boxs']
		if len(boxs_info) == 0:
			invaid_img_info = 'img: ' + python_line['img']
			invaid_img_list.append(invaid_img_info)
		else:
			img_ID = python_line['img']
			shutil.copy(src_path + img_ID, img_path + img_ID)
			pos_list = [[] for i in range(len(boxs_info))]
			for RID in range(len(boxs_info)):
				ROI_pos = boxs_info[RID]['vertexs']
				for posID in range(len(ROI_pos)):
					pos_list[RID].append(int(ROI_pos[posID]['x']))
					pos_list[RID].append(int(ROI_pos[posID]['y']))
				pos_list[RID].append(int(ROI_pos[0]['x']))
				pos_list[RID].append(int(ROI_pos[0]['y']))

			draw_picture(img_ID, pos_list)

			img_info = 'img_ID:%s\n' % img_ID
			sp.write(img_info)
			for RID in range(len(pos_list)):
				if boxs_info[RID].has_key('content'):
					ROI_info = boxs_info[RID]['content']
					line = '	%s %s\n' % (pos_list[RID], ROI_info.encode('utf-8'))
				else:
					line = '	%s\n' % pos_list[RID]
				sp.write(line)

	sp.close()

	print 'invaid_img: ',invaid_img_list


def draw_picture(img_ID, pos_list):
	im = Image.open(img_path + img_ID)
	draw = ImageDraw.Draw(im)
	for RID in range(len(pos_list)):
		draw.line(pos_list[RID], fill = (255,0,0), width = 2)
	im.save(img_path + img_ID)

if __name__ == '__main__':
	txt_path = 'data/paopao_subtitle.txt'
	src_path = 'data/paopao_picture/'
	img_path = 'data/paopao_picture_draw/'
	save_path = 'data/paopao_subtitle_information.txt'
	if os.path.exists(img_path):
		shutil.rmtree(img_path)
	os.mkdir(img_path)
	get_information(txt_path)

