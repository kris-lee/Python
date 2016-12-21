# code for calculating the count of every word in the txt including total words and low frequent words
# auth : Li zhichao
# data : 2016-8-12


# -*- coding:utf-8 -*-  
import os,sys
import string

def calculate(dic, generate_file):
	with open(generate_file, 'rw') as fp:
		for line in fp.readlines():
			string = line.split()[2]
			word = unicode(''.join(string),'utf-8')
			for cha in word:
				if cha in dic:
					dic[cha] = dic[cha] + 1
				else:
					dic[cha] = 1
	dict = sorted(dic.iteritems(), key = lambda d:d[1], reverse = True)
	with open(calculate_file , 'wb') as cr:
		for i in dict:
			line = '%s %s\n' % (i[0].encode('utf-8'),i[1])
			cr.write(line)
	dic.clear()


def lowfrequent(calculate_file, totaltext_file):
	lowfrequent_list = []
	with open(calculate_file, 'rw') as cf:
		border = 1000
		for line in cf.readlines():
			count = int(line.split()[1])
			if count < border:
				char = line.split()[0]
				ch_char = unicode(''.join(char),'utf-8')
				lowfrequent_list.append(ch_char.encode('utf-8'))
				
	lowfrequent_sentence = []

	with open(totaltext_file, 'rw') as tf:
		for line in tf.readlines():
			for letter in lowfrequent_list:
				if letter in line:
					string = unicode(''.join(line),'utf-8')
					lowfrequent_sentence.append(string.encode('utf-8'))					
	del lowfrequent_list


	with open(lowfrequent_text_file,'wb') as lf:
		for string in lowfrequent_sentence:
			line = unicode(''.join(string),'utf-8')
			sentence = '%s' %line
			lf.write(sentence.encode('utf-8'))
	del lowfrequent_sentence				
					
if __name__ == '__main__':

	file_path = '/data/Subtitle/'
	generate_file = file_path + '%s.txt' % 'list_merge'
	calculate_file = file_path + 'calculate_result.txt'
	totaltext_file = file_path + 'subtitle.sentence.common.no.space.txt'
	lowfrequent_text_file = file_path + 'totaltext_lowfrequent_word.txt'

	dic = {}
	calculate(dic, generate_file)
	lowfrequent(calculate_file, totaltext_file)
