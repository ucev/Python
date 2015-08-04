#!/usr/bin/python3.4
import re,os,shutil

currVFile='currVFile'
allVFile='allVFile'

conf=re.compile(r'\d{1,2}\.\d{1,2}\.\d{1,2}-\d{1,2}(?=-generic)')
conf1=re.compile(r'\d{1,2}\.\d{1,2}\.\d{1,2}-\d{1,2}')
os.system('uname -a > %s' % (currVFile))
os.system('dpkg --get-selections|grep linux > %s ' % (allVFile))

currVStr=open(currVFile,'r').read()
res=conf.search(currVStr)
currV=res.group()
preV=None
for line in open(allVFile,'r'):
	res=conf1.search(line)
	if res:
		preV=res.group()
		if not preV==currV:
			break
		else:
			preV=None

if preV:
	os.system('apt-get purge linux-headers-%s linux-image-%s' % (preV,preV))
os.remove(currVFile)
os.remove(allVFile)

tarDir='/boot/grub'

grubFile='/boot/grub/grub.cfg'
tempFile='/boot/grub/temp'

f=open(grubFile,'r')
f2=open(tempFile,'w')

traverseWin=False
submenuText=''

for line in f:
	if re.search(r"submenu 'Advanced options for Ubuntu'",line):
		if not traverseWin:
			count=1
			submenuText+='\n'+line
			for line1 in f:
				submenuText+=line1
				leftIter=re.finditer('{',line1)
				for it in leftIter:
					count+=1
				rightIter=re.finditer('}',line1)
				for it in rightIter:
					count-=1
				if count==0:
					submenuText+='\n'
					break
		else:
			f2.write(line)
	elif re.search(r"menuentry 'Memory test \(.*?\)'",line):
		f2.write('#'+line)
		count=1
		for line1 in f:
			f2.write('#'+line1)
			leftIter=re.finditer('{',line1)
			for it in leftIter:
				count+=1
			rightIter=re.finditer('}',line1)
			for it in rightIter:
				count-=1
			if count==0:
				break
	else:
		mat=re.search(r"(?<=menuentry \'Windows).*?/dev/sda1\)",line)
		if mat:
			f2.write(line[:mat.start()]+"10"+line[mat.end():])
			count=1
			for line1 in f:
				f2.write(line1)
				leftIter=re.finditer('{',line1)
				for it in leftIter:
					count+=1
				rightIter=re.finditer('}',line1)
				for it in rightIter:
					count-=1
				if count==0:
					f2.write(submenuText)
					traverseWin=True
					break
		else:
			mat=re.search(r"(?<=set timeout=)\d+",line)
			if mat:
				f2.write(line[:mat.start()]+"4"+line[mat.end():])
			else:
				f2.write(line)

f.close()
f2.close()

shutil.move(tempFile,grubFile)
