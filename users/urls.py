from django.conf.urls import url
from users.views import *
from users import views as myapp_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # debut web service

    url(r'^$', UserList.as_view()),
    url(r'^interests/$', InterestList.as_view()),
    url(r'^favourite/$', FavouriteContactList.as_view()),
    # url(r'^interests/media/$', myapp_views.media, name='media'),

    url(r'^(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^inscription/$', myapp_views.inscription, name='inscription'),
    url(r'^validation/$', myapp_views.validation_Code, name='validation_Code'),
    url(r'^contacts/$', myapp_views.contacts, name='contacts'),
    url(r'^authentification/$',myapp_views.authentification, name='authentification'),
    url(r'^listInterest/$', myapp_views.listInterest, name='listInterest'),
    url(r'^complements_info/$', myapp_views.complements_info, name='complements_info'),
    url(r'^save_interest/$', myapp_views.save_interest, name='save_interest'),
    url(r'^addFavoriteContact/$', myapp_views.addFavoriteContact, name='addFavoriteContact'),
    url(r'^addFavoriteContact2/$', myapp_views.addFavoriteContact2, name='addFavoriteContact2'),
    url(r'^getFavoriteContact/$', myapp_views.getFavoriteContact, name='getFavoriteContact'),
    url(r'^modify_info/$', myapp_views.modify_info, name='modify_info'),
    url(r'^modify_password/$', myapp_views.modify_password, name='modify_password'),
    url(r'^edit_photo/$', myapp_views.edit_photo, name='edit_photo'),
    url(r'^save_image/$', myapp_views.save_image, name='save_image'),
    url(r'^send_email_password/$', myapp_views.send_email_password, name='send_email_password'),
    url(r'^get_Favourite/$', myapp_views.get_Favourite, name='get_Favourite'),
    # url(r'^verif_user/$', myapp_views.verif_user, name='verif_user'),
    url(r'^verif_user/(?P<telephone>[0-9]+)/$', myapp_views.verif_user, name='verif_user'),
    url(r'^push_notification_fcm/$', myapp_views.push_notification_fcm, name='push_notification_fcm'),
    url(r'^send_fcm_notification/$', myapp_views.send_fcm_notification, name='send_fcm_notification'),
    url(r'^mane_message/$', myapp_views.mane_message, name='mane_message'),
    url(r'^testovh/$', myapp_views.testovh, name='testovh'),
    url(r'^testovh2/$', myapp_views.testovh2, name='testovh2'),
    url(r'^password_crypting/$', myapp_views.password_crypting, name='password_crypting'),

    ## Fin du web service

    url(r'^contacter_wiri/$', myapp_views.contacter_wiri, name='contacter_wiri'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)