from django.contrib import admin

from django.contrib import admin
from jmspots.models import *
from jmrequests.models import *



class RequestAdmin(admin.ModelAdmin):
    list_display = ('spot', 'card')


class Request_ReceiversAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'state')


admin.site.register(Request, RequestAdmin)
admin.site.register(Request_Receivers, Request_ReceiversAdmin)

admin.site.site_title = 'Administration de la plateforme WIRI'
admin.site.site_header = 'Administration de la plateforme WIRI'