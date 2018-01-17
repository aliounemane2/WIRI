from django.db import models
from users.models import *
from django import forms
from datetime import datetime

# from fcm.utils import get_device_model

#MyDevice = get_device_model()




class ChatGroup(models.Model):
    content = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    ## userss = models.ForeignKey(User, related_name='admin_group', on_delete=models.CASCADE)
    userss = models.ForeignKey(User, related_name='admin_group')
    users =  models.ManyToManyField(User, related_name='group_users')

    def __str__(self):
        return self.content


class Message(models.Model):
    content = models.CharField(max_length=255, null=True, blank=True)
    photo = models.FileField(null=True, blank=True, upload_to='chatroom/')
    chatgroup = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    users =  models.ForeignKey(User, related_name='sender')
    users_receivers =  models.ManyToManyField(User, related_name='list_receive')
    # date_created = models.DateTimeField(default=datetime.now())
    date_created = models.DateTimeField(auto_now_add=True, blank=True)



    def __str__(self):
        return str(self.date_created)


class Media(models.Model):
    image = models.FileField(null=True, upload_to='medias/')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return self.id




class ChatGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        # fields = '__all__'
        exclude = ['users', 'created', 'userss']


