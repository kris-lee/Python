# code for transform the OCR result(with json form) producted by baidu to personal form
# auth : Li zhichao
# data : 2016-11-4

# 将OCR识别结果分成四类：
# 1、未能识别出的图片
# 2、能识别出，并且没有字幕的图片
# 3、能识别出，并且只有一组字幕的图片
# 4、能识别出，并且有多组字幕的图片


# -*- coding:utf-8 -*-
import os
import json
import sys
import os,shutil


def get_information(txt_list_path):
	txt_list = []
	for root, dir, files in os.walk(txt_list_path):
		for txt_name in files:
			filename = os.path.join(root, txt_name)
			txt_list.append(filename)
	
	fp = open(fail_save_path, 'wb')
	np = open(no_save_path, 'wb')
	op = open(one_save_path, 'wb')
	mp = open(more_save_path, 'wb')

	for filename in txt_list:
		lines = open(filename, 'rb').readlines()
		for line in lines:
			len_split = len(line.split())
			if len_split == 0:
				print 'line is null\n'
				continue
			abspath = line.split()[0]
			img_ID = abspath[abspath.rfind('/')+1:]
			label_line = line[len(line.split()[0]):]
			if 'html' in label_line:
				print 'new_line: %s......subtitle fail recognize\n' % img_ID
				fail_img_name = '%s\n' % img_ID
				fp.write(fail_img_name)
				continue	
			json_line = json.loads(label_line)
			ret_info = json_line.get('ret', 'None')
			rect_with_word_sum = ''
			if ret_info == 'None' or len(ret_info) == 0:
				print 'new_line: %s......no subtitle\n' % img_ID
				no_img_name = '%s\n' % img_ID
				np.write(no_img_name)
				continue
			for ret_info_ID in range(len(ret_info)):
				pos = ret_info[ret_info_ID]['rect']

				print 'pos:%s' % pos

				left_top_pos = '%s,%s' % (pos['left'],pos['top'])
				right_bottom_pos = '%d,%d' % (int(pos['left'])+int(pos['width']), int(pos['top'])+int(pos['height']))
				roi_pos = '[%s,%s]' % (left_top_pos, right_bottom_pos)

				print 'roi_pos:%s' % roi_pos

				word = ret_info[ret_info_ID]['word']
				rect_with_word = ' %s %s' % (roi_pos, word)
				if ret_info_ID > 0:
					rect_with_word = ' ;' + rect_with_word
				rect_with_word_sum = rect_with_word_sum + rect_with_word
						
			new_line = '%s%s\n' % (img_ID, rect_with_word_sum.encode('utf-8'))
			print 'new_line: %s' % new_line
			if len(ret_info) == 1:
				op.write(new_line)
			else:
				mp.write(new_line)	
	
	np.close()
	op.close()
	mp.close()




if __name__ == '__main__':
	txt_list_path = '/data/baidu_subtitle_txt_list/'
	fail_save_path = '/data/baidu_information_fail_subtitle.txt' 
	no_save_path = '/data/baidu_information_no_subtitle.txt'
	one_save_path = '/data/baidu_information_one_subtitle.txt'
	more_save_path = '/data/baidu_information_more_subtitle.txt'
	get_information(txt_list_path)

