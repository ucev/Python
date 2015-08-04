import os,sys,shelve

def correctMIMEType():
	moduleFileName='correctMIMEType.py'
	fileTypeFile='fileType'
	mimeTypeFile='mime'
	countFile='fileCnt'
	for dn in sys.path:
		if os.path.exists(dn+'/'+moduleFileName):
			dirname=dn
			break
	files=[x for x in os.listdir() if os.path.isfile(x)]
	files.sort()
	unknownType=[]
	fileType=shelve.open(dirname+'/'+fileTypeFile)
	mimeType=shelve.open(dirname+'/'+mimeTypeFile)
	curCountFile=shelve.open(dirname+'/'+countFile)
	curCount=curCountFile['count']
	for filename in files:
		if filename[0]!='.':
			fe=list(os.path.splitext(filename))
			f0change=False
			try:
				fileCnt=int(fe[0])
				if fileCnt<curCount:
					pass
				elif fileCnt==curCount:
					curCount+=1
				else:
					fe[0]=str(curCount)
					curCount+=1
					f0change=True
			except ValueError:
				fe[0]=str(curCount)
				curCount+=1
				f0change=True
			f=open(filename,'rb').read()
			for pictureType in fileType['pictureType']:
				findType=False
				for tp in mimeType[pictureType]:
					if f[tp[0]:tp[1]]==tp[2]:
						if fe[1]!=pictureType:
							newname=fe[0]+pictureType
							os.rename(filename,newname)
							f0change=False
						findType=True
						break
				if findType:
					break
			else:
				unknownType.append(filename)
			if f0change:
				newname=fe[0]+fe[1]
				os.rename(filename,newname)
	curCountFile['count']=curCount
	fileType.close()
	mimeType.close()
	curCountFile.close()
	return unknownType
