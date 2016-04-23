#!/usr/bin/env python 

from fabric.api import *  
from fabric.context_managers import *  
from fabric.contrib.console import confirm  

from CodacManager.models import *
import os

def FabGetSddList():
	workDir = WorkDir.objects.filter(taskname = 'sdd_workspace')[0].director
	hostList = HostGroup.objects.filter(group='SddDeveloper')[0].host.all()  

	sddPrjList = []
	for host in hostList: 
		with cd(workDir):
			with settings(
					host_string = host.user + '@' + host.ip,
					password = host.password,
					warn_only = True,
					):
				prjList = run("ls -1 | grep m-").split('\r\n') # | sed 's/^m-//g'") 
				for prj in prjList : 
					rpmList = run("ls -1 %s%s/target/*.rpm" % (workDir, prj)).split('\r\n')

					sddPrj = {}
					sddPrj['host'] = host.ip
					sddPrj['prjName'] = prj.replace('m-', '')
					sddPrj['rpmList'] = rpmList

					sddPrjList.append(sddPrj.copy())

	sddPrjInfo = {
			'workDir' : workDir,
			'sddPrjList' : sddPrjList,
			}
	return sddPrjInfo


def FabGetCssList():
	workDir = WorkDir.objects.filter(taskname = 'css_workspace')[0].director
	hostList = HostGroup.objects.filter(group='CssDeveloper')[0].host.all()  

	cssPrjList = []
	# cssPrjList = [
	#	{'host': xxx, 'prjList' : ['111', '222'] }
	# ]

	for host in hostList: 
		with cd(workDir):
			with settings(
					host_string = host.user + '@' + host.ip,
					password = host.password,
					warn_only = True,
					):
				prjList = run('ls -F | grep "/$"').split('\r\n')

				cssPrj = {}
				cssPrj['host'] = host.ip
				cssPrj['prjList'] = prjList

				cssPrjList.append(cssPrj.copy())

	

	cssPrjInfo = {
			'workDir' : workDir,
			'cssPrjList' : cssPrjList,
			}
	return cssPrjInfo

def FabInstallRpm(rpm, sourceHost, targetList): 
	# first, get the file  form source host to local
	for target in targetList:
		with settings(
				host_string = sourceHost,
				password = Host.objects.filter(ip=sourceHost.split('@')[-1])[0].password,
				warn_only = True,
				):
			get(rpm, "/tmp/")
	
	# now the file director is changed !
	rpm = '/tmp/' + os.path.basename(rpm)

	# then, put the file from local to target host
	for target in targetList:
		with settings(
				host_string = target,
				password = Host.objects.filter(ip=target.split('@')[-1])[0].password,
				warn_only = True,
				):
			put(rpm, "/tmp/")
			# run('rpm -ivh %s' % rpm) 

def FabPutCssFolder(sourceHost, sourceFolder, targetList):
	# first, get the file  form source host to local
	for target in targetList:
		with settings(
				host_string = sourceHost,
				password = Host.objects.filter(ip=sourceHost.split('@')[-1])[0].password,
				warn_only = True,
				):
			get(sourceFolder, "/tmp/")
	
	# now the file director is changed !
	if '/' == sourceFolder[-1]:
		sourceFolder = '/tmp/' +  sourceFolder.split('/')[-2] + '/'
	else :

		sourceFolder = '/tmp/' +  sourceFolder.split('/')[-1] + '/'

	# then, put the file from local to target host
	cssWorkDir = WorkDir.objects.filter(taskname = 'css_workspace')[0].director
	for target in targetList:
		with settings(
				host_string = target,
				password = Host.objects.filter(ip=target.split('@')[-1])[0].password,
				warn_only = True,
				):
			put(sourceFolder, cssWorkDir)

def FabGetIocList(iocServerList):
	iocInfoList = []
	for iocServer in iocServerList:
		host = '%s@%s' % (iocServer.user, iocServer.ip)
		with cd('/usr/bin/'):
			with settings(
					host_string = host,
					password = iocServer.password,
					warn_only = True,
					):
				iocInfo = { }
				iocInfo['host'] = host
				iocInfo['iocList'] = []

				ioc_status = { }
				tmpList = run('ls -1 MAG-*').split('\r\n')
				for ioc in tmpList:
					ret = run('%s status' % ioc)
					ioc_status['ioc'] = ioc
					ioc_status['status'] = 'red' if 'not running' in ret else 'green'

					iocInfo['iocList'].append(ioc_status.copy())


				iocInfoList.append(iocInfo.copy())

#	iocInfoList = [
#			{'host': xxx, 'iocList': [{'ioc': xxx, 'status': 'green' }, ] },
#			{'host': xxx, 'iocList': [{'ioc': xxx, 'status': 'red' }, ] }, 
#			]
	return iocInfoList 

# Switch the status of ioc
def FabIOCStartSop(ioc, host):
	with settings(
			host_string = host,
			password = Host.objects.filter(ip = host.split('@')[-1])[0].password,
			warn_only = True,
			):
		ret = run('%s status' % ioc)
		if 'not running' in ret:
			if 'OK' in run('%s start' % ioc):
				return 'green'
			else:
				return 'red'
		else :
			if 'OK' in run('%s stop' % ioc):
				return 'red'
			else:
				return 'green'
		# green means runing, red means stoped

def FabGetArchiveStatus(host):
	with settings(
			host_string = "%s@%s" % (host.user, host.ip),
			password = host.password,
			warn_only = True,
			):
		ret = run('css-archive-engine status')
		return 'red' if 'not running' in ret else 'green'

def FabSwitchArchiveStatus(host):
	with settings(
			host_string = "%s@%s" % (host.user, host.ip),
			password = host.password,
			warn_only = True,
			): 
		status = run('css-archive-engine status')

		if 'not running' in status:
			ret = sudo('css-archive-engine start')
#			return 'green' if 'OK' in ret else 'red'
		else:
			ret = sudo('css-archive-engine stop')
#			return 'red' if 'OK' in ret else 'green'
		return FabGetArchiveStatus(host)


def FabConfigArchive(sourceHost, sourcePath, targetHost):
	# first, get the file  form source host to local /tmp/
	with settings(
			host_string = sourceHost,
			password = Host.objects.filter(ip=sourceHost.split('@')[-1])[0].password,
			warn_only = True,
			):
		get(sourcePath, "/tmp/")
	
	# now the file director is changed !
	sourcePath = '/tmp/' + os.path.basename(sourcePath)

	# then, put the file from local to target host /tmp/
	with settings(
			host_string = targetHost,
			password = Host.objects.filter(ip=targetHost.split('@')[-1])[0].password,
			warn_only = True,
			):
		put(sourcePath, '/tmp/')
		# now install the configure file and restart the engine
#		run('archive-configtool -engine CODAC -import -config %s -replace_engine' % sourcePath)
#		run('css-archive-engine restart')


#################################### for test #####################################

def FabTest():
	with cd('~/Desktop/'):
		with settings(
				host_string = 'codac-dev@10.136.64.101',
				password = 'operator@htscl',
				warn_only = True,
				):
			date = run('pwd; date >> test.txt')
	return date




