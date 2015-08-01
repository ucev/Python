import os,time

def func():
	d1=time.ctime().split()[2]
	action=input('Do you want to halt(h) or reboot(r) your computer?\n')
	if action in {'h','r'}:
		t=input('enter the interval of the operation:\n')
		tim=t=int(t)
		if t>86400:
			print('out of range\n')
			return
		epoc_sec=time.time()+tim
		str_time=time.ctime(epoc_sec)
		tm=str_time.split()[3]
		d2=time.ctime().split()[2]
		tom=True if int(d2)>int(d1) else False
		if action=='h':
			op='Your computer will be halted at {0} tomorrow'.format((tm)) if tom else 'Your computer will be halted at {0}'.format((tm))
			print(op)
			time.sleep(tim)
			os.system('halt')
		else:
			op='Your computer will be rebooted at {0} tomorrow'.format((tm)) if tom else 'Your computer will be rebooted at {0}'.format((tm))
			print(op)
			time.sleep(tim)
			os.system('reboot')
	else:
		print('Please input \'h\' or \'r\'\n')
		func()

func()
