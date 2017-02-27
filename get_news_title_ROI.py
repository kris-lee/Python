# code for getting the ROI(position) of news title from picture and storing filename and value of ROI in the txt
# auth : Li zhichao
# data : 2017-2-27

import os
import cv2
import shutil

def get_news_title_picture(src_path):
	img_list = []
	for root, dir, files in os.walk(src_path):
		for img_name in files:
			filename = os.path.join(root, img_name)
			img_list.append(filename)

	close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(50, 50))
	for img_path in img_list:
		img_name = img_path[img_path.rfind('/')+1:]
		print 'img_name: %s' % img_name
		src_img = cv2.imread(img_path)
		img_height, img_width, channels = src_img.shape
		print 'img_height: %s , img_width: %s' % (img_height, img_width)
		width_region_min = 0
		width_region_max = 630
		height_region_min = 0
		height_region_max = 0
		sum = 0
		if img_height == 360:
			width_region_min = 178
			height_region_min = 288
			height_region_max = 315
		else:
			width_region_min = 130
			height_region_min = 384
			height_region_max = 420
		copy_img = src_img.copy()
		crop_img = src_img[height_region_min : height_region_max, width_region_min : width_region_max]

		gray_img = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
		ret, threshold_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

		cv2.imwrite(copy_path + img_name, threshold_img)

		crop_height, crop_width = threshold_img.shape
		print 'height: %s , crop_width: %s' %  (crop_height, crop_width)
		
		width_begin = 0
		width_end = 0
		shift = 5
		for i in range(0, crop_width):
			sum = 0
			for j in range(0, crop_height):
				sum = sum + threshold_img[j,i]
			if (sum > 0):
				width_begin = width_region_min + i
				break

		for i in range(crop_width-1,0,-1):
			sum = 0
			for j in range(0, crop_height):
				sum = sum + threshold_img[j,i]
			if (sum > 0):
				print 'sum: %d' % (sum/255)
				width_end = width_region_max - (crop_width-i)
				break
		
		print 'begin: (%s,%s), end: (%s,%s)' % (width_begin, height_region_min,width_end, height_region_max)
		cv2.rectangle(copy_img,(width_begin-shift, height_region_min),(width_end+shift, height_region_max),(255,255,255),1)
		cv2.imwrite(copy_path + img_name, copy_img)
		line = '%s\t%s,%s;%s,%s\n' % (img_name, width_begin-shift, height_region_min, width_end+shift, height_region_max)
		f = open(copy_path + 'info.txt', 'a')
		f.write(line)
		f.close()
		
		#raw_input()

if __name__ == "__main__":
	copy_path = '/data/news_draw/'
	path = '/data/news_title_picture/' 
	get_news_title_picture(path)
