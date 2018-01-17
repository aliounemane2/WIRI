from django import forms
from django.db import models
from django.conf import settings
from django.conf.urls.static import static
from fcm.models import AbstractDevice






class Interest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    image = models.FileField(null=True, upload_to='interests/')
    # category = models



    def __str__(self):
        return self.name

    @property
    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)



class Log(models.Model):
    created = models.DateField(auto_now_add=True)
    operation = models.CharField(max_length=255, blank=True, null=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.operation+'  '+self.author


#class SharedCard(models.Model):
#    date_time = models.DateTimeField(auto_now_add=True)





class User(models.Model):
    telephone = models.CharField(max_length=255, unique=True, null=True)
    activation_token = models.CharField(max_length=6, null=True)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=255, unique=False, null=True)
    last_name = models.CharField(max_length=255, unique=False, null=True)
    email = models.CharField(max_length=255, unique=True, null=True)
    password = models.CharField(max_length=255, unique=False, null=True)
    photo = models.FileField(null=True, upload_to='users/')
    interest = models.ManyToManyField(Interest, null=True, blank=True)
    #favoriteContact = models.ForeignKey(FavouriteContact, null=True, blank=True)

    def __str__(self):
        return str(self.telephone)





class UserForm(forms.ModelForm):
    photo = forms.FileField(required=False)
    password = forms.CharField(min_length=8)
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['telephone', 'is_active', 'activation_token']


class UserForm2(forms.ModelForm):
    photo = forms.FileField(required=False)
    #password = forms.CharField(min_length=8)
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['telephone', 'is_active', 'activation_token', 'password']



class FavouriteContact(models.Model):
    # userss = models.ForeignKey(User, related_name='favourite', null=True, blank=True)
    userss = models.ForeignKey(User, related_name='favourite', on_delete=models.CASCADE )
    created = models.DateField(auto_now_add=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return str(self.created)




class MyDevice(AbstractDevice):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL)
    user = models.ForeignKey(User)

#
# class InterestUser(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     interest = models.ForeignKey(Interest, on_delete=models.CASCADE )
#     created = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return self.user.first_name+ ' '+self.user.last_name+' '+self.interest.name
#
#     class Meta:
#         auto_created = True



