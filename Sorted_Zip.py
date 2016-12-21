# code for classifying zipping the files
# auth : Li zhichao
# data : 2016-8-20

import os,shutil
import sys
import glob
import zipfile



def getList(dir, suffix):
	dic = []
	f = glob.glob(dir + '//*.' + suffix)
	for file in f:
		filename = os.path.basename(file)
		dic.append(filename)
	return dic


def getSortedList(dic):
	dic.sort(key = lambda x:int(x[:-4]))
	return dic


def getSortedZip(sortedDic, dir, fileDir, zipDir):
	fileCount = 0
	count = 0
	filetexts = []
	filePath = fileDir + '%s' % fileCount + '/'
	os.makedirs(filePath)
	for name in sortedDic:

		#copy files to holder
		filetexts.append(name.split(".")[0])
		shutil.copy(dir + name, filePath + name)
		count = count + 1
		if (count == 100 or name == sortedDic[-1] ) :
			count = 0
			
			#generate zip
			zipCount = fileCount
			zipName = zipDir + 'video_resized_p%s.zip' % zipCount
			#zipName = 'video_resized_p%s.zip' % zipCount
			f = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)  
			for dirpath, dirnames, filenames in os.walk(filePath):  
    				for filename in filenames:
        				f.write(os.path.join(dirpath,filename), arcname = filename)  
			f.close() 
			
			#generate txt
			textName = filePath + 'list_p%s.txt' % zipCount
			with open(textName,"wb") as fp:
				for filetext in filetexts:
					line = '%s \n' % filetext
					fp.write(line)
			del filetexts[:]
				
			#generate folder to hold files 
			if name != sortedDic[-1]:
				fileCount = fileCount + 1
				filePath = fileDir + '%s' % fileCount + '/'
				os.makedirs(filePath)
				

if __name__ == '__main__':
	dir = '/data/racv_data/0/'
	fileDir = '/data/sorted_zip/filesList/'
	zipDir = '/data/sorted_zip/'
	suffix = 'mp4'
	dic = getList(dir, suffix)
	sortedDic = getSortedList(dic)
	getSortedZip(sortedDic, dir, fileDir, zipDir)
