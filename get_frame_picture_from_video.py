# code for getting the frame of video based on given info stored in the form of excel with the tool of ffmpeg
# auth : Li zhichao
# data : 2016-11-24

# excel form like: 
# 节目期号	节目名	开头帧	结尾帧	主持人画面帧数						标题									标题帧		标题位置
# 20161102 四川新闻 25847		26333				26160				第十六届西博会明天上午10点开幕	26237		535.932；658x98

# 1、根据主持人帧和标题帧数，从视频中截取图片，分别存于主持人和标题文件夹下
# 2、并在标题文件夹下将标题内容、标题位置ROI保存在txt中


# -*- coding: utf-8 -*
import os
import xlrd
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

def get_picture(file, path):
	nsi = open(txt, 'wb')
	data = xlrd.open_workbook(file)
	sheet_table = data.sheets()[0]
	# get sheet[0] data info 
	news_date_table = sheet_table.col_values(0)
	host_frame_table = sheet_table.col_values(4)
	subtitle_info_table = sheet_table.col_values(5)
	subtitle_frame_table = sheet_table.col_values(6)
	subtitle_roi_table = sheet_table.col_values(7)
	#check sheet[0] every row data in news_date_table
	for i in range(1, len(news_date_table)):
		txt_line = []
		host_frame = host_frame_table[i]
		subtitle_frame = subtitle_frame_table[i]
		subtitle_roi = subtitle_roi_table[i]
		subtitle_info = subtitle_info_table[i]
		# get frame time
		# get roi value
		left_upper_point_roi = '%s,%s' % (subtitle_roi.split(';')[0].split(',')[0], subtitle_roi.split(';')[0].split(',')[1])
		right_lower_x = int(subtitle_roi.split(';')[0].split(',')[0]) + int(subtitle_roi.split(';')[1].split(u'×')[0])
		right_lower_y = int(subtitle_roi.split(';')[0].split(',')[1]) + int(subtitle_roi.split(';')[1].split(u'×')[1]) 
		right_lower_point_roi = '%s,%s' % (str(right_lower_x), str(right_lower_y))
		roi = '%s;%s' % (left_upper_point_roi, right_lower_point_roi)
		print 'roi: %s' % roi
		if news_date_table[i] != '':
			news_date = '%s' % (str(int(news_date_table[i])))
			host_file_path = base_path + news_date + '/host_capture/'
			subtitle_file_path = base_path + news_date + '/subtitle_capture/'
			if not os.path.exists(host_file_path):
				os.makedirs(host_file_path)
			if not os.path.exists(subtitle_file_path):
				os.makedirs(subtitle_file_path)
		# get frame picture
		video_file = video_path + news_date + '.flv'
		if host_frame != '简讯无主持人':
			host_jpg_name = '%s_%s.jpg' % (news_date, str(int(host_frame)))
			host_jpg_path =  host_file_path + host_jpg_name
			host_time = int(host_frame/25)
			host_command = './ffmpeg -i %s -f image2 -ss %s -vframes 1 %s' % (video_file, host_time, host_jpg_path)
			# os.system(): run the system command with the tool of ffmpeg
			os.system(host_command)
		subtitle_jpg_name = '%s_%s.jpg' % (news_date, str(int(subtitle_frame)))
		subtitle_jpg_path = subtitle_file_path + subtitle_jpg_name
		subtitle_time = int(subtitle_frame/25)
		subtitle_command = './ffmpeg -i %s -f image2 -ss %s -vframes 1 %s' % (video_file, subtitle_time, subtitle_jpg_path)
		os.system(subtitle_command)
		# save info in the txt
		subtitle_line = '%s %s %s\n' % (subtitle_jpg_name, roi, subtitle_info.encode('utf-8'))
		nsi.write(subtitle_line)
		print subtitle_line
		#raw_input()
	nsi.close()



if __name__ == '__main__':
	base_path = '/data/video_capture/'
	video_path = '/data/video_capture/'
	file = './29-30.xlsx'
	txt = './news_subtitle_info.txt'
	get_picture(file, video_path)
