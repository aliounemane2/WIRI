from django.conf.urls import url

#from users import views as myapp_views
from jmspots import views as myapp_views



from django.conf.urls import url
from jmrequests.views import *
from jmrequests import views as myapp_views

urlpatterns = [
    url(r'^$', RequestList.as_view()),
    url(r'^requestReceivers/$', Request_ReceiversList.as_view()),
    url(r'^jmrequest_join_me/$', myapp_views.jmrequest_join_me, name='jmrequest_join_me'),
    url(r'^jmrequest_to_bejoined/$', myapp_views.jmrequest_to_bejoined, name='jmrequest_to_bejoined'),
    url(r'^jmrequest_join_me_card/$', myapp_views.jmrequest_join_me_card, name='jmrequest_join_me_card'),
    url(r'^jmrequest_joiner/$', myapp_views.jmrequest_joiner, name='jmrequest_joiner'),
    url(r'^invitation/$', myapp_views.invitation, name='invitation'),
    url(r'^acept_decliner/$', myapp_views.acept_decliner, name='acept_decliner'),
    url(r'^change_is_active_request_receivers/$', myapp_views.change_is_active_request_receivers, name='change_is_active_request_receivers'),
    url(r'^jmrequest_card_past/$', myapp_views.jmrequest_card_past, name='jmrequest_card_past'),
    url(r'^jmrequest_card_next/$', myapp_views.jmrequest_card_next, name='jmrequest_card_next'),
    url(r'^jmrequest_card_wait/$', myapp_views.jmrequest_card_wait, name='jmrequest_card_wait'),
    url(r'^joinme_tobejoined_send/$', myapp_views.joinme_tobejoined_send, name='joinme_tobejoined_send'),
    url(r'^joinme_tobejoined_receivers/$', myapp_views.joinme_tobejoined_receivers, name='joinme_tobejoined_receivers'),
    url(r'^joinme_tobejoined_send_new/$', myapp_views.joinme_tobejoined_send_new, name='joinme_tobejoined_send_new'),
]