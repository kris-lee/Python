import cv2
import os
import numpy as np  
from matplotlib import pyplot as plt  

def get_row_lection(src_path):
	# Load image
	img_list = []
	for root, dir, files in os.walk(src_path):
		for img_name in files:
			filename = os.path.join(root, img_name)
			img_list.append(filename)
	for img_path in img_list:
		img_name = img_path[img_path.rfind('/')+1:-4]
		print 'img_path:%s, img_name:%s' % (img_path, img_name)
		new_file = base_path + img_name
		if not os.path.exists(new_file):
			os.mkdir(new_file)
		src_img = cv2.imread(img_path)
		# convert image to gray and blur it
		gray_image = cv2.cvtColor(src_img, cv2.COLOR_RGB2GRAY)
		blur_image = cv2.blur(gray_image, (5,5))
		thresh_callback(new_file, src_img, blur_image)

def thresh_callback(new_file, src_img, blur_image):
	ret, threshold_image = cv2.threshold(blur_image, min_thresh, max_thresh, cv2.THRESH_BINARY_INV)

	# dilate image
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1, 200))
	dilate_image = cv2.dilate(threshold_image, kernel)
	img_copy = src_img.copy()
	
	contours, hierarchy = cv2.findContours(dilate_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	i = 1
	print 'len(contours): ', len(contours)
	for count in contours:
		x, y, w, h = cv2.boundingRect(count)
		if w > 10:
			roi = src_img[y:y+h, x:x+w]
			cv2.imwrite(new_file + '/%s.jpg' % i, roi)
			cv2.rectangle(img_copy,(x,y),(x+w,y+h),(255,0,0),3)
			i = i + 1
	cv2.imwrite(new_file + '/cut_result.jpg', img_copy)
	cv2.imwrite(base_path + '/%s.jpg' % (new_file[new_file.rfind('/')+1:]), img_copy)
	
if __name__ == "__main__":
	base_path = '/data/ordered_lection_result/'
	src_path = '/data/ordered_lection/'
	min_thresh = 100
	max_thresh = 255
	get_row_lection(src_path)
