from django import forms
from django.db import models
from users.models import User
from chatroom.models import ChatGroup

from datetime import datetime
from django.forms import extras
import datetime
from datetimewidget.widgets import DateTimeWidget
from django.conf import settings
from django.forms import formset_factory
from django.forms import modelformset_factory






def last_years():
    first_year = datetime.datetime.now().year - 6
    return list(range(first_year + 7, first_year, -1))











class Spot(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return str(self.latitude)+' '+str(self.longitude)+' '+str(self.name)



class SpotForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.TextInput(attrs={'type': 'text'}))
    longitude = forms.FloatField(widget=forms.TextInput(attrs={'type': 'text'}))

    class Meta:
        model = Spot
        fields = '__all__'


class Event(models.Model):
    name = models.CharField(max_length=105)
    description = models.CharField(max_length=255, blank=True, null=True)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    ## chatroom = models.OneToOneField(ChatGroup, blank=True, null=True)
    chatroom = models.OneToOneField(ChatGroup)
    ### date_begin = models.DateField()

    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()

    #  user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class EventForm(forms.ModelForm):

    name= forms.CharField(max_length=100, label='Nom de l evenement ')
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    description = forms.CharField(max_length=255, label='Description de l evenement ')

    date_begin = forms.DateTimeField(label=('Date de Debut'), widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime',  'size':'28', 'height': '20'}),
                                     input_formats=settings.DATETIME_INPUT_FORMATS)
    # date_begin = forms.DateField(widget = forms.SelectDateWidget(years=last_years()))
    date_end = forms.DateTimeField(label=('Date de Fin'), widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime', 'size':'28', 'height': '20'}),
                                   input_formats=settings.DATETIME_INPUT_FORMATS)

    class Meta:
        model = Event
        # fields = '__all__'
        exclude = ['spot', 'chatroom']

        # name = self.cleaned_data['name']
        # description = self.cleaned_data['description']
        # date_begin = self.cleaned_data['date_begin']
        # date_end = self.cleaned_data['date_end']



    #
    # def natural_keys(self):
    #     return self.event.id, self.event.name, self.event.description, self.event.jm_tag, str(self.event.created)


class Institution(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class InstitutionForm(forms.ModelForm):

    name= forms.CharField(max_length=100, label='Nom de l institution', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=255, label='Description de l institution', widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Institution
        exclude = ['spot']




class Horaires(models.Model):


    Lundi = 'Lundi'
    Mardi = 'Mardi'
    Mercredi = 'Mercredi'
    Jeudi= 'Jeudi'
    Vendredi = 'Vendredi'
    Samedi = 'Samedi'
    Dimanche = 'Dimanche'

    DAYS_OF_WEEK = (
        (Lundi, 'Lundi'),
        (Mardi, 'Mardi'),
        (Mercredi, 'Mercredi'),
        (Jeudi, 'Jeudi'),
        (Vendredi, 'Vendredi'),
        (Samedi, 'Samedi'),
        (Dimanche, 'Dimanche'),

    )
    # null=True, blank=True
    days = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    time_degin = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)
    time_degin2 = models.TimeField(null=True, blank=True)
    time_end2 = models.TimeField(null=True, blank=True)
    # time_end2 = models.TimeField(null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.time_degin)







class HorairesForm(forms.ModelForm):
    #days =

    class Meta:
        model = Horaires
        exclude = ['institution']


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)


    def __str__(self):
        return self.name



class Card(models.Model):
    file = models.FileField(null=True, upload_to='cards/')
    jm_tag = models.CharField(max_length=150, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.OneToOneField(Institution, blank=True, null=True)
    event = models.OneToOneField(Event, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type_card = models.CharField(max_length=50, null=True, blank=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return str(self.institution)




class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        # fields = '__all__'
        exclude = ['owner', 'event', 'type_card', 'institution']



class CardFormCustomize(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Card
        fields = '__all__'
        # exclude = ['owner', , 'type_card', 'institution', 'file']
        exclude = ['owner', 'type_card', 'event', 'institution', 'jm_tag']






class UserCard(models.Model):

    RECEIVED = 'RECEIVED'
    DECLINED = 'DECLINED'
    NULL = 'NULL'

    STATE_REQUEST = (
        (RECEIVED, 'RECEIVED'),
        (DECLINED, 'DECLINED'),
        (NULL, 'NULL'),
    )

    sender = models.ForeignKey(User, related_name='sender_card', on_delete=models.CASCADE)
    card = models.ForeignKey(Card)
    date_created = models.DateTimeField(auto_now_add=True)
    users_receivers = models.ForeignKey(User, related_name='users_receivers_card', on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=STATE_REQUEST, default=NULL)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return str(self.sender)





class UserCardFavourite(models.Model):
    RECEIVED = 'RECEIVED'

    STATE_REQUEST = (
        (RECEIVED, 'RECEIVED'),
    )

    sender = models.ForeignKey(User, related_name='sender_cardfavourite', on_delete=models.CASCADE)
    card = models.ManyToManyField(Card)
    date_created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=20, choices=STATE_REQUEST, default=RECEIVED)


    def __str__(self):
        return str(self.sender)

    def natural_key(self):
        return str(self.sender, self.card)


