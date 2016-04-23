from django.contrib import admin

# Register your models here.

from .models import *
class UserInfoAdmin(admin.ModelAdmin):
	fieldsets = [
			('Register information', {'fields' : ['username', 'password', 'mailaddr']}), 
			('Date information'    , {'fields' : ['createtime']}),
	]

class HostAdmin(admin.ModelAdmin):
	list_display = ('hostname', 'ip', 'user', 'password')
	fields = ('ip', 'hostname', ('user', 'password'))
	pass

class WorkDirAdmin(admin.ModelAdmin):
	list_display = ('taskname', 'director')
	list_editable = ('director', )
	pass

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(WorkDir, WorkDirAdmin)
admin.site.register(HostGroup)
