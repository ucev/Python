#!/usr/bin/python3.4

'''
	这是从windows到ubuntu上的文件转换格式
'''

import sys,os

def transfer(args):
	for filename in args:
		tempname=filename+"1"
		with open(filename,'rb') as targetfile,open(tempname,'w') as tempfile:
			lines=[line.decode('gbk') for line in targetfile.readlines()]
			tempfile.writelines(lines)
		os.remove(filename)
		os.rename(tempname,filename)


if __name__ == '__main__':
	args=sys.argv[1:]
	transfer(args)
