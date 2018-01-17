from django.conf.urls import url
from jmspots.views import *
from jmspots import views as myapp_views


urlpatterns = [

    url(r'^$', CategorytList.as_view()),
    url(r'^card/$', CardList.as_view()),
    url(r'^FavouriteCardList/$', FavouriteCardList.as_view()),
    url(r'^event/$', EventList.as_view()),
    url(r'^institution/$', InstitutionList.as_view()),
    url(r'^horaires/$', HorairesList.as_view()),
    url(r'^spot/$', SpotList.as_view()),
    url(r'^usercard/$', UserCardList.as_view()),
    url(r'^usercardfavourite/$', UserCardFavouriteList.as_view()),
    url(r'^listFavourite/$', myapp_views.listFavourite, name='listFavourite'),
    # url(r'^getAllspot/$', myapp_views.getAllspot, name='getAllspot'),
    url(r'^get_Cartes_public/$', myapp_views.get_Cartes_public, name='get_Cartes_public'),
    url(r'^get_Create_Carte/$', myapp_views.get_Create_Carte, name='get_Create_Carte'),
    url(r'^usercardShared/$', myapp_views.usercardShared, name='usercardShared'),
    url(r'^usercardShared_last/$', myapp_views.usercardShared_last, name='usercardShared_last'),
    url(r'^change_is_active_usercard/$', myapp_views.change_is_active_usercard, name='change_is_active_usercard'),
    url(r'^acept_decliner_usercard/$', myapp_views.acept_decliner_usercard, name='acept_decliner_usercard'),
    url(r'^get_Shared_Card/$', myapp_views.get_Shared_Card, name='get_Shared_Card'),
    url(r'^get_Favourite_Card/$', myapp_views.get_Favourite_Card, name='get_Favourite_Card'),
    url(r'^get_Create_Carte_Favourite/$', myapp_views.get_Create_Carte_Favourite, name='get_Create_Carte_Favourite'),
    url(r'^get_Cartes_event_public/$', myapp_views.get_Cartes_event_public, name='get_Cartes_event_public'),
    url(r'^get_Cartes_institution_public/$', myapp_views.get_Cartes_institution_public, name='get_Cartes_institution_public'),
    url(r'^suggestion_card/$', myapp_views.suggestion_card, name='suggestion_card'),
    url(r'^addFavoriteCard/$', myapp_views.addFavoriteCard, name='addFavoriteCard'),
    url(r'^addFavoriteCard2/$', myapp_views.addFavoriteCard2, name='addFavoriteCard2'),

    #url(r'^listcardInstitutionelEvent/$', myapp_views.listcardInstitutionelEvent, name='listcardInstitutionelEvent'),



]