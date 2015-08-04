#! /usr/bin/python3.4
import os,sys,shelve

moduleFilename='correctMIMEType.py'
fileTypeFile='fileType'
mimeTypeFile='mime'
for dn  in sys.path:
	if os.path.exists(os.path.join(dn,moduleFilename)):
		dirname=dn
		break
digitFilesList=[]
unamedFilesList=[]
renamedFilesList=[]
for x in os.listdir('.'):
	if os.path.isfile(x):
		if not x.startswith('.'):
			if os.path.splitext(x)[0].isdigit():
				digitFilesList.append(x)
			else:
				unamedFilesList.append(x)
digitFilesList=sorted(digitFilesList,key=lambda x:int(os.path.splitext(x)[0]),reverse=True)
print(digitFilesList)
print(unamedFilesList)
count=0
while digitFilesList:
	count+=1
	f=digitFilesList[len(digitFilesList)-1]
	newname=str(count)+os.path.splitext(f)[1]
	os.rename(f,newname)
	digitFilesList.pop()
while unamedFilesList:
	count+=1
	f=unamedFilesList[len(digitFilesList)-1]
	newname=str(count)+os.path.splitext(f)[1]
	os.rename(f,newname)
	unamedFilesList.pop()
	renamedFilesList.append(newname)
fileType=shelve.open(os.path.join(dirname,fileTypeFile))
mimeType=shelve.open(os.path.join(dirname,mimeTypeFile))
for filename in renamedFilesList:
	fe=list(os.path.splitext(filename))
	f=open(filename,'rb').read()
	for pictureType in fileType['pictureType']:
		findType=False
		for tp in mimeType[pictureType]:
			if f[tp[0]:tp[1]]==tp[2]:
				if fe[1]!=pictureType:
					fe[1]=pictureType
				findType=True
				break
		if findType:
			break
	newname=fe[0]+fe[1]
	print('oldname=%s\tnewname=%s' % (filename,newname))
	os.rename(filename,newname)
