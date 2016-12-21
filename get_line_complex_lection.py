# code for processing sutra lection with opencv.
# auth : Li zhichao
# data : 2016-12-13

# 垂直切割经文的步骤
# 1、对图片进行灰度化，二值化
# 2、对二值化去除部分噪点，减少噪点对后面水平、垂直方向投影的影响
# 3、水平方向投影，确定经文的位置，去除边缘条纹
# 4、垂直方向投影，进一步减少噪点引起的低像素投影，找出垂直切割经文的位置
# 5、垂直方向膨胀图片，使垂直文字形成连通区域
# 6、图像形态学处理，获取连通区域，进一步去除噪点、切割经文

from __future__ import division
import cv2
import os
import numpy as np  

def get_row_lection(src_path):
	img_list = []
	for root, dir, files in os.walk(src_path):
		for img_name in files:
			filename = os.path.join(root, img_name)
			img_list.append(filename)
	for img_path in img_list:
		img_name = img_path[img_path.rfind('/')+1:-4]
		new_file = base_path + img_name
		if not os.path.exists(new_file):
			os.mkdir(new_file)
		print 'new_file: %s' % new_file
		# step 1
		src_image, threshold_image = get_threshold_image(new_file, img_path)
		# step 2
		threshold_image = denoise(new_file, threshold_image)
		# step 3
		crop_src_image, crop_threshold_image = get_lection_position(src_image, threshold_image)
		# step 4
		middle_point_sum = remove_interfere(crop_threshold_image)
		# step 5
		dilate_image = get_dilate_image(new_file, crop_threshold_image, middle_point_sum)
		# step 6
		crop_src_image = get_retangle_contours(new_file, crop_src_image, dilate_image)
		cv2.imwrite(base_path + '/cut_image_%s.jpg' % img_name, crop_src_image) 

# 1.gray and threshold image
def get_threshold_image(new_file, img_path):
	# Load image
	src_image = cv2.imread(img_path)
	# convert image to gray and blur it
	gray_image = cv2.cvtColor(src_image, cv2.COLOR_RGB2GRAY)
	blur_image = cv2.blur(gray_image, (5,5))
	ret, threshold_image = cv2.threshold(blur_image, 0, max_thresh, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
	return src_image, threshold_image

# 2.remove noise pixel
def denoise(new_file, threshold_image):
	# close
	threshold_image_copy = threshold_image.copy()
	close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(50, 50))
	closed_image = cv2.morphologyEx(threshold_image, cv2.MORPH_CLOSE, close_kernel)

	contours, hierarchy = cv2.findContours(closed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	pos_shift = 2
	for count in contours:
		if (len(count) < 50):
			x, y, w, h = cv2.boundingRect(count)
			cv2.rectangle(threshold_image_copy,(x,y),(x+w,y+h),(255,0,0),5)
			threshold_image[y-pos_shift:y+h+pos_shift, x-pos_shift:x+w+pos_shift] = 0
	
	return threshold_image

# 3.horizontal project and get the lection fixed-position
def get_lection_position(src_image, threshold_image):
	img_height, img_width = threshold_image.shape
	row_sum = []
	up_min_pos = 500
	up_max_pos = 1000
	down_min_pos = 3000
	down_max_pos = 3500
	min_differ = 0
	min_index = 0
	max_differ = 0
	max_index = 0
	for i in range(up_min_pos, up_max_pos):
		sum = 0
		for j in range(img_width):
			sum = sum + threshold_image[i, j]
		if i > up_min_pos:
			pre_sum = cur_sum
			cur_sum = sum
			differ = cur_sum - pre_sum
			if min_differ > differ:
				min_differ = differ
				min_index = i
		else:
			cur_sum = sum

	for i in range(down_min_pos, down_max_pos):
		sum = 0
		for j in range(img_width):
			sum = sum + threshold_image[i, j]
		if i > down_min_pos:
			pre_sum = cur_sum
			cur_sum = sum
			differ = cur_sum - pre_sum
			if max_differ < differ:
				max_differ = differ
				max_index = i
		else:
			cur_sum = sum
	print 'max_index: %d, min_index: %d' % (min_index, max_index)
	crop_shift = 20
	crop_threshold_image = threshold_image[min_index + crop_shift : max_index - crop_shift,:]
	crop_src_image = src_image[min_index + crop_shift : max_index - crop_shift,:].copy()
	return crop_src_image, crop_threshold_image

# 4.vertical project, get rid of interfere factor which results to low pixel.
def remove_interfere(crop_threshold_image):	
	img_height, img_width = crop_threshold_image.shape
	threshold_value = 200
	distance = 100

	width_sum = []
	for j in range(img_width):
		sum = 0
		for i in range(img_height):
			sum = sum + crop_threshold_image[i, j]
		width_sum.append(sum/255)
	width_sum[0] = 0
	flag = 'false'
	change_point = 0
	middle_point_sum = []
	for k in range(1, len(width_sum)):
		if width_sum[k] >= threshold_value:	
			width_sum[k] = 1
			if (flag == 'true') and (width_sum[k] != width_sum[k-1]):
				flag = 'false'
				middle_point = int((change_point + k)/2)
				if len(middle_point_sum) >= 1 and middle_point - middle_point_sum[-1] <= distance:
					middle_point_sum[-1] = int((middle_point_sum[-1]+middle_point)/2)
				else:
					middle_point_sum.append(middle_point)
		else:
			width_sum[k] = 0
			if (flag == 'false') and (width_sum[k] != width_sum[k-1]):
				flag = 'true'
				change_point = k
	print 'middle_point: %s' %  middle_point_sum
	return middle_point_sum

# 5.get dilate image
def get_dilate_image(new_file, crop_threshold_image, middle_point_sum):
	#cv2.imwrite(new_file + '/5.1-crop_threshold_image.jpg', crop_threshold_image)
	dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1, 500))
	dilate_image = cv2.dilate(crop_threshold_image, dilate_kernel)
	for i in middle_point_sum:
		dilate_image[:,i-5:i+5] = 0
	#cv2.imwrite(new_file + '/5.2-dilate.jpg', dilate_image)
	return dilate_image

# 6.get retangle
def get_retangle_contours(new_file, crop_src_image, dilate_image):
	contours, hierarchy = cv2.findContours(dilate_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	i = 1
	for count in contours:
		x, y, w, h = cv2.boundingRect(count)
		if h > 500 and w > 100:
			roi = crop_src_image[y:y+h, x:x+w]
			cv2.imwrite(new_file + '/%s.jpg' % i, roi)
			cv2.rectangle(crop_src_image,(x,y),(x+w,y+h),(255,0,0),5)
			i = i + 1
	print 'len(contours): %d, len(cut): %d\n' % (len(contours),i)
	cv2.imwrite(new_file + '/cut_image.jpg', crop_src_image)
	return crop_src_image
	
if __name__ == "__main__":
	base_path = 'data/sutra_lection_result/'
	src_path = 'data/sutra_lection/'
	min_thresh = 100
	max_thresh = 255
	get_row_lection(src_path)
