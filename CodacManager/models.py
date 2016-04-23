
#!/usr/bin/python

from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

class UserInfo(models.Model):
	username = models.CharField(max_length = 64,  primary_key=True)
	password = models.CharField(max_length = 64)
	mailaddr = models.EmailField(max_length = 254, null = True)
	createtime = models.DateTimeField('date created')
	def __str__(self):              # __unicode__ on Python 2
		return self.username + '\t' + self.mailaddr

class Host(models.Model):
	ip = models.GenericIPAddressField(primary_key=True)
	hostname = models.CharField(max_length = 64, null = True)
	user = models.CharField(max_length=64)
	password = models.CharField(max_length=64)
	def __str__(self):              # __unicode__ on Python 2
		return self.hostname + ' : ' + self.ip + ' ' + self.user 

class HostGroup(models.Model):
	group = models.CharField(max_length=64, primary_key = True) 
	host = models.ManyToManyField(Host)

	def __str__(self):              # __unicode__ on Python 2
		return self.group

class WorkDir(models.Model): # the dir of each task 
	taskname = models.CharField(max_length=64, primary_key = True)
	director = models.CharField(max_length=64)
	def __str__(self):              # __unicode__ on Python 2
		return self.taskname + '\t' + self.director



