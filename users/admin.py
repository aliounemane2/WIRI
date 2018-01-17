from django.contrib import admin
from users.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('telephone', 'email')
    list_filter = ('telephone',)


class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)


class FavouriteContactAdmin(admin.ModelAdmin):
    pass


# class UserFavouriteContactAdmin(admin.ModelAdmin):
#     list_display = ('user', 'favouriteconatct',)


admin.site.register(User, UserAdmin)
admin.site.register(Interest, InterestAdmin)
# admin.site.register(InterestUser, InterestUserAdmin)
admin.site.register(FavouriteContact, FavouriteContactAdmin)
# admin.site.register(UserFavouriteContact, UserFavouriteContactAdmin)

admin.site.site_title = 'Administration de la plateforme WIRI'
admin.site.site_header = 'Administration de la plateforme WIRI'



