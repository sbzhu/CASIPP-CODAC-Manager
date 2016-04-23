from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'PIDConfigure/$', views.PIDConfigure, name='PIDConfigure'),
	url(r'ServerManager/$', views.ServerManager, name='ServerManager'),
	url(r'AlignConfigure/$', views.AlignConfigure, name='AlignConfigure'),
	url(r'AutosaveConfigure/$', views.AutosaveConfigure, name='AutosaveConfigure'),
	url(r'IOCInstall/$', views.IOCInstall, name='IOCInstall'),
	url(r'IOCStartStop/$', views.IOCStartStop, name='IOCStartStop'),
	url(r'ArchiveEngineConfigure/$', views.ArchiveEngineConfigure, name='ArchiveEngineConfigure'),
	url(r'ArchiveEngineRunStop/$', views.ArchiveEngineRunStop, name='ArchiveEngineRunStop'),
	url(r'DatabaseBackup/$', views.DatabaseBackup, name='DatabaseBackup'),
	url(r'WebopiInstall/$', views.WebopiInstall, name='WebopiInstall'),
	url(r'OPIDistribution/$', views.OPIDistribution, name='OPIDistribution'),
	url(r'ServerHealthyMonitor/$', views.ServerHealthyMonitor, name='ServerHealthyMonitor'),
	url(r'GetIocStatus/$', views.GetIocStatus, name='GetIocStatus'),
	url(r'^about/', TemplateView.as_view(template_name="about")),
	url(r'TestPage/$', views.TestPage, name='TestPage'),
	url(r'TestAjax/$', views.TestAjax, name='TestAjax'),
]
