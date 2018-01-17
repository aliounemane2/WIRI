from django.contrib import admin

from django.contrib import admin
from jmspots.models import *


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'spot')


class HorairesAdmin(admin.ModelAdmin):
    list_display = ('time_degin', 'time_end')


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name',)



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CardAdmin(admin.ModelAdmin):
    list_display = ('institution', 'event',)


class SpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')


class UserCardAdmin(admin.ModelAdmin):
    list_display = ('sender', 'date_created')


class UserCardFavouriteAdmin(admin.ModelAdmin):
    list_display = ('sender',)


admin.site.register(Event, EventAdmin)
admin.site.register(Horaires, HorairesAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Spot, SpotAdmin)
admin.site.register(UserCard, UserCardAdmin)
admin.site.register(UserCardFavourite, UserCardFavouriteAdmin)

admin.site.site_title = 'Administration de la plateforme WIRI'
admin.site.site_header = 'Administration de la plateforme WIRI'




