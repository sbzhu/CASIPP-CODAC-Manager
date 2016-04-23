#!/usr/bin/python 
import paramiko, os
from ConfigParser import ConfigParser 

# Created by ablezhu
# 2016.1.19

class RemoteCmd :
	def __init__(self):
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	def conncet(self, ip, user, password): 
		self.ssh.connect(ip, 22, user, password) 

	def excute(self, cmd): 
		stdin, stdout, stderr = self.ssh.exec_command(cmd) 
		print stdout.read()

	def disconnect(self): 
		self.ssh.close()

class RemoteUploadDir:
	def __init__(self, ip, user, password):
		self.ssh = paramiko.Transport((ip, 22)) 
		self.ssh.connect(username = user, password = password) 
		self.sftp = paramiko.SFTPClient.from_transport(self.ssh) 

	def excute(self, localDir, remoteDir):
		fileList = os.listdir(localDir) 
		for file in fileList: 
			print 'Uploading file : ' +  os.path.join(localDir, file) 
			self.sftp.put(os.path.join(localDir, file), os.path.join(remoteDir, file)) 

	def disconnect(self):
		self.ssh.close()

class TestCase :
	def test_RemoteCmd(self):
		parser = ConfigParser()
		parser.read('configure.ini')
		ipList = parser.items('IocServer')
		ip = ipList[0][1]

		remoteController = RemoteCmd()
		remoteController.conncet(ip, 'codac-dev', 'core09')
		remoteController.excute('pwd;ls ~/Desktop/')
		remoteController.excute('free')
		remoteController.disconnect()

	def test_RemoteUploadDir(self):
		remoteUploadDir = RemoteUploadDir('10.136.64.114', 'codac-dev', 'core09')
		remoteUploadDir.excute('.', '~/Desktop/')
		remoteUploadDir.disconnect()

	def WalkDir(self, dir):
		s = os.sep 
		for i in os.listdir(dir):
			if os.path.isfile(os.path.join(dir, i)):
				print i
			elif os.path.isdir(os.path.join(dir, i)):
				self.WalkDir(os.path.join(dir, i))
		

testCase = TestCase()
#testCase.test_RemoteCmd()
#testCase.test_RemoteUploadDir()
testCase.WalkDir('/home/codac-dev/workspace/python')


















