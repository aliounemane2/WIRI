"""wiri URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
# from users import views as users_views
from django.conf import settings
from django.conf.urls.static import static
from users.views import *
from jmspots.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls')),
    url(r'^chatroom/', include('chatroom.urls')),
    url(r'^jmspots/', include('jmspots.urls')),
    url(r'^jmrequests/', include('jmrequests.urls')),
    url(r'^fcm/', include('fcm.urls')),

    #url(r'^accueil/$', home),
    # url(r'^$', home,name='accueil') ,
    url(r'^$', index, name='index') ,
    url(r'^accounts/$', index_office, name='accounts'),
    url(r'^accounts/login/$', login_account, name='login_account'),
    url(r'^accounts/logout_account/$', logout_account, name='logout_account'),
    url(r'^send_message_mane/$', send_message_mane, name='send_message_mane'),
    url(r'^accounts/signup/$', signup, name='signup'),
    url(r'^accounts/signup_account/$', signup_account, name='signup_account'),
    url(r'^accounts/signup_account2/$', signup_account2, name='signup_account2'),
    url(r'^accounts/signup_account3/$', signup_account3, name='signup_account3'),
    # url(r'^accounts/forget_password/$', forget_password_account, name='forget_password_account'),
    url(r'^accounts/forget_password/$', forget_password, name='forget_password'),
    url(r'^accounts/profil/$', profil, name='profil'),
    url(r'^accounts/forget_password_account/$', forget_password_account, name='forget_password_account'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^modify_password/$', modify_password, name='modify_password'),
    url(r'^modify_password2/$', modify_password2, name='modify_password2'),

    url(r'^mane_message/$', mane_message, name='mane_message'),
    url(r'^mane_message_nexmo/$', mane_message_nexmo, name='mane_message_nexmo'),
    url(r'^twilio_sendmess/$', twilio_sendmess, name='twilio_sendmess'),



    url(r'^events/create_event/$', create_event, name='create_event'),
    url(r'^institution/create_institution/$', create_institution, name='create_institution'),
    url(r'^institution/new_instutition/$', new_instutition, name='new_instutition'),
    url(r'^events/new_event/$', new_event, name='new_event'),
    url(r'^edit_card/$', edit_card, name='edit_card'),
    url(r'^pixlr/$', pixlr, name='pixlr'),
    url(r'^event_pixlr/$', event_pixlr, name='event_pixlr'),
	url(r'^save_pixlr_event/$', save_pixlr_event, name='save_pixlr_event'),
	url(r'^save_pixlr_institution/$', save_pixlr_institution, name='save_pixlr_institution'),
	
	

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)