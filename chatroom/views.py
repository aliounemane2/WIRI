from django.shortcuts import render

from django.shortcuts import render
from django.http import Http404
from random import randint
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User, Interest
from rest_framework import status
from users.serializers import UserSerializer, InterestSerializer
from chatroom.serializers import *

from rest_framework.serializers import *
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
import json
from django.db.models import Q
from fcm.models import AbstractDevice
from fcm.utils import get_device_model
MyDevice = get_device_model()
from django.db.models import Sum, Count





class ChatGroupList(APIView):

    def get(self, request):
        chatgroup = ChatGroup.objects.all()
        serializer = ChatGroupSerializer(chatgroup, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = ChatGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


    def put(self, request, pk, format=None):
        chatgroup = self.get_object(pk)
        serializer = ChatGroupSerializer(chatgroup, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class MessageList(APIView):

    def get(self, request):
        message = Message.objects.all()
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)




class MediaList(APIView):

    def get(self, request):
        media = Media.objects.all()
        serializer = MediaSerializer(media, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



@api_view(['POST'])
def getGroupList(request):

    id_user = request.data['id']

    try:
        # chatgroup = ChatGroup.objects.filter(userss=id_user) | ChatGroup.objects.filter(users=id_user)
        # ####### chatgroup = ChatGroup.objects.filter(Q(userss=id_user) | Q(users=id_user)).distinct()
        chatgroup = ChatGroup.objects.filter(Q(userss=id_user) | Q(users=id_user)).distinct()
        if len(chatgroup) > 0:
            serializer = ChatGroupSerializer(chatgroup, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(data={
                'status': 1,
                'message': 'Cet utilisateur ne figure dans aucun groupe de discussion.'
            })
    except:
        return Response(data={
            'status': 1,
            'message': 'Cet utilisateur ne figure pas dans la base de données.'
        })



@api_view(['PUT'])
def addUserGroup(request):

    id_group = request.data['id_group']
    list_users = request.data['users']
    print(list_users)

    try:
        chatgroup = ChatGroup.objects.get(id=id_group)

        i = 0
        print(' debut boucle 1 ')
        while i < (len(list_users)):
            print (list_users[i])
            chatgroup.users.add(list_users[i])
            i += 1
        print(' fin boucle 1 ')

        chatgroup.save()

        groupechat = ChatGroup.objects.filter(id=id_group).values('userss__first_name',
                                                                  'userss__last_name',
                                                                  'content',
                                                                  'userss'
                                                                  )
        print(groupechat)

        j=0

        print (' Début milieu ')

        device3 = MyDevice.objects.filter(user_id=list_users[j]).values('reg_id')
        print(device3)

        print(' Fin milieu ')

        print(' debut boucle 2 ')

        while j < (len(list_users)):
            # device = MyDevice.objects.get(user_id=list_users[i])

            device = MyDevice.objects.filter(user_id=list_users[j]).values('reg_id')
            print('Valeur de device')
            print(device)




            if len(device) == 0:
                print(' vide ')
                print(' vide ')
                print(' vide ')
                print(' vide ')

                device111 = MyDevice.objects.filter(user_id=groupechat[0]['userss']).values('reg_id')
                device_last111 = MyDevice.objects.get(reg_id=device111[0]['reg_id'])
                print(device_last111)
                print(' Envoie ')
                print(' Personne ')

                user1 = User.objects.filter(id=list_users[j]).values('first_name', 'last_name')
                print(user1)
                print(' Envoie ')
                print(' Personne ')
                print(str(user1[0]['first_name']))
                print(str(user1[0]['last_name']))




                # device_last.send_message({'message': 'my test message'}, collapse_key='something')

                # device_last.send_message(data={"title":"Nouveau Invitation",
                #                                "sender":str(user1[0]['first_name'])+" "+str(user1[0]['last_name']),
                #                                "type":0,
                #                                "latitude": latitude,
                #                                "longitude": longitude
                #                                })
                # }

                print('Notification non envoyé du fcm')
                device_last111.send_message(data={"title": "Echec Ajout Groupe",
                                                  "receivers": str(user1[0]['first_name']) + " " + str(
                                                      user1[0]['last_name']),
                                                  "type": 12,
                                                  "message": "est dans le groupe mais recevra les notifications plutard."
                                                  })


            else:

                device1 = device[0]['reg_id']
                print(device1)
                print(' Dans la boucle 2')

                device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
                print(device_last)

                # device_last.send_message({
                #     body: 'Vous etes ajouté au groupe'+str(groupechat[0]['content'])+
                #                ' par '+str(groupechat[0]['userss__first_name'])+' '
                #                                  + str(groupechat[0]['userss__last_name'])})

                # device_last.send_message(title="Nouveau Groupe", body=str(groupechat[0]["userss__first_name"])+" "
                #                                                       + str(groupechat[0]["userss__last_name"])+" vous a ajouté dans le groupe "+str(groupechat[0]["content"]))

                # device_last.send_message("Nouveau Groupe", str(groupechat[0]["userss__first_name"])+" "+ str(groupechat[0]["userss__last_name"])+" vous a ajouté dans le groupe "+str(groupechat[0]["content"]))
                # device_last.send_message(data={"title": "test", "message": "dasfsaf"})

                device_last.send_message(data={"sender": str(groupechat[0]["userss__first_name"])+" "+ str(groupechat[0]["userss__last_name"]),
                                               "title":"Nouveau groupe.",
                                               "type":3,
                                               "name_groupe":str(groupechat[0]["content"])})






                ### device_last.send_message(notification={"body": "test", "title": "dasfsaf"})

                ##### device_last.send_message(title= "test", message= "dasfsaf")
                ### device_last.send_message("test", "dasfsaf")
                print(device_last)

                #
                # print(device_last)

                #### device.send_message({'message': 'Vous etes ajouté au groupe'})

                # a = MyDevice.objects.all().send_message({'message': 'Vous etes ajouté au groupe'})
                # print (a)

                #### device_last.send_message({'message': 'Vous etes ajouté au groupe'})

                j += 1
            print (' fin boucle 2 ')

            # device = MyDevice.objects.get(reg_id=token)
            # device.send_message({'message': 'salut '})




            return Response(data={
                'status':0,
                'message': 'Ajout de l\'utilisateur dans le groupe effectif.'
            })
    except:
        return Response(data={
            'status': 1,
            'message': 'Echec de l\'ajout de l\'utilisateur dans le groupe.'
        })




@api_view(['POST'])
def addGroup(request):
    serializer = ChatGroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # res = {"status": 0, "message": "Création du groupe fait avec success", "users": serializer.data}
        #return Response(data=json.dumps(res), status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        # return Response(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
def addGroup2(request):

    if request.method == "POST":

        try:
            content = request.data['content']
            idContact = request.data['id_user']
            listeContact = request.data['users']

            print (listeContact)
            chatgroup = ChatGroup()


            # Si l'utilisateur n'a pas de device Token
            device_sender = MyDevice.objects.filter(user_id=idContact).values('reg_id')
            print('Valeur de device sender')
            print(len(device_sender))
            print(device_sender)

            print(' debut sender ')

            if len(device_sender) == 0:
                print(' dans sender ')

                return Response(data={
                    'status': -1,
                    'message': 'Nous rencontrons un problème reconnectez vous SVP.'
                })

                # Fin du sender




            id_user = User.objects.get(id=idContact)
            chatgroup.userss = id_user
            print (id_user)
            print (chatgroup.userss)

            chatgroup.content=content

            i = 0
            print(' debut boucle ')

            while i < (len(listeContact)):
                print (listeContact[i])
                chatgroup.save()
                chatgroup.users.add(listeContact[i])
                # favouriteContacts.users.add(listeContact[i])
                i += 1
                print (' fin boucle ')


            # favouriteContacts.save()
            chatgroup.users.add(idContact)


            # Debut de Creation

            groupechat = User.objects.filter(id=idContact).values('first_name', 'last_name')
            print(groupechat)

            j = 0
            print (' Début milieu ')

            device3 = MyDevice.objects.filter(user_id=listeContact[j]).values('reg_id')
            print(device3)

            print(' Fin milieu ')

            print(' debut boucle 2 ')

            while j < (len(listeContact)):
                # device = MyDevice.objects.get(user_id=list_users[i])

                print(' debut ')

                device897 = MyDevice.objects.filter(user_id=listeContact[j]).values('reg_id', 'is_active')
                print('Valeur de device')
                print(device897)
                print(' voila ')
                print(len(device897))
                # is_active=True,
                print(' valeur de is active')
                # print(device[z]['is_active'])


                if len(device897) == 0:
                    print(' vide ')
                    print(' vide ')
                    print(' vide ')
                    print(' vide ')

                    device111 = MyDevice.objects.filter(user_id=idContact).values('reg_id', 'is_active')

                    device_last111 = MyDevice.objects.get(reg_id=device111[0]['reg_id'])
                    print(device_last111)
                    user1 = User.objects.filter(id=listeContact[j]).values('first_name', 'last_name')
                    print(user1)
                    print(' Envoie ')
                    print(' Personne ')
                    print(str(user1[0]['first_name']))
                    print(str(user1[0]['last_name']))
                    # device_last.send_message({'message': 'my test message'}, collapse_key='something')

                    # device_last.send_message(data={"title":"Nouveau Invitation",
                    #                                "sender":str(user1[0]['first_name'])+" "+str(user1[0]['last_name']),
                    #                                "type":0,
                    #                                "latitude": latitude,
                    #                                "longitude": longitude
                    #                                })

                    # }

                    print('Notification non envoyé du fcm')
                    device_last111.send_message(data={"title": "Echec de l'envoi",
                                                      "receivers": str(user1[0]['first_name']) + " " + str(
                                                          user1[0]['last_name']),
                                                      "type": 12,
                                                      "message": "n'a pas reçu la notification de l'ajout de groupe",
                                                      "name_groupe": str(content)

                                                      })

                    # z+=1
                    print(' Fin ')
                    j += 1

                else:

                    device = MyDevice.objects.filter(user_id=listeContact[j]).values('reg_id')
                    print('Valeur de device')
                    print(device)

                    device1 = device[0]['reg_id']
                    print(device1)
                    print(' Dans la boucle 2')

                    device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
                    print(device_last)

                    device_last.send_message(data={
                        "sender": str(groupechat[0]["first_name"]) + " " + str(groupechat[0]["last_name"]),
                        "title": "Nouveau groupe",
                        "type": 3,
                        "name_groupe": str(content)
                    })

                    j += 1

                #j += 1


                # Fin de creation

            return Response(
                data={
                    'status': 0,
                    'message': 'Création du groupe effective.'
                    # 'favourite': favouriteContacts.userss
                })

        except:
            return Response(data={'status': 1, 'message': 'Echec de la création du groupe.'})




@api_view(['POST'])
def addPhotos(request):

    if request.method == "POST":

        photo = request.data['photo']
        chatgroup = request.data['chatgroup']
        sender = request.data['sender']



        # Si l'utilisateur n'a pas de device Token
        device_sender = MyDevice.objects.filter(user_id=sender).values('reg_id')
        print('Valeur de device sender')
        print(len(device_sender))
        print(device_sender)

        print(' debut sender ')

        if len(device_sender) == 0:
            print(' dans sender ')

            return Response(data={
                'status': -1,
                'message': 'Nous rencontrons un problème reconnectez vous SVP.'
            })

            # Fin du sender


        chatgroups = ChatGroup.objects.filter(id=chatgroup).values('userss',
                                                                   'userss__first_name',
                                                                   'userss__last_name',
                                                                   'userss__photo',
                                                                   'users',
                                                                   'content'
                                                                   )
        print (chatgroups)

        i = 0
        print(' debut boucle ')

        message = Message()

        message.photo = photo

        chatgroup1 = ChatGroup.objects.get(id=chatgroup)
        message.chatgroup = chatgroup1

        userssssss = User.objects.get(id=sender)
        message.users = userssssss

        while i < (len(chatgroups)):
            print (chatgroups[i]['users'])

            message.save()
            # userssssss2 = User.objects.get(id=chatgroups[i]['users'])
            message.users_receivers.add(chatgroups[i]['users'])


            i += 1
            print (' fin boucle ')

        last_requete = Message.objects.latest('id')
        print (' LAST REQUETTE ')
        last_reque = last_requete.pk
        print (last_reque)

        mess = Message.objects.filter(id=last_reque).values('photo')
        print (mess)
        print (mess[0]['photo'])


        j = 0
        print (' Début milieu ')

        device3 = MyDevice.objects.filter(user_id=chatgroups[j]['users']).values('reg_id')
        print(device3)

        print(' Fin milieu ')

        print(' debut boucle 2 ')

        usersssssss = User.objects.filter(id=sender).values('first_name', 'last_name')


        while j < (len(chatgroups)):
            # device = MyDevice.objects.get(user_id=list_users[i])

            print (' BIENVENU ')
            print (' BIENVENU ')
            print (' BIENVENU ')
            print (' BIENVENU ')

            print (' Valeur chatgroups[j][users] ')
            print (chatgroups[j]['users'])

            print (' sender ')
            print (sender)



            if str(chatgroups[j]['users']) != str(sender):


                print (' Valeur de J')
                print (j)

                print (' FIN OK 1 ')
                print (' FIN OK  1')
                print (' FIN OK 1 ')

                device = MyDevice.objects.filter(user_id=chatgroups[j]['users']).values('reg_id')
                print('Valeur de device')
                print(device)

                print('debut')

                if len(device) == 0:
                    print(' vide ')
                    print(' vide ')
                    print(' vide ')
                    print(' vide ')

                    device111 = MyDevice.objects.filter(user_id=sender).values('reg_id')
                    device_last111 = MyDevice.objects.get(reg_id=device111[0]['reg_id'])
                    print(device_last111)
                    user1 = User.objects.filter(id=chatgroups[j]['users']).values('first_name', 'last_name')
                    print(user1)
                    print(' Envoie ')
                    print(' Personne ')
                    print(str(user1[0]['first_name']))
                    print(str(user1[0]['last_name']))
                    # device_last.send_message({'message': 'my test message'}, collapse_key='something')

                    # device_last.send_message(data={"title":"Nouveau Invitation",
                    #                                "sender":str(user1[0]['first_name'])+" "+str(user1[0]['last_name']),
                    #                                "type":0,
                    #                                "latitude": latitude,
                    #                                "longitude": longitude
                    #                                })

                    # }

                    print('Notification non envoyé du fcm')
                    device_last111.send_message(data={"title": "Echec de l'envoi",
                                                      "receivers": str(user1[0]['first_name']) + " " + str(
                                                          user1[0]['last_name']),
                                                      "type": 12,
                                                      "message": "n'a pas reçu la photo envoyée.",
                                                      "file": str('/media/') + str(mess[0]['photo']),

                                                      })


                    j += 1

                else:

                    print('fin')
                    device = MyDevice.objects.filter(user_id=chatgroups[j]['users']).values('reg_id')
                    print('Valeur de device')
                    print(device)




                    device1 = device[0]['reg_id']
                    print(device1)
                    print(' Dans la boucle 2')

                    device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
                    print(device_last)
                    print (' FIN OK 2 ')
                    print (' FIN OK  2')
                    print (' FIN OK 2 ')




                    device_last.send_message(data={
                        "title": "Envoi de photo",
                        "type": 6,
                        "chatgroup": str(chatgroups[j]['content']),
                        "message": str('/media/')+str(mess[0]['photo']),
                        "sender": str(usersssssss[0]['first_name']) + " " + str(usersssssss[0]['last_name']),
                        "sender_id": sender,
                        "chatgroup_id": chatgroup,
                        "date_message": str(datetime.now())
                    })
                    j += 1

            else:
                j += 1
                print (' ELSE ')
                print (' ELSE ')
                print (' ELSE ')
                print (' ELSE ')
                print (' ELSE ')




        return Response(data={'status': 0, 'message': 'Envoi de la photo effective.'})








@api_view(['POST'])
def addPhotos2(request):

    if request.method == "POST":

        photo = request.data['photo']
        chatgroup = request.data['chatgroup']
        sender = request.data['sender']


        chatgroups  = ChatGroup.objects.filter(id=chatgroup).values('userss',
                                                                    'userss__first_name',
                                                                    'userss__last_name',
                                                                    'userss__photo',
                                                                    'users',
                                                                    'content'
                                                                    )
        print (chatgroups)

        i = 0
        print(' debut boucle ')

        message = Message()
        message.photo = photo

        print (photo)

        chatgroup1 = ChatGroup.objects.get(id=chatgroup)
        message.chatgroup = chatgroup1
        print (chatgroup1)

        userssssss = User.objects.get(id=sender)
        message.users = userssssss
        print (userssssss)

        while i < (len(chatgroups)):
            print (chatgroups[i]['users'])

            message.save()
            # userssssss2 = User.objects.get(id=chatgroups[i]['users'])
            message.users_receivers.add(chatgroups[i]['users'])

            i += 1
            print (' fin boucle ')





        j = 0
        print (' Début milieu ')

        device3 = MyDevice.objects.filter(user_id=chatgroups[j]['users']).values('reg_id')
        print(device3)

        print(' Fin milieu ')



        print(' debut boucle 2 ')

        while j < (len(chatgroups)):
            # device = MyDevice.objects.get(user_id=list_users[i])

            device = MyDevice.objects.filter(user_id=chatgroups[j]['users']).values('reg_id')
            print('Valeur de device')
            print(device)

            device1 = device[0]['reg_id']
            print(device1)
            print(' Dans la boucle 2')

            device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
            print(device_last)

            device_last.send_message(data={
                "title": "Envoi de photo",
                "type": 5,
                "chatgroup": str(chatgroups[j]['content']),
                "photo": str('/media/chatroom/')+str(photo),
                "sender_id":sender
            })

            j += 1



        return Response(data={'status': 0, 'message': 'Envoi de la photo effective.'})







@api_view(['POST'])
def sendMessage(request):
    if request.method == "POST":

        sms = request.data['message']
        chatgroup = request.data['chatgroup']
        sender = request.data['sender']




        # Si l'utilisateur n'a pas de device Token
        device_sender = MyDevice.objects.filter(user_id=sender).values('reg_id')
        print('Valeur de device sender')
        print(len(device_sender))
        print(device_sender)

        print(' debut sender ')

        if len(device_sender) == 0:
            print(' dans sender ')

            return Response(data={
                'status': -1,
                'message': 'Nous rencontrons un problème reconnectez vous SVP.'
            })

            # Fin du sender




        chatgroups = ChatGroup.objects.filter(id=chatgroup).values('userss',
                                                                   'userss__first_name',
                                                                   'userss__last_name',
                                                                   'userss__photo',
                                                                   'users',
                                                                   'content'
                                                                   )
        print (chatgroups)

        i = 0
        print(' debut boucle ')

        message = Message()

        message.content = sms

        chatgroup1 = ChatGroup.objects.get(id=chatgroup)
        message.chatgroup = chatgroup1

        userssssss = User.objects.get(id=sender)
        message.users = userssssss

        while i < (len(chatgroups)):
            print (chatgroups[i]['users'])

            message.save()
            # userssssss2 = User.objects.get(id=chatgroups[i]['users'])
            message.users_receivers.add(chatgroups[i]['users'])


            i += 1
            print (' fin boucle ')


        j = 0
        print (' Début milieu ')

        device3 = MyDevice.objects.filter(user_id=chatgroups[j]['users']).values('reg_id')
        print(device3)

        print(' Fin milieu ')

        print(' debut boucle 2 ')

        usersssssss = User.objects.filter(id=sender).values('first_name', 'last_name')



        dd = datetime.now()
        print (dd)
        # print (mess3[0]['date_created'])
        print (' COOL ')

        while j < (len(chatgroups)):
            # device = MyDevice.objects.get(user_id=list_users[i])

            print (' BIENVENU ')
            print (' BIENVENU ')
            print (' BIENVENU ')
            print (' BIENVENU ')

            if chatgroups[j]['users'] != sender:
                print (' Valeur de J')
                print (j)

                print (' FIN OK 1 ')
                print (' FIN OK  1')
                print (' FIN OK 1 ')

                device = MyDevice.objects.filter(user_id=chatgroups[j]['users']).values('reg_id')
                print('Valeur de device')
                print(device)

                print('debut')

                if len(device) == 0:
                    print(' vide ')
                    print(' vide ')
                    print(' vide ')
                    print(' vide ')

                    device111 = MyDevice.objects.filter(user_id=sender).values('reg_id')
                    device_last111 = MyDevice.objects.get(reg_id=device111[0]['reg_id'])
                    print(device_last111)
                    user1 = User.objects.filter(id=chatgroups[j]['users']).values('first_name', 'last_name')
                    print(user1)
                    print(' Envoie ')
                    print(' Personne ')
                    print(str(user1[0]['first_name']))
                    print(str(user1[0]['last_name']))
                    # device_last.send_message({'message': 'my test message'}, collapse_key='something')

                    # device_last.send_message(data={"title":"Nouveau Invitation",
                    #                                "sender":str(user1[0]['first_name'])+" "+str(user1[0]['last_name']),
                    #                                "type":0,
                    #                                "latitude": latitude,
                    #                                "longitude": longitude
                    #                                })

                    # }

                    print('Notification non envoyé du fcm')
                    device_last111.send_message(data={"title": "Echec de l'envoi",
                                                      "receivers": str(user1[0]['first_name']) + " " + str(
                                                          user1[0]['last_name']),
                                                      "type": 12,
                                                      "message": "n'a pas reçu le message envoyée",
                                                      "file": str(sms),

                                                      })

                    j += 1

                else:

                    device1 = device[0]['reg_id']
                    print(device1)
                    print(' Dans la boucle 2')

                    device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
                    print(device_last)
                    print (' FIN OK 2 ')
                    print (' FIN OK  2')
                    print (' FIN OK 2 ')

                    device_last.send_message(data={
                        "title": "Envoi de message",
                        "type": 6,
                        "chatgroup": str(chatgroups[j]['content']),
                        "message": str(sms),
                        "id_groupe":chatgroup,
                        "sender": str(usersssssss[0]['first_name'])+ " "+ str(usersssssss[0]['last_name']),
                        "sender_id":sender,
                        "date_message":str(datetime.now())

                    })
                    j += 1

            else:
                j += 1
                print (' ELSE ')
                print (' ELSE ')
                print (' ELSE ')
                print (' ELSE ')
                print (' ELSE ')




        return Response(data={'status': 0, 'message': 'Envoi du message effectif.'})





@api_view(['POST'])
def getAllMessages(request):

    if request.method == "POST":

        chatgroup = request.data['chatgroup']
        message = Message.objects.filter(chatgroup=chatgroup)
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





@api_view(['DELETE'])
def delete_groups(request):

    if request.method == "DELETE":

        id_chatgroup = request.data['chatgroup']
        id_user = request.data['user']


        try:
            chatgroup = ChatGroup.objects.filter(id=id_chatgroup).values('userss', 'content', 'users')
            print(chatgroup)
            if len(chatgroup) == 0:
                return Response(data={
                    'status': -2,
                    'message': 'Le groupe de discussion n\'existe pas.'
                })

            usersssss = User.objects.filter(id=id_user).values('first_name', 'last_name')




            # Le cas du device Token
            device_sender = MyDevice.objects.filter(user_id=id_user).values('reg_id')
            print('Valeur de device sender')
            print(len(device_sender))
            print(device_sender)

            print(' debut sender ')

            if len(device_sender) == 0:
                print(' dans sender ')

                return Response(data={
                    'status': -1,
                    'message': 'Nous rencontrons un problème reconnectez vous SVP.'
                })
            # Si celui qui envoie n'a pas de device Token  le message est envoyé


            if chatgroup[0]['userss'] == id_user:

                j = 0
                while j < (len(chatgroup)):

                    print(' BIENVENU ')
                    print(' BIENVENU ')
                    print(' BIENVENU ')
                    print(' BIENVENU ')

                    if chatgroup[j]['users'] != id_user:
                        print(' Valeur de J')
                        print(j)

                        print(' FIN OK 1 ')
                        print(' FIN OK  1')
                        print(' FIN OK 1 ')

                        device = MyDevice.objects.filter(user_id=chatgroup[j]['users']).values('reg_id')
                        print('Valeur de device')
                        print(device)

                        print('debut')

                        if len(device) == 0:
                            print(' vide ')
                            print(' vide ')
                            print(' vide ')
                            print(' vide ')

                            device111 = MyDevice.objects.filter(user_id=id_user).values('reg_id')
                            device_last111 = MyDevice.objects.get(reg_id=device111[0]['reg_id'])
                            print(device_last111)
                            user1 = User.objects.filter(id=chatgroup[j]['users']).values('first_name', 'last_name')
                            print(user1)
                            print(' Envoie ')
                            print(' Personne ')
                            print(str(user1[0]['first_name']))
                            print(str(user1[0]['last_name']))
                            print('Notification non envoyé du fcm')
                            j += 1

                        else:

                            device1 = device[0]['reg_id']
                            print(device1)
                            print(' Dans la boucle 2')

                            device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
                            print(device_last)
                            print(' FIN OK 2 ')
                            print(' FIN OK  2')
                            print(' FIN OK 2 ')

                            print(' Nom du groupe')
                            print(chatgroup[0]['content'])

                            device_last.send_message(data={
                                "title": "Suppression du groupe",
                                "type": 12,
                                "message": str(usersssss[0]['first_name']) + " " + str(usersssss[0]['last_name'])+ " a supprimé le groupe "+str(chatgroup[0]['content']),

                            })
                            j += 1

                    else:
                        j += 1
                        print(' ELSE ')
                        print(' ELSE ')
                        print(' ELSE ')
                        print(' ELSE ')
                        print(' ELSE ')


                chatgroupss = ChatGroup.objects.get(id=id_chatgroup)
                chatgroupss.delete()
                return Response(data={'status': 1, 'message': 'Suppression du groupe effectif.'})
            else:

                chatgroupr = ChatGroup.objects.get(id=id_chatgroup)
                chatgroupr.users.remove(id_user)
                users = User.objects.filter(id=id_user).values('first_name', 'last_name')
                return Response(data={'status': 1, 'message': str(users[0]['first_name'])+ ' '+str(users[0]['last_name']) + ' s\'est retiré du groupe.'})

        except:
            return Response(data={'status': 2, 'message': 'Echec l\'utilisateur ou le groupe n\'existe pas.'})


@api_view(['POST'])
def get_members_groups(request):

    if request.method == "POST":
        id_chatgroup = request.data['chatgroup']

        chatgroup = ChatGroup.objects.filter(id=id_chatgroup)
        serializer = ChatGroupSerializer(chatgroup, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
