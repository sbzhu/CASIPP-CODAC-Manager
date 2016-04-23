
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
import traceback
import os
from .forms import *
from django.http import Http404

from epicsInterface import EpicsInterface 
epicsInterface = EpicsInterface() 

from CodacManager.models import *

from fabfile  import *

# Create your views here.

# created by abelzhu
# 2016.1.19

def index(request):
	#	return HttpResponse("Hello, world ! Welcom to CODAC Configure site : %f " % pvValue)
	context = { }
	return render(request, 'CodacManager/index.html', context)

def PIDConfigure(request):
	pidPreFix = 'MAG-FDR-PID:'
	pidList = [
			'PID-00',
			'PID-01',
			'PID-02',
			'PID-03',
			'PID-04',
			'PID-05',
			'PID-06',
			'PID-07',
			'PID-08',
			'PID-09',
			'PID-10',
			'PID-11',
			'PID-12',
			'PID-13',
			'PID-14',
			'PID-15',
			]

	# check if it's submited by user
	try:
		callback = request.POST['callback']
	except Exception :
		callback = 'false' 
	if 'true' == callback :
		# do submit, write configuration
		for i in range(0, 16) : 
			# get configuration
			pidInpConf = request.POST['pid_' + str(i) + '_inp']
			pidOutConf = request.POST['pid_' + str(i) + '_out'] 

			# write configuration
			# caget MAG-FDR-STT:Ebloxx5-0.FLNK MAG-FDR-PID:PID-00:PV.DOL MAG-FDR-PID:PID-00:PV.OMSL MAG-FDR-PID:PID-00:LMN.FLNK MAG-FDR-CFG:AO1-2.DOL MAG-FDR-CFG:AO1-2.OMSL
			# MAG-FDR-STT:Ebloxx5-0.FLNK     MAG-FDR-PID:PID-00:PV
			# MAG-FDR-PID:PID-00:PV.DOL      MAG-FDR-STT:Ebloxx5-0 NPP NMS
			# MAG-FDR-PID:PID-00:PV.OMSL     closed_loop
			# MAG-FDR-PID:PID-00:LMN.FLNK    MAG-FDR-CFG:AO1-2
			# MAG-FDR-CFG:AO1-2.DOL          MAG-FDR-PID:PID-00:LMN NPP NMS
			# MAG-FDR-CFG:AO1-2.OMSL         closed_loop

			epicsInterface.caput(pidInpConf + '.FLNK', pidPreFix + pidList[i] + ':PV') 

			epicsInterface.caput(pidPreFix + pidList[i] + ':PV.DOL', pidInpConf)
			epicsInterface.caput(pidPreFix + pidList[i] + ':PV.OMSL', 'closed_loop')

			epicsInterface.caput(pidPreFix + pidList[i] + ':LMN.FLNK', pidOutConf) 

			epicsInterface.caput(pidOutConf + '.DOL', pidPreFix + pidList[i] + ':LMN') 
			epicsInterface.caput(pidOutConf + '.OMSL', 'closed_loop') 

	pidConfigureList = [ ]

	for pid in pidList :
		pidConfigure = { }
		# MAG-FDR-PID:PID-00:PV.DOL      MAG-FDR-STT:Ebloxx5-0 NPP NMS
		pv = epicsInterface.caget(pidPreFix + pid + ':PV.DOL' ) 
		pidConfigure['inp'] = pv[1] if len(pv) > 1 else ''
		# MAG-FDR-PID:PID-00:LMN.FLNK    MAG-FDR-CFG:AO1-2
		pv = epicsInterface.caget(pidPreFix + pid + ':LMN.FLNK' )
		pidConfigure['out'] = pv[1] if len(pv) > 1 else ''

		pidConfigureList.append(pidConfigure.copy())

	context = {
			'pidList' : pidList,
			'pidConfigureList' : pidConfigureList,
			}
	return render(request, 'CodacManager/PIDConfigure.html', context)

def ServerManager(request): 
	context = {}
	return render(request, 'CodacManager/ServerManager.html', context)

def AlignConfigure(request):
	return HttpResponse("Align configure page")

def AutosaveConfigure(request):
	return HttpResponse("Autosave configure page")

def IOCInstall(request):
	# get the sdd projects list in the dir  
	sddPrjInfo = FabGetSddList()
	IocServerList = HostGroup.objects.filter(group='IocServer')[0].host.all()  

	# check if it's submited by user
	try:
		callback = request.POST['callback']
	except Exception :
		callback = 'false' 
	if 'true' == callback :
		# do submit, write configuration
		# scp /home/codac-dev/m-HTSCL_FAT/target/xxx.rpm
		# rpm -ivh xxx.rpm
		targetList = []
		for server in IocServerList:
			host = '%s@%s' % (server.user, server.ip)
			if host in request.POST.getlist('sel_srv'):
				targetList.append(host)

		for sddPrj in sddPrjInfo['sddPrjList']: 
			for rpm in sddPrj['rpmList']:
				if '%s_%s_%s' % (rpm, sddPrj['prjName'], sddPrj['host']) in request.POST.getlist('sel_rpm'):
					FabInstallRpm(rpm, sddPrj['host'], targetList)
		
	context = {
			'sddPrjInfo' : sddPrjInfo,
			'IocServerList' : IocServerList,
			}

	return render(request, 'CodacManager/IOCInstall.html', context)

def IOCStartStop(request):
	# check if it's submited by user
	if 'POST' == request.method:
		# do submit, write configuration 
		ioc, host = request.POST['clicked_ioc'].split('_')
		status = FabIOCStartSop(ioc, host)
		return HttpResponse('%s' % status)

	else :
		# get the ioc list
		iocServerList = HostGroup.objects.filter(group='IocServer')[0].host.all()  
		iocInfoList = FabGetIocList(iocServerList)
		_iocInfoList = [
			{'host1': '111', 'iocList': [{'ioc': 'ioc111', 'status': 'green' }, ] },
			{'host2': '222', 'iocList': [{'ioc': 'ioc222', 'status': 'red' }, ] }, 
		]

		context = {
				'iocInfoList' : iocInfoList,
				}
		return render(request, 'CodacManager/IOCStartStop.html', context)

def ArchiveEngineConfigure(request):
	# check if it's submited by user
	if 'POST' == request.method:
		sourceHost = request.POST['sourceHost']
		sourcePath = request.POST['sourcePath']
		targetHostList = request.POST['targetHostList'].split('_')
		print targetHostList
		# do submit, write configuration
		for targetHost in targetHostList:
			if not targetHost.strip(): continue
			FabConfigArchive(sourceHost, sourcePath, targetHost)

		return HttpResponse('Config Archive OK : %s:%s' % (sourceHost, sourcePath))

	# show the archive servers to be installed in
	ArchiveServerList = HostGroup.objects.filter(group='ArchiveEngine')[0].host.all()  

	context = {
			'serverList' : ArchiveServerList,
			}
	return render(request, 'CodacManager/ArchiveEngineConfigure.html', context) 

def ArchiveEngineRunStop(request):
	# check if it's submited by user
	if 'POST' == request.method:
		# do submit, write configuration
		clicked_server = request.POST['clicked_server']
		# change this host's server status
		host = Host.objects.filter(ip = clicked_server)[0]
		status = FabSwitchArchiveStatus(host)

		return HttpResponse(status)

	# get the host list
	ArchiveServerList = HostGroup.objects.filter(group='ArchiveEngine')[0].host.all()  
	serverStatus = { }
	for host in ArchiveServerList : 
		status = FabGetArchiveStatus(host)
		serverStatus[host.ip] = status 

#	serverStatus = {'10.136.64.102' : 'red', '10.136.64.103': 'green',}
	context = {
			'serverList' : serverStatus,
			}
	return render(request, 'CodacManager/ArchiveEngineRunStop.html', context)

def DatabaseBackup(request):
	return HttpResponse("Backup the data from database to .bac file")

def WebopiInstall(request):
	return HttpResponse("Configure the webopi and start the web server")

def OPIDistribution(request):
	if 'POST' == request.method:
		# do submit, write configuration
		try:
			iocServerList = Host.objects.all()
			targetList = []
			for server in iocServerList:
				host = '%s@%s' % (server.user, server.ip)
				if host in request.POST.getlist('check_target'):
					targetList.append(host) 

			ip, selFolder = request.POST['sel_prj'].split(':')
			host  = 'root@' + ip
			cssFolder = WorkDir.objects.filter(taskname = 'css_workspace')[0].director + selFolder

			FabPutCssFolder(host, cssFolder, targetList)
		except:
			raise Http404()

	# get the css project list
	context = FabGetCssList()
	context['hostList'] = Host.objects.all()

	return render(request, 'CodacManager/OPIDistribution.html', context)

def ServerHealthyMonitor(request):
	return HttpResponse("Monitor the load of servers' cpu/IO/disk and so on")

def GetIocStatus(request):
	# ioc_host = request.GET['ioc_host']
	# ioc, host = ioc_host.split('_')
	status = 'yellow' #FabGetIocStatus(ioc, host)
	return HttpResponse(status)

#################################### for test #####################################

def TestAjax(request): 
	if 'POST' == request.method:
		name = request.POST['name']
		password = request.POST['password']
		clicked_input = request.POST['clicked_input']

		return HttpResponse('Test OK : %s' % (clicked_input))
	else :
		context = {}
		return render(request, 'CodacManager/TestAjax.html', context)


def TestPage(request): 
	data = FabTest()

	files = ''
	for i in data:
		files += str(i)

	return HttpResponse("Done the test ! See the test file in the Desktop ! %s" % files)


