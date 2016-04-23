#!/usr/bin/python

import os 

# created by abelzhu
# 2016.1.19

class EpicsInterface:
	def __init__(self):
		    self.data = []

	def caget(self, pv_name):
		p = os.popen('caget ' + pv_name).readlines()
		re = ''
		for line in p:
			re += ' '.join(line.split(' ')) # strip the spare space

		return re.split() # the information is stored in list

	def caput(self, pv_name, value):
		os.popen('caput ' + pv_name + ' ' + value)
