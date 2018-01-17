
from django.contrib import admin
from jmspots.models import *
from jmrequests.models import *
from chatroom.models import *


class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ('created', 'content')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('users', 'content')

class MediaAdmin(admin.ModelAdmin):
    list_display = ('message',)



admin.site.register(ChatGroup, ChatGroupAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Media, MediaAdmin)

#admin.site.register(UserChatGroup, UserChatGroupAdmin)
#admin.site.register(CardShare, CardShareAdmin)
#admin.site.register(InterestCardShare, InterestCardShareAdmin)
#admin.site.register(UserCardShare, UserCardShareAdmin)

admin.site.site_title = 'Administration de la plateforme WIRI'
admin.site.site_header = 'Administration de la plateforme WIRI'