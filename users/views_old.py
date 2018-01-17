# -*- coding: utf-8 -*-
from _testcapi import return_null_without_error

from django.shortcuts import render
from django.http import Http404
from random import randint
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User, Interest
from rest_framework import status
from users.serializers import UserSerializer, InterestSerializer, FavouriteContactSerializer
from rest_framework.serializers import *
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
from base64 import b64decode
from django.core.files.base import ContentFile
import base64
from jmspots.models import Card

import urllib.parse

# from twilio.rest import TwilioRestClient
from django.conf import settings

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.db.models import Q
from django.contrib.auth import authenticate
# from nexmo import send_message
# from nexmo import *
#from nexmo.libpynexmo.nexmomessage import NexmoMessage
from django.contrib import messages

import imghdr # Used to validate images
#import urllib2 # Used to download images
import urllib.request # Used to download images
from urllib.parse import urljoin
# import urlparse # Cleans up image urls

from io import StringIO
import io

#import cStringIO # Used to imitate reading from byte file
#from PIL import Image # Holds downloaded image and verifies it
import copy # Copies instances of Image
from django.shortcuts import render
import ssl
import ovh
import json








def createActivationToken():
    return randint(100000, 1000000)



class InterestList(APIView):


    def get(self, request):
        interests = Interest.objects.all()
        serializer = InterestSerializer(interests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InterestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)





class FavouriteContactList(APIView):

    def get(self, request):
        favourite = FavouriteContact.objects.all()
        serializer = FavouriteContactSerializer(favourite, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FavouriteContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)





class UserList(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        if data["telephone"]:
            data["activation_token"] = createActivationToken()
            data["is_active"] = False
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance




class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_Favourite(request):
    favourite = FavouriteContact.objects.all()
    # serializer = FavouriteContactSerializer(favourite, many=True)
    serializer = FavouriteContactSerializer(favourite, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def inscription(request):

    """ Permet de gerer l'inscription d'un utilisateur.

    Le scenario d'inscription d'un utilisateur sur Wiri se fait comme suit:
        1 - l'utilisateur saisi un numero de telephone qui existe deja en base
            a - le compte associe a ce numero est actif: on demande a l'utilisateur d'aller se connecter
            b - le compte associe a ce numero est inactif: on lui envoi un token d'activation et on lui demande de poursuivre son inscription
        2 - l'utilisateur saisi un numero de telephone qui n'existe pas en base: On lui creer un compte et on lui demande de l'activer

    """

    telephone = request.data['telephone']

    try:
        u = User.objects.get(telephone=telephone)
        if u.is_active == True:
            return Response(data={
                'status': -1,
                'message': 'Vous etes deja inscrit. Connectez-vous pour acceder a Wiri.',
            })
        else:
            return Response(data={
                'status': 1,
                'message': 'Votre compte n\'est pas encore active. Veuillez saisir le code envoye par SMS',
                'user': {
                    'id': u.id,
                    'telephone': u.telephone,
                    'activation_token': u.activation_token,
                },
            })
    except:
        u = User()
        u.telephone = telephone
        u.is_active = False
        u.activation_token = createActivationToken()

        urls = 'https://www.ovh.com/cgi-bin/sms/http2sms.cgi?&account=sms-sb79455-1&login=qualshore&password=Qsroot15&from=WIRI&to=' + str(telephone) + '&message=' + str(u.activation_token)

        context = ssl._create_unverified_context()
        print (context)
        response = urllib.request.urlopen(urls, context=context)
        print (response)

        #return HttpResponse(response.read())
        print ('cool sms ')
        print ('cool sms ')
        print ('cool sms ')
        print ('cool sms ')
        print ('cool sms ')


        # Decommenter pour activer l'envoie de sms
        #
        # params = {
        #     'text': 'Votre code WIRI est : ' + str(u.activation_token),
        #     'to': telephone,
        # }
        #
        # url = 'https://lampush.lafricamobile.com/api?accountid=QUALSHORE&password=q04L5r321@&' + urllib.parse.urlencode(
        #     params)
        #
        # context = ssl._create_unverified_context()
        # response = urllib.request.urlopen(url, context=context)


        u.save()
        return Response(data={
            'status': 0,
            'message': 'Votre inscription est bien prise en compte, Veuillez saisir le code envoye par SMS',
            'user': {
                'id': u.id,
                'telephone': u.telephone,
                'activation_token': u.activation_token,
            },
        })





@api_view(['PUT'])
def validation_Code(request):

    if request.method == "PUT":
        try:
            u = User.objects.get(activation_token=request.data["code"], telephone=request.data["telephone"])
            u.activation_token = None
            u.is_active = True
            u.save()
            return Response(data={
                'status': 0,
                'message': 'Votre compte Wiri est active avec succes.',
            })

        except:
            return Response(data={
                'status': 1,
                'message': 'Echec de l\'activation du compte. Verifiez votre code s\'il vous plait.',
            })


# Compléments d'information
@api_view(['PUT'])
def complements_info(request):

    """ Permet de compléter les informations de l'utilisateur

        Le scenario du complément d'information d'un utilisateur sur Wiri se fait comme suit:

            - l'utilisateur doit d'abord exister en base de donnée et son compte soit actif:
            l'utilisateur doit remplir son prénom , nom , email et mot de passe qui sont insérés en base de donnée

        """



    if request.method == "PUT":

        try:

            numero = request.data['telephone']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']

            user = User.objects.get(telephone=numero)
            if user is not None:

                user.first_name= first_name
                user.last_name=last_name
                user.email=email
                user.password=password
                user.save()

                return Response(data={
                    'status': 0,
                    'message': 'Bienvenue sur wiri, votre profil a été bien pris prise en compte',
                    'user': {
                        'id': user.id,
                        'telephone': user.telephone,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'password': user.password,
                        'photo': str(user.photo),
                    },})
        except:
            return Response(data={'status': 1, 'message': 'Echec de l\' enregistrement des informations complémentaires'})




@api_view(['PUT'])
def save_interest(request):

    """ Permet de modifier les centres d'interet d'un utilisateur.

        Le scenario de l'enregistrement des centres d'intéret d'un utilisateur sur Wiri se fait comme suit:

            1 - l'utilisateur saisi un numero de telephone qui existe deja en base et
            un tableau des centres d'intérets que l'utilisateur a choisit
             et qui sont insérés en base de données

        """


    if request.method == "PUT":
        telephone = request.data['telephone']
        user = User.objects.get(telephone=telephone)
        print(user)

        interest = request.data['interest']
        print (interest)



        i = 0
        print(' debut boucle ')
        while i < (len(interest)):
            print (interest[i])
            user.interest.add(interest[i])
            i += 1

        print (' fin boucle ')
        user.save()

        tt = []
        i = 0

        interests = User.objects.filter(telephone=telephone).values('interest')
        print(interests)
        while i < (len(interests)):
            print (interests[i])
            tt.append(interests[i]['interest'])
            print(interests[i]['interest'])

            i += 1

        return Response(
                    data={'status': 0,
                          'message': 'Vos centres d\' interet ont bien été enregsitrés',
                          'user': {
                              'id': user.id,
                              'telephone': user.telephone,
                              'first_name': user.first_name,
                              'last_name': user.last_name,
                              'email': user.email,
                              'password': user.password,
                              'photo': str(user.photo),
                              'interest': interest
                          },
                          }


        )
    else:

        return Response(data={'status': 1, 'message': 'Echec de l\' enregsitrement du centre d\'interet'})





# Liste de centre d'intéret
@api_view(['GET'])
def listInterest(request, numero):
    try:
        listInterest = User.objects.values('interest').filter(telephone=numero)
        serialiser = InterestSerializer(listInterest)
        return Response(data={listInterest})
    except User.DoesNotExist:
            raise Http404




# L'ensemble des contacts qui sont dans wiri
@api_view(['GET'])
def contacts(request):

    if request.method == "GET":
        try:
            u = User.objects.filter(is_active=True)
            serialiser = UserSerializer(u, many=True)
            return Response(serialiser.data)
        except:
            return Response(data={'status': -1, 'message': ' Utilisateur inextant '})



@api_view(['POST'])
def authentification(request):

    if request.method == "POST":

        telephone = request.data['telephone']
        password = request.data['password']

        try:
            user = User.objects.get(telephone=telephone)
            if user.telephone == telephone and user.password==password:

                interest = User.objects.filter(telephone=telephone).values('interest')
                print(interest)

                tt = []
                i=0
                while i < (len(interest)):
                    print (interest[i])
                    tt.append(interest[i]['interest'])
                    print(interest[i]['interest'])


                    i+=1

                if len(interest) != 0:
                    return Response(
                        data={'status': 0,
                              'message': 'L authentification reussit',
                              'user': {
                                  'id': user.id,
                                  'telephone': user.telephone,
                                  'first_name': user.first_name,
                                  'last_name': user.last_name,
                                  'email': user.email,
                                  'password': user.password,
                                  'photo': str(user.photo),
                                  'interest': tt
                                },
                              })

                else:
                    print(' Pas de centre dinetret ')
                    tt.append()
                    return Response(
                        data={'status': 0,
                              'message': 'L authentification reussit',
                              'user': {
                                  'id': user.id,
                                  'telephone': user.telephone,
                                  'first_name': user.first_name,
                                  'last_name': user.last_name,
                                  'email': user.email,
                                  'password': user.password,
                                  'photo': str(user.photo),
                                  'interest': tt
                              },
                              })

            else:
                return Response(data={'status':1, 'message':'Le Login ou le mot de passe est inccorect'})
        except:
            return Response(data={'status': 1, 'message': 'Le Login ou le mot de passe est inccorect'})











# ok
@api_view(['GET'])
def verif_user(request, telephone):

    if request.method == "GET":

        # telephone = request.data['telephone']

        try:
            user = User.objects.get(telephone=telephone)
            # if user.is_active == True:
            if user.telephone == telephone and user.is_active == True:
                return Response(
                    data={'status': 0,
                          'message': 'True',
                          'user': {
                              'id': user.id,
                              'telephone': user.telephone,
                              'first_name': user.first_name,
                              'last_name': user.last_name,
                              'email': user.email,
                              'password': user.password,
                                },
                          })
            else:
                return Response(data={'status': 1, 'message': 'False'})
        except:
            return Response(data={'status': 1, 'message': 'False'})





# #ok
# @api_view(['POST'])
# def verif_user(request):
#
#     if request.method == "POST":
#
#         telephone = request.data['telephone']
#
#         try:
#             user = User.objects.get(telephone=telephone)
#             # if user.is_active == True:
#             if user.telephone == telephone and user.is_active==True:
#                 return Response(
#                     data={'status': 0,
#                           'message': 'Utilisateur existant',
#                           'user': {
#                               'id': user.id,
#                               'telephone': user.telephone,
#                               'first_name': user.first_name,
#                               'last_name': user.last_name,
#                               'email': user.email,
#                               'password': user.password,
#                             },
#                           })
#             else:
#                 return Response(data={'status':1, 'message':'Utilisateur nest pas de WIRI'})
#         except:
#             return Response(data={'status': 1, 'message': 'Le Login ou le mot de passe est inccorect'})











@api_view(['POST'])
def addFavoriteContact(request):

    if request.method == "POST":

        try:
            idContact = request.data['id']
            listeContact = request.data['favouriteContact']
            print (listeContact)

            favouriteContacts = FavouriteContact()

            id_user = User.objects.get(id=idContact)
            favouriteContacts.userss = id_user
            print (id_user)
            print (favouriteContacts.userss)


            i = 0
            print(' debut boucle ')

            while i < (len(listeContact)):
                print (listeContact[i])
                favouriteContacts.save()
                favouriteContacts.users.add(listeContact[i])
                # favouriteContacts.users.add(listeContact[i])
                i += 1
                print (' fin boucle ')

            # favouriteContacts.save()

            return Response(
                data={
                    'status': 0,
                    'message': 'Enregistrement effectué avec success ',
                    # 'favourite': favouriteContacts.userss
                })

        except:
            return Response(data={'status': 1, 'message': 'Echec de l\'enregistrement'})




@api_view(['POST'])
def getFavoriteContact(request):

    if request.method == "POST":

            idContact = request.data['id']
            # favouriteContact = FavouriteContact.objects.get(userss=idContact)
            favouriteContact = FavouriteContact.objects.filter(userss=idContact)
            serializer = FavouriteContactSerializer(favouriteContact, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(data={'status': 1, 'message': 'Affichage non effectué'})




# La bonne
@api_view(['POST'])
def addFavoriteContact2(request):

    serializer = FavouriteContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors)







@api_view(['PUT'])
def modify_info(request):
    if request.method == "PUT":

        try:
            numero = request.data['telephone']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']

            user = User.objects.get(telephone=numero)
            if user is not None:

                user.first_name= first_name
                user.last_name=last_name
                user.email=email
                user.save()

                return Response(data={
                    'status': 0,
                    'message': 'La modification de votre profil a été bien prise en compte',
                    'user': {
                        'id': user.id,
                        'telephone': user.telephone,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                    },})
        except:
            return Response(data={'status': 1, 'message': 'Echec de la modification des informations'})




@api_view(['PUT'])
def modify_password(request):
    if request.method == "PUT":

        try:

            old_password = request.data['old_password']
            new_password = request.data['new_password']

            numero = request.data['telephone']

            user = User.objects.get(telephone=numero)

            if user is not None and user.password==old_password:

                user.password= new_password
                user.save()

                return Response(data={
                    'status': 0,
                    'message': 'La modification de votre mot de passe a été bien prise en compte',
                    'user': {
                        'id': user.id,
                        'telephone': user.telephone,
                        'password': user.password
                    },})
            else:
                return Response(data={'status': 1, 'message': 'Echec de la modification du mot de passe'})
        except:
            return Response(data={'status': 1, 'message': 'Echec de la modification du mot de passe'})






@api_view(['PUT'])
def edit_photo(request):
    if request.method == "PUT":
        try:
            numero = request.data['telephone']
            photo = request.data['photo']
            user = User.objects.get(telephone=numero)

            if user is not None:

                user.photo= photo
                user.save()

                return Response(data={
                    'status': 0,
                    'message': 'La modification de votre photo a été bien prise en compte',
                    'user': {
                        'id': user.id,
                        'photo': str(user.photo),
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'password': user.password,
                        'telephone': user.telephone
                    },})
            else:
                return Response(data={'status': 1, 'message': 'Echec de la modification du photo de profil'})
        except:
            return Response(data={'status': 1, 'message': 'Echec de la modification du photo de profil'})




@api_view(['PUT'])
def save_image(request):

    if request.method == "PUT":
        try:
            numero = request.data['telephone']

            photo = request.data['photo']
            print (' cc ')
            user = User.objects.get(telephone=numero)
            print (' ok 1')

            # request.data['photo'] = str(user.telephone) + '.png'

            user.photo = photo
            # print (user.photo)
            print (' ok 2')

            user.save()
            print (' ok 3')
            return Response(data={'status': 0, 'message': 'Success Photo', 'photo':str(user.photo)})

        except:
            return Response(data={'status': 1, 'message': 'Echec de la Photo'})






@api_view(['PUT'])
def forget_password(request):
    if request.method == "PUT":

        try:
            numero = request.data['telephone']
            email = request.data['email']


            photo = request.data['photo']
            print (' cc ')
            user = User.objects.get(telephone=numero)
            print (' ok 1')

            # request.data['photo'] = str(user.telephone) + '.png'
            user.photo = photo
            print (user.photo)
            print (' ok 2')

            user.save()
            print (' ok 3')
            return Response(data={'status': 0, 'message': 'Success Photo'})

        except:
            return Response(data={'status': 1, 'message': 'Echec de la Photo'})





@api_view(['PUT'])
def send_email_password(request):

    if request.method == "PUT":
        try:
            # user = User.objects.get(email=email)
            emails = request.data['email']

            # user = User.objects.filter(Q(email=emails) | Q(telephone=emails))
            # user = User.objects.filter(Q(email=emails)) | User.objects.filter(Q(telephone=emails))
            user = User.objects.filter(Q(telephone=emails) | Q(telephone=emails) )
            # user = User.objects.filter(Q(email=emails) | Q(telephone=emails)).values('password', 'email')

            new_password = randint(100000, 1000000)

            print (user)
            user.update(password=new_password)

            print(' ok 1')
            print(user[0].email)


            # print (user[6])
            print(' ok 2')

            if user is not None:
                print (' cccccc ')
                print (new_password)

                print (' 1111111111 ')


                send_mail('Nouveau mot de passe', 'Your password '+str(new_password), '',
                          [user[0].email])
                return Response(data={'status': 0, 'message': 'Success Email'})

            else:
                return Response(data={'status': 1, 'message': 'Echec de l\' envoie de l\'email  1'})
        except:
            return Response(data={'status': 1, 'message': 'Echec de l\' envoie de l\'email 2'})





@api_view(['POST'])
def push_notification_fcm(request):

    if request.method == "POST":
        try:

            id_User = request.data['id']
            token = request.data['token']

            print (id_User)
            print (token)
            print ('steps 0 ')


            try:
                print ('steps 1 ')

                e = MyDevice.objects.get(user_id=id_User)


                if e is not None:
                    e.reg_id = token
                    e.save()
                    print ('steps 2 ')

                    return Response(data={'status': 0, 'message': 'Creation effectué'})


            except:

                print ('steps 3')

                MyDevice.objects.create(dev_id=id_User, reg_id=token, is_active=True, user_id=id_User)
            # p.save() user_id=id_User

            # mydevice = MyDevice.objects.create(reg_id=token, is_active=True, user_id=id_User)

                return Response(data={'status': 0, 'message': 'Creation effectué'})

        except:
            return Response(data={'status': 1, 'message': 'Echec de la création'})




@api_view(['POST'])
def send_fcm_notification(request):

    if request.method == "POST":
        try:
            # id_User = request.data['id']

            token = request.data['token']

            device = MyDevice.objects.get(reg_id=token)
            # device = MyDevice.objects.get(reg_id=token)
            print(' cc ')

            #device = FCMDevice.objects.all().first()

            # device.send_message("Title", "Message")


            device.send_message({'message': 'salut '}, delay_while_idle=True, time_to_live=5)
            a = device.send_message({'message': 'salut '}, delay_while_idle=True, time_to_live=5)
            print (a)
            return Response(data={'status': 0, 'message': 'Notification envoyé '})

        except:
            return Response(data={'status': 1, 'message': 'Echec Echec de la création et de lenvoie '})




                # @api_view(['PUT'])
# def send_email_password(request):
#
#     if request.method == "PUT":
#         try:
#             # user = User.objects.get(email=email)
#             emails = request.data['email']
#             # num = request.data['telephone']
#
#             # user = User.objects.filter(Q(email=emails) | Q(telephone=emails))
#             # user = User.objects.filter(Q(email=emails)) | User.objects.filter(Q(telephone=emails))
#             # user = User.objects.filter(Q(email=emails)) | User.objects.filter(Q(telephone=emails))
#             user = User.objects.filter(Q(email=emails) | Q(telephone=emails)).values('password', 'email')
#
#             print (user)
#
#             print(' ok 1')
#             print(user[0].email)
#
#             # print (user[6])
#             print(' ok 2')
#
#             if user is not None:
#                 print (' cccccc ')
#                 new_password = randint(100000, 1000000)
#                 print (new_password)
#
#                 print (' 1111111111 ')
#                 user[0].password = new_password
#                 print (user[0].password)
#                 user[0].password = "ddd"
#                 print (' dfsdf010f ')
#                 print (' 2222222222 ')
#                 print (user[0].password)
#                 print (user[0].save())
#                 print ('final ')
#                 print (user[0].password)
#
#                 print (user[0]['password'] == new_password)
#
#                 print(' ok 3')
#                 ### user.save() à décommenter
#                 # user[0].save(update_fields=['password'])
#                 user[0].save(update_fields=['password'])
#                 # user.update(['password'])
#                 print(' ok 4')
#                 user[0].save()
#                 print(' ok 5')
#
#                 # send_mail('Nouveau mot de passe', 'Your password '+str(new_password), '',
#                 #          [user[0].email])
#                 return Response(data={'status': 0, 'message': 'Success Email'})
#
#             else:
#                 return Response(data={'status': 1, 'message': 'Echec de l\' envoie de l\'email  1'})
#         except:
#             return Response(data={'status': 1, 'message': 'Echec de l\' envoie de l\'email 2'})








# @api_view(['POST'])
# def email(request):
#
# if request.method == "POST":
#
#     try:
#
#         numero = request.data['telephone']
#         email = request.data['email']
#
#         user = User.objects.get(email=email)
#         # user = User.objects.filter(Q(email=email) | Q(telephone=numero))
#         print (user)
#
#         print(' ok 1')
#         # print (user.get('email'))
#
#         if user is not None:
#
#             new_password = randint(100000, 1000000)
#             print (new_password)
#
#             print (user.email)
#
#             print(' ok 2')
#
#             send_mail('Nouveau mot de passe', 'Your password ' + str(new_password),
#                       'alioune.mane@qualshore.com',
#                       [user.email])
#
#             print(' ok 3')
#
#             return Response(data={'status': 0, 'message': 'Success Email'})
#
#         else:
#             return Response(data={'status': 1, 'message': 'Echec de l\' envoie de l\'email  1'})
#
#     except:
#         return Response(data={'status': 1, 'message': 'Echec de l\' envoie de l\'email 2'})













    # subject = request.POST.get('subject', '')
    # message = request.POST.get('message', '')
    # from_email = request.POST.get('from_email', '')
    # if subject and message and from_email:


    #     try:
    #         send_mail(subject, message, from_email, ['admin@example.com'])
    #     except BadHeaderError:
    #         return HttpResponse('Invalid header found.')
    #     return HttpResponseRedirect('/contact/thanks/')
    # else:
    #     # In reality we'd use a form class
    #     # to get proper validation errors.
    #     return HttpResponse('Make sure all fields are entered and valid.')



    # send_mail('<Your subject>', '<Your message>', 'alioune.mane@qualshore.com', ['alioune.mane@qualshore.com'])
    # return HttpResponse(' Envoyé ')

























#
# @api_view(['PUT'])
# def valid_img(img):
#     """Verifies that an instance of a PIL Image Class is actually an image and returns either True or False."""
#     type = img.format
#     if type in ('GIF', 'JPEG', 'JPG', 'PNG'):
#         try:
#             img.verify()
#             return True
#         except:
#             return False
#     else: return False
#
#
#
#
# @api_view(['PUT'])
# def download_image(url):
#     """Downloads an image and makes sure it's verified.
#
#     Returns a PIL Image if the image is valid, otherwise raises an exception.
#     """
#
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'} # More likely to get a response if server thinks you're a browser
#     r = urllib.request.Request(url, headers=headers)
#     request = urllib.request.urlopen(r, timeout=10)
#     image_data = StringIO.StringIO(request.read()) # StringIO imitates a file, needed for verification step
#     # image_data = CStringIO.StringIO(request.read()) # StringIO imitates a file, needed for verification step
#     img = Image.open(image_data) # Creates an instance of PIL Image class - PIL does the verification of file
#     img_copy = copy.copy(img) # Verify the copied image, not original - verification requires you to open the image again after verification, but since we don't have the file saved yet we won't be able to. This is because once we read() urllib2.urlopen we can't access the response again without remaking the request (i.e. downloading the image again). Rather than do that, we duplicate the PIL Image in memory.
#     if valid_img(img_copy):
#         return img
#     else:
#         # Maybe this is not the best error handling...you might want to just provide a path to a generic image instead
#         return Response('An invalid image was detected when attempting to save a Product!')
#
#
#
# @api_view(['PUT'])
# def save_image(request, ):
#     url = ''
#
#
#
#     numero = request.data['telephone']
#     photo = request.data['photo']
#     user = User.objects.get(telephone=numero)
#
#     if user.photo != '' and url != '':
#         image = download_image(url) # See function definition below
#         try:
#             filename = urljoin.urlparse(url).path.split('/')[-1]
#             user.photo = filename
#             tempfile = image
#             tempfile_io = StringIO.StringIO() # Will make a file-like object in memory that you can then save
#             tempfile.save(tempfile_io, format=image.format)
#             user.photo.save(filename, ContentFile(tempfile_io.getvalue()), save=False) # Set save=False otherwise you will have a looping save method
#             return Response(' Enregistrement effectué ')
#         except:
#             # print ("Error trying to save model: saving image failed: ")
#             return Response('  Erreur enregistrement image')
















def testovh2(request):
    urls = 'https://www.ovh.com/cgi-bin/sms/http2sms.cgi?&account=sms-sb79455-1&login=qualshore&password=Qsroot15&from=WIRI&to=0033603136995&message=PM10'

    code=198374
    params = {
        'to': '0033603136995',
        # 'to': '00221771096893',
        'message': 'Votre code WIRI est : ' +str(code)
    }


    # url = 'https://rest.nexmo.com/sms/json?' + urllib.parse.urlencode(params)
    url = 'https://www.ovh.com/cgi-bin/sms/http2sms.cgi?&account=sms-sb79455-1&login=qualshore&password=Qsroot15&from=WIRI' + urllib.parse.urlencode(params)

    # fin

    # response = urllib.request.urlopen(url)

    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    # fin









    # return HttpResponse(response.read())



    return HttpResponse(' COOL ')






def testovh(request):
    #client = ovh.Client('ovh-eu', application_key='your_application_key',
    #                    application_secret='your_application_secret, consumer_key='' )



    #client = ovh.Client('ovh-eu', application_key='FK0iABRRwdrjj7vd',
    #                   application_secret='SDF3d9yLRoeyqSII85IbxNeGupZzfHmm', consumer_key='sms-sb79455-1')

    # client = ovh.Client('ovh-eu', application_key='sb79455-ovh',
    #                     application_secret='Qsroot15@', consumer_key='TnpZAd5pYNqxk4RhlPiSRfJ4WrkmII2i')






    client = ovh.Client('ovh-eu', application_key='R84bg6U70Q8JWBEJ',
                        #application_secret='tzszKN9eDlrNX55Gt0Z2vz8oScIf68C8', consumer_key='wzhCszi3FcijXiePtYFzqWUnXL1V6XTc')
                        application_secret='VbEJqZYKqa8xgEH0sIRZ2Ohd2NudKPUb', consumer_key='Rt0BzniDKNJXseJw5S9n59L35SJpi1CG')





    ck = client.new_consumer_key_request()
    # ck.add_recursive_rules(ovh.API_READ_WRITE, '/')
    print(ck.request())

    # ck.add_recursive_rules(ovh.API_READ_ONLY, "/me")
    ck.add_recursive_rules(ovh.API_READ_ONLY, "/me")
    ck.add_recursive_rules(ovh.API_READ_WRITE, "/sms")

    print(ck.request())




    print (' sms debut ')
    res = client.get('/sms')
    print (res)
    print (' sms fin ')

    print (' sms jobs debut ')
    url = '/sms/' + res[0] + '/jobs/'
    print (' sms jobs fin ')

    # urls = 'https://www.ovh.com/cgi-bin/sms/http2sms.cgi?&account=sms-sb79455-1&login=sb79455-ovh&password=&Qsroot15@from=RESTAUPRIVE&to=0033603136995&contentType=text/xml&message=#title#%0d#message#&noStop=1'
    # url = 'https://www.ovh.com/cgi-bin/sms/http2sms.cgi?&account=sms-sb79455-1&login=sb79455-ovh&password=&Qsroot15@from=RESTAUPRIVE'

# qualshore-Root15@
    # result_send = client.post(url,
    result_send = client.post(url,
                              charset='UTF-8',
                              coding='7bit',
                              message="Votre message",
                              noStopClause=False,
                              priority='high',
                              receivers=["+33603136995"],
                              senderForResponse=False,
                              validityPeriod=2880,
                              # sender="Le nom du sender tel que proposé dans l'admin"
                              sender="papa"
                              )

    print (json.dumps(result_send, indent=4))

    return HttpResponse(' COOL ')






def index(request):
    return render(request, 'index.html', {})



def contacter_wiri(request):

    send_mail('Contact', request.POST['nom_contact']+'    '+request.POST['message']+'  '+request.POST['sujet'] ,
              'aliounemane2@gmail.com', [request.POST['email']])
    return render(request, 'index.html', {'sucess': ' Votre mail a été bien envoyé '})


def index_office(request):
    return render(request, 'office/login.html')



def dashboard(request):

    us = request.session.get('id')
    user = User.objects.get(id=us)

    request.session['first_name'] = user.first_name
    request.session['last_name'] = user.last_name
    request.session['id'] = user.id
    request.session['telephone'] = user.telephone

    cards = Card.objects.filter(owner=user)
    print (cards)
    if cards.count() > 0:
        page = '#page'
        return render(request, 'dashboard.html', locals())
    page = 'page'
    return render(request, 'dashboard.html', {})

    return render(request, 'dashboard.html')


def login_account(request):

    # user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))

    if User.objects.filter(email=request.POST.get('email'), password=request.POST.get('password')).count() == 1:
        page = '#'

        user = User.objects.get(email=request.POST.get('email'), password=request.POST.get('password'))
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        request.session['id'] = user.id
        request.session['telephone'] = user.telephone
        cards = Card.objects.filter(owner=user)
        print (cards)
        if cards.count() > 0:
            page = '#page'
            return render(request, 'dashboard.html', locals())
        page = '#page'
        return render(request, 'dashboard.html', locals())

    else:

        error = 'Login ou mot de passe Incorrect'
        return render(request, 'office/login.html', {'error': error})


    #     lesevenements = Evenement.objects.filter(utilisateur=user)
    #     if lesevenements.count() > 0:
    #         page = '#page'
    #     if user.type == 'O':
    #         return render(request, 'dashboard.html', locals())
    #     if user.type == 'I':
    #         lespo = Pageofficielle.objects.filter(institution=(Institution.objects.get(utilisateur=user)))
    #         if lespo.count() > 0:
    #             page = '#page'
    #         return render(request, 'dashboard2.html', locals())
    # request.session['connexion'] = True

        # return render(request, 'office/login.html', {'error': 'Echec authentification'})


def logout_account(request):

    request.session.flush()
    return render(request, 'index.html', {})



def send_message_mane(request): #  revoir
    # send_message(frm='+221771096893', to='+221779258627', message='My sms message body')
    send_message(frm='+221771096893', to='+221779258627', message='My sms message body')
    return HttpResponse(' Fait ')



def signup(request):
    return render(request, 'office/register.html')


def signup_account(request):

    first_name= request.POST['first_name']
    last_name= request.POST['last_name']
    email= request.POST['email']
    password1= request.POST['password1']
    password2= request.POST['password2']
    telephone= request.POST['telephone']


    try:
        User.objects.get(telephone=telephone)

        message_telephone = 'Numéro  Téléphone Existant'
        print ('Numéro téléphone Existant')
        return render(request, 'office/register.html',
                      {'message_telephone': message_telephone})

    except User.DoesNotExist:

        try:
            User.objects.get(email=email)
            message_email = ' Email Existant'
            print ('Email  Existant')
            return render(request, 'office/register.html', {'message_email': message_email})

        except:

            if password1 == password2:


                code = randint(100000, 1000000)

                user = User()
                user.telephone = telephone
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.password = password1
                user.activation_token=code
                user.is_active=False
                user.photo = str('users/photo.jpg')
                user.save()

                params = {
                    'to': telephone,
                    'message': 'Votre code WIRI est : ' + str(user.activation_token)
                }

                # url = 'https://rest.nexmo.com/sms/json?' + urllib.parse.urlencode(params)
                ### url = 'https://www.ovh.com/cgi-bin/sms/http2sms.cgi?&account=sms-sb79455-1&login=qualshore&password=Qsroot15&from=WIRI'+urllib.parse.urlencode(params)
                ###########url = 'https://www.ovh.com/cgi-bin/sms/http2sms.cgi?&account=sms-sb79455-1&login=qualshore&password=Qsroot15&from=WIRI'+urllib.parse.urlencode(params)

                urls = 'https://www.ovh.com/cgi-bin/sms/http2sms.cgi?&account=sms-sb79455-1&login=qualshore&password=Qsroot15&from=WIRI&to='+str(telephone)+'&message='+str(user.activation_token)

                context = ssl._create_unverified_context()
                print (context)
                response = urllib.request.urlopen(urls, context=context)
                print (response)

                #return HttpResponse(response.read())
                print ('cool sms ')
                print ('cool sms ')
                print ('cool sms ')
                print ('cool sms ')
                print ('cool sms ')


                send_mail(' Code de Validation ', ' Le code de Validation est  :   '+str(user.activation_token),
                          'aliounemane2@gmail.com', [str(email)])

                # Bon code avec Nexmo
                # debut
                # params = {
                #     'api_key': '6d792c50',
                #     'api_secret': 'b6082b3c77e561cf',
                #     'to': '+221771096893',
                #     'from': 'NEXMO',
                #     'text': 'Votre code WIRI est : ' +str(code)
                # }
                # Ancien code avec NEXMO
                # url = 'https://rest.nexmo.com/sms/json?' + urllib.parse.urlencode(params)
                # fin


#### https: // lampush.lafricamobile.com / api?accountid = QUALSHORE & password = q04L5r321 @ & text = Helllo & to = 00221778605050

                # params = {
                #     'accountid': 'QUALSHORE',
                #     'password': 'q04L5r321@',
                #     'text': 'Votre code WIRI est : ' +str(code),
                #     'to': telephone,
                # }
                #
                #
                # url = 'https://lampush.lafricamobile.com/api?' + urllib.parse.urlencode(params)
                # response = urllib.request.urlopen(url)





                # Bon code avec API SMS
                # debut
                # params = {
                #     'text': 'Votre code WIRI est : '+str(code),
                #     'to': telephone,
                # }
                #
                # url = 'https://lampush.lafricamobile.com/api?accountid=QUALSHORE&password=q04L5r321@&' + urllib.parse.urlencode(
                #     params)
                # ### url = 'https://lampush.lafricamobile.com/api?' + urllib.parse.urlencode(params)
                #
                # context = ssl._create_unverified_context()
                # response = urllib.request.urlopen(url, context=context)
                # fin









                # return HttpResponse(response.read())







                # return HttpResponse(response.read())
                # print ('  Inscription reussit ')
                # send_mail(' Inscription fait avec success',
                #           request.POST['first_name'] +'  '+ request.POST['last_name'],
                #           'aliounemane2@gmail.com', [request.POST['email']])
                return render(request, 'office/register2.html',{'user': user.id})

            else:
                message_password = 'Password non Identique '
                print (' Password non identique ')
                return render(request, 'office/register.html',
                              {'message_password': message_password})



def signup_account2(request):

    # u = User.objects.get(activation_token=request.POST.get('user.activation_token'))
    try:
        u = User.objects.get(activation_token=request.POST['code'])
        u.is_active = True
        u.save()
        print (u)
        print (' COOL ')
        print (' OUI BIEN FAIT  ')
        message_code = 'Inscription fait avec success '
        send_mail(' Inscription fait avec success',
                  u.first_name+'  '+ u.last_name,
                  'aliounemane2@gmail.com', [u.email])
        return render(request, 'office/login.html', {'message_code': message_code})

    except:
        message_code = 'Verifiez le code d activation '
        print (' Code d activation non identique ')
        return render(request, 'office/register2.html',
                      {'message_password': message_code})





def forget_password_account(request):
    user = User.objects.get(email=request.POST['email'])

    try:

        print (user)
        new_password = randint(100000, 1000000)
        user.password= new_password
        user.save()
        # user.update(password=new_password)
        # print(user[0].email)
        # if user is not None:
        send_mail(' Nouveau Mot de passe',
                  'Voici votre nouveau mot de passe  ' + str(new_password),
                  'aliounemane2@gmail.com', [request.POST['email']])
        message = ' Votre mot de passe a été envoyé par mail '
        return render(request, 'office/login.html', {'message': message})

    except:

        message = ' Votre mail ne se trouve pas sur la base de données'
        return render(request, 'office/forget_password.html', {'message': message})





def forget_password(request):
    return render(request, 'office/forget_password.html', {})



def mane_message(request):

    # # with nexmo
    # params = {
    #     'api_key': 'df963b26',
    #     'api_secret': 'acb88028',
    #     'to': '+221771096893',
    #     'from': '+2211096893',
    #     'text': 'WIRI votre code est '
    # }
    #
    # url = 'https://rest.nexmo.com/sms/json?'+urllib.parse.urlencode(params)


    params = {
        'text': 'votre code wiri',
        'to': '00221771096893',
    }

    ## https: // lampush.lafricamobile.com / api?accountid = QUALSHORE & password = q04L5r321 @ & text = Helllo & to = 00221778605050


    url = 'https://lampush.lafricamobile.com/api?accountid=QUALSHORE&password=q04L5r321@&' + urllib.parse.urlencode(params)
    ### url = 'https://lampush.lafricamobile.com/api?' + urllib.parse.urlencode(params)

    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)

    # urllib.urlopen("https://no-valid-cert", context=context)



    return HttpResponse(response.read())



def mane_message_nexmo(request):

    code = randint(100000, 1000000)
    params = {
        'api_key': '6d792c50',
        'api_secret': 'b6082b3c77e561cf',
        'to': '+221771096893',
        'from': 'NEXMO',
        'text': 'Votre code WIRI est '+str(code)
    }

    url = 'https://rest.nexmo.com/sms/json?'+urllib.parse.urlencode(params)

    response = urllib.request.urlopen(url)
    return HttpResponse(response.read())




def twilio_sendmess(request):
    TWILIO_ACCOUNT_SID = 'AC149fc8ff0f95e8bd6ec2a56d81b751ff'
    TWILIO_AUTH_TOKEN = 'f2e2c35a7aa9ccfa46cc07606fbd635a'

    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    response = client.messages.create(body='sdfdff je suis en test  ', to='+221779258627',from_='+12056710441')
    return HttpResponse(' CC ')



# def profil(request):
#
#     u = User.objects.all()
#     if request.method == "POST":
# 		if request.POST['ok']=='Annuler':
# 			return dashboard(request)
# 		formU= UtilisateurForm(request.POST,instance=u)
# 		if formU.is_valid():
# 			formU.save()
# 			request.session['nom']=formU.cleaned_data['nom']
# 		 	request.session['prenom']=formU.cleaned_data['prenom']
# 			if u.type=="O" :
# 				return dashboard(request)
# 			elif u.type=="I" :
# 				formI=InstitutionForm(request.POST,instance=Institution.objects.get(utilisateur=u))
# 				if formI.is_valid():
# 					formI.save()
# 					return dashboard(request)
#     else:
#         formUser = UserForm(instance=u)
#         if u.type=='I':
# 			i=Institution.objects.get(utilisateur=u)
# 			formI=InstitutionForm(instance=i)
# 			is_institution=True
# 		else:
# 			is_institution=False
# 	return render(request,'profil.html',locals())


def profil(request):
    us = request.session.get('id')
    user = User.objects.get(id=us)
    print (' CCCCCCCCCCCCCCC ')
    print (user)
    print (user.first_name)
    print (user.last_name)


    request.session['first_name'] = user.first_name
    request.session['last_name'] = user.last_name
    request.session['id'] = user.id
    request.session['telephone'] = user.telephone

    cards = Card.objects.filter(owner=user)
    print (cards)
    if cards.count() > 0:
        page = '#page'
        # return render(request, 'dashboard.html', locals())
    page = '#page'
    # return render(request, 'dashboard.html', {})







    if request.method == 'POST':  # S'il s'agit d'une requête POST

        print (' Debut POST ')

        # if request.POST['ok']=='Annuler':
        #     print (' Annuler ')
        #     cards = Card.objects.filter(owner=user)
        #     print (cards)
        #     if cards.count() > 0:
        #         page = '#page'
        #         return render(request, 'dashboard.html', locals())
        #     page = '#page'
        # return render(request, 'dashboard.html', locals())

        ######## ancien  formUser = UserForm(request.POST or None, instance=user)
        formUser = UserForm(request.POST or None, request.FILES or None, instance=user)
        # formUser = UserForm(request.POST, instance=user or None)
        print(' FORMULAIRE ')
        print(formUser)
        if formUser.is_valid():

            print (' Enregister 2')

            first_name = formUser.cleaned_data['first_name']
            last_name = formUser.cleaned_data ['last_name']
            email = formUser.cleaned_data['email']
            password = formUser.cleaned_data['password']
            photo = formUser.cleaned_data['photo']
            formUser.save()

            print (' FIN SAVE ')

            request.session['first_name'] = formUser.cleaned_data['first_name']
            request.session['last_name'] = formUser.cleaned_data['last_name']

            cards = Card.objects.filter(owner=user)
            print (cards)
            if cards.count() > 0:
                page = '#page'
                return render(request, 'dashboard.html', locals())
            page = '#page'
            # return HttpResponse("/")


            ### return HttpResponseRedirect("/")

            ## return HttpResponseRedirect('.')

            return render(request, 'dashboard.html', locals())
        else:

            cards = Card.objects.filter(owner=user)
            print (cards)
            if cards.count() > 0:
                page = '#page'
                return render(request, 'dashboard.html', locals())
            page = '#page'
            return render(request, 'dashboard.html', locals())




        print (' DEHORS ')
        return render(request, 'dashboard.html', locals())
            # return render(request, 'dashboard.html', {'formUser':formUser})

            ########## return redirect(request, 'dashboard.html', locals())
            ###return redirect('/dashboard.html')  # Redirect after POST

                # return HttpResponseRedirect('dashboard.html')  # Redirect after POST

    else:  # Si ce n'est pas du POST, c'est probablement une requête GET
        # Nous créons un formulaire pré-rempli
        #### formUser = UserForm(instance=user)
        formUser = UserForm(instance=user)
    # return render(request, 'office/profil.html', locals())
        return render(request, 'office/profil.html', {'formUser':formUser})