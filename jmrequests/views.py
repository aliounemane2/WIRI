from django.shortcuts import render

from django.shortcuts import render

from django.shortcuts import render
from django.http import Http404
from random import randint
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User, Interest
from jmspots.models import *
from rest_framework import status
from users.serializers import UserSerializer, InterestSerializer
from jmrequests.models import *
from jmrequests.serializers import *
from jmspots.serializers import *

from rest_framework.serializers import *
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
from datetime import datetime
from django.db import transaction
import json
# from fcm import FCMDevice
# from fcm.models import get_device_model

from fcm.utils import get_device_model
MyDevice = get_device_model()
from django.db.models import Sum, Count
from django.utils import timezone




class RequestList(APIView):

    def get(self, request):
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)
        # serializer = RequestSerializer(requests)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # def post(self, request):
    #     serializer = RequestSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors)




class Request_ReceiversList(APIView):

    def get(self, request):
        requestsReceivers = Request_Receivers.objects.all()
        serializer = Request_ReceiversSerializer(requestsReceivers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = Request_ReceiversSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



@api_view(['POST'])
@transaction.atomic
def jmrequest_join_me(request):

    if request.method == 'POST':

        #telephone = request.data['telephone']
        latitude=request.data['latitude']
        longitude=request.data['longitude']
        sender=request.data['sender']
        list_receivers= request.data['receivers']

        try:

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


            z=0
            while z < (len(list_receivers)):
                # device = MyDevice.objects.get(user_id=list_users[i])

                device = MyDevice.objects.filter(user_id=list_receivers[z]).values('reg_id', 'is_active')
                print('Valeur de device')
                print(device)
                print(' voila ')
                print(len(device))
                # is_active=True,
                print(' valeur de is active')
                #print(device[z]['is_active'])




                if len(device) == 0:

                    print(' vide ')
                    print(' vide ')
                    print(' vide ')
                    print(' vide ')

                    device111 = MyDevice.objects.filter(user_id=sender).values('reg_id', 'is_active')

                    device_last = MyDevice.objects.get(reg_id=device111[0]['reg_id'])
                    print(device_last)
                    user1 = User.objects.filter(id=list_receivers[z]).values('first_name', 'last_name')
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
                    device_last.send_message(data={"title": "Echec de l'envoi",
                                                   "receivers": str(user1[0]['first_name']) + " " + str(
                                                       user1[0]['last_name']),
                                                   "type": 12,
                                                   "message": "n'a pas reçu votre invitation"
                                                   })

                    # z+=1

                else:
                    print('Debut else ')

                    device = MyDevice.objects.filter(user_id=list_receivers[z]).values('reg_id', 'is_active')
                    print('Valeur de device')
                    print(device)
                    print(' voila ')
                    print(len(device))


                    if device[0]['is_active'] == False:
                        print('False *****')
                        # print(device[z]['is_active'])
                        # device[z].is_active=True
                        print('True')
                        # device.save()
                        # device[0]['is_active']
                        #device.update(is_active=True)
                        print('Enregistrement effectué')




                    spot = Spot()
                    requests = Request()
                    request_receivers = Request_Receivers()

                    spot.latitude = latitude
                    spot.longitude = longitude
                    spot.save()

                    requests.spot = spot
                    requests.date_sender = datetime.now()

                    requests.save()

                    last_requete = Request.objects.latest('id')
                    print(' LAST REQUETTE ')
                    last_reque = last_requete.pk
                    print(last_reque)

                    print(' ok 1')

                    print(' sender ')
                    sender1 = User.objects.get(id=sender)
                    request_receivers.sender = sender1
                    print(request_receivers.sender)
                    print(' ok 2')

                    print(list_receivers)
                    i = 0
                    print(' debut boucle ')
                    # with transaction.commit_on_success():


                    with transaction.atomic():

                        while z < (len(list_receivers)):
                            print(' ccccccccccccccccccc ')
                            print(list_receivers[z])
                            request_receivers.sender = sender1
                            print(' cc 1 ')
                            request_receivers.is_active = False
                            print(' cc 2 ')
                            # request_receivers.list_receivers.add(list_receivers[i])

                            u = User.objects.get(id=list_receivers[z])
                            request_receivers.list_receivers = u
                            print(request_receivers.list_receivers)
                            print(' cc 3 ')
                            # request_receivers.state= 'NULL'
                            # print (' cc 4 ')

                            req = Request.objects.get(id=last_reque)
                            Request.objects.latest('id')
                            print(' Requette ')
                            print(req)
                            request_receivers.receivers = req
                            print(' cc 4 ')
                            a = Request_Receivers(
                                sender=sender1,
                                list_receivers=u,
                                receivers=req,
                                is_active=False,
                            )
                            print(' cc 5 ')
                            a.save()
                            print(' cc 6 ')

                            last_requete1 = Request_Receivers.objects.latest('id')
                            print(' LAST REQUETTE ')
                            last_reque1 = last_requete1.pk
                            print(last_reque1)

                            # request_receivers.save()
                            print(' cc 7 ')
                            print(' cc 8 ')

                            device = MyDevice.objects.filter(user_id=list_receivers[z]).values('reg_id')
                            print('Valeur de device')
                            print(device)


                            if len(device) == 0:
                                print(' vide ')
                                print(' vide ')
                                print(' vide ')
                                print(' vide ')

                                device111 = MyDevice.objects.filter(user_id=sender).values('reg_id', 'is_active')

                                device_last = MyDevice.objects.get(reg_id=device111[0]['reg_id'])
                                print(device_last)
                                user1 = User.objects.filter(id=list_receivers[z]).values('first_name', 'last_name')
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
                                device_last.send_message(data={"title": "Echec de l'envoi",
                                                               "receivers": str(user1[0]['first_name']) + " " + str(
                                                                   user1[0]['last_name']),
                                                               "type": 12,
                                                               "message": "n'a pas reçu votre invitation"
                                                               })
                            else:







                                #device1 = device[0]['reg_id']
                                #print(device1)
                                print(' Dans la boucle 2')

                                device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
                                print(device_last)
                                user1 = User.objects.filter(id=sender).values('first_name', 'last_name')
                                print(user1)
                                print(' Envoie ')
                                # device_last.send_message({'message': 'my test message'}, collapse_key='something')

                                # device_last.send_message(data={"title":"Nouveau Invitation",
                                #                                "sender":str(user1[0]['first_name'])+" "+str(user1[0]['last_name']),
                                #                                "type":0,
                                #                                "latitude": latitude,
                                #                                "longitude": longitude
                                #                                })

                                # }
                                device_last.send_message(data={"title": "Nouvelle invitation",
                                                               "sender": str(user1[0]['first_name']) + " " + str(
                                                                   user1[0]['last_name']),
                                                               "type": 0,
                                                               "latitude": latitude,
                                                               "longitude": longitude,
                                                               "id_requette": last_reque1
                                                               })



                            z += 1
                        print(' fin boucle ')

                        # Ajout de code
                        # j = 0

                            # Fin ajout de code

                    print('Fin else ')
                z+=1

            return Response(data={
                'status': 0,
                'message': 'Enregistrement effectif.'})







        except :
            return Response(
                data={
                    'status':1,
                    'message':'Echec de l\'enregistrement.'})






@api_view(['POST'])
@transaction.atomic
def jmrequest_join_me_card(request):

    if request.method == 'POST':

        sender = request.data['sender']
        list_receiver = request.data['list_receiver']
        message = request.data['message']
        id_card = request.data['card']
        date_receivers = request.data['date_receivers']

        try:

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

            requests = Request()
            ##### La bonne ancien   cards = Card.objects.values('event__spot__id', 'institution__spot__id').get(id=id_card)
            cards = Card.objects.values('event__spot__id', 'institution__spot__id', 'file').get(id=id_card)
            print (cards)

            if cards['event__spot__id']== None:
                print(' Carte institutionnelles ')

                print (sender)
                print (list_receiver)
                print (message)
                print (id_card)
                print (date_receivers)

                print (cards['institution__spot__id'])
                spot = Spot.objects.get(id=cards['institution__spot__id'])

                print (' ****  SPOT **** ')
                print (spot)

                print (' ****  SPOT  ID **** ')
                print (spot.id)

                print(' OK 2')
                requests.spot = spot
                print(' OK  3 3')

                # requests.save()
                print (' PREMIER ETAPE  VALIDE ')

                cardss = Card.objects.get(id=id_card)
                print(' OK 5')
                print (' CARTE ')
                print (cardss)


                requests.card = cardss
                print(' OK  6')

                requests.with_card = True
                print(' OK 7')
                requests.date_sender = datetime.now()
                print(' OK 8')
                requests.date_receivers=date_receivers
                # requests.date_receivers = datetime.now()
                print(' OK 9')
                requests.message = message
                print(' OK 10 ')

                print (' FIN AVANT ENREGISTREMENT ')

                requests.save()
                print(' OK 11 ')

                last_requete = Request.objects.latest('id')
                print (' LAST REQUETTE ')
                last_reque = last_requete.pk
                print (last_reque)

                request_receivers = Request_Receivers()
                i = 0

                with transaction.atomic():
                    while i < (len(list_receiver)):
                        print (' ccccccccccccccccccc ')
                        print (list_receiver[i])

                        sender1 = User.objects.get(id=sender)
                        request_receivers.sender = sender1
                        print (' cc 1 ')

                        request_receivers.is_active = True
                        print (' cc 2 ')
                        # request_receivers.list_receivers.add(list_receivers[i])

                        req = Request.objects.get(id=last_reque)
                        Request.objects.latest('id')
                        print (' Requette ')
                        print (req)
                        request_receivers.receivers = req
                        print (' cc 4 ')

                        print (list_receiver)
                        print (list_receiver[i])

                        u = User.objects.get(id=list_receiver[i])
                        request_receivers.list_receivers = u

                        print (request_receivers.receivers)
                        print (' cc 3 ')

                        a = Request_Receivers(
                            sender=sender1,
                            list_receivers=u,
                            receivers=req,
                            is_active=True,
                        )

                        print(' cc 5 ')
                        a.save()
                        print(' cc 6 ')

                        #request_receivers.save()

                        last_requete1 = Request_Receivers.objects.latest('id')
                        print (' LAST REQUETTE ')
                        last_reque1 = last_requete1.pk
                        print (last_reque1)
                        print(' cc 7 ')
                        print('Debut filtre ')
                        print('Debut filtre ')
                        print('Debut filtre ')
                        print('Debut filtre ')

                        device = MyDevice.objects.filter(user_id=list_receiver[i]).values('reg_id', 'is_active')
                        print('Valeur de device')
                        print(device)

                        if len(device) == 0:
                            print(' vide ')
                            print(' vide ')
                            print(' vide ')
                            print(' vide ')

                            device111 = MyDevice.objects.filter(user_id=sender).values('reg_id', 'is_active')

                            device_last = MyDevice.objects.get(reg_id=device111[0]['reg_id'])
                            print(device_last)
                            user1 = User.objects.filter(id=list_receiver[i]).values('first_name', 'last_name')
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

                            device_last.send_message(data={"title": "Echec de l'envoi",
                                                           "receivers": str(user1[0]['first_name']) + " " + str(
                                                               user1[0]['last_name']),
                                                           "type": 12,
                                                           "message": "n'a pas reçu votre invitation"
                                                           })

                            cardsss = Card.objects.filter(id=id_card).values('institution__spot__latitude',
                                                                             'institution__spot__longitude', 'file',
                                                                             'institution__name')
                            # cardsss = Request.objects.filter(card__institution__spot__id=id_card).values('event__spot__latitude', 'event__spot__longitude', 'institution__spot__latitude', 'institution__spot__longitude')
                            # device_last.send_message({'message': 'my test message'}, collapse_key='something')
                            print(cardsss)

                            # device_last.send_message(data={"title": "Nouvelle Invitation",
                            #                           "sender": str(user1[0]['first_name'])+" " +str(user1[0]['last_name']),
                            #                           "file":str('/media/')+str(cardsss['file']),
                            #                           "latitude":str(cardsss[0]['institution__spot__latitude']),
                            #                           "longitude": str(cardsss[0]['institution__spot__longitude'])
                            #                           })

                            device_last.send_message(data={"title": "Echec de l'envoi",
                                                           "receivers": str(user1[0]['first_name']) + " " + str(
                                                               user1[0]['last_name']),
                                                           "file": str('/media/') + str(cardsss[0]['file']),
                                                           "type": 12,
                                                           "name": str(cardsss[0]['institution__name']),
                                                           "message": "n'a pas reçu votre invitation à "+str(cardsss[0]['institution__name']),
                                                           "date_receivers": date_receivers
                                                           })

                            print('Notification non envoyé du fcm')
                            i += 1

                        else:



                            device1 = device[0]['reg_id']
                            print(device1)
                            print(' Dans la boucle 2')

                            device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
                            print(device_last)
                            user1 = User.objects.filter(id=sender).values('first_name', 'last_name')
                            print(user1)
                            print(' Envoie ')
                            cardsss = Card.objects.filter(id=id_card).values('institution__spot__latitude',
                                                                             'institution__spot__longitude', 'file',
                                                                             'institution__name')
                            # cardsss = Request.objects.filter(card__institution__spot__id=id_card).values('event__spot__latitude', 'event__spot__longitude', 'institution__spot__latitude', 'institution__spot__longitude')
                            # device_last.send_message({'message': 'my test message'}, collapse_key='something')
                            print(cardsss)

                            # device_last.send_message(data={"title": "Nouvelle Invitation",
                            #                           "sender": str(user1[0]['first_name'])+" " +str(user1[0]['last_name']),
                            #                           "file":str('/media/')+str(cardsss['file']),
                            #                           "latitude":str(cardsss[0]['institution__spot__latitude']),
                            #                           "longitude": str(cardsss[0]['institution__spot__longitude'])
                            #                           })

                            device_last.send_message(data={"title": "Nouvelle invitation",
                                                           "sender": str(user1[0]['first_name']) + " " + str(
                                                               user1[0]['last_name']),
                                                           "file": str('/media/') + str(cardsss[0]['file']),
                                                           "latitude": cardsss[0]['institution__spot__latitude'],
                                                           "longitude": cardsss[0]['institution__spot__longitude'],
                                                           "id_requete": last_reque1,
                                                           "type": 1,
                                                           "name": str(cardsss[0]['institution__name']),
                                                           "message": message,
                                                           "date_receivers": date_receivers
                                                           })
                            i += 1
                #
                #             print('Fin filtre ')
                #             print('Fin filtre ')
                #             print('Fin filtre ')
                #             print('Fin filtre ')
                #
                #         #i += 1
                #     print (' fin boucle ')
                # # Ajout de code
                #
                #
                # j = 0
                # while j < (len(list_receiver)):
                #     # device = MyDevice.objects.get(user_id=list_users[i])
                #
                #     device = MyDevice.objects.filter(user_id=list_receiver[j]).values('reg_id')
                #     print('Valeur de device')
                #     print(device)
                #
                #     device1 = device[0]['reg_id']
                #     print(device1)
                #     print(' Dans la boucle 2')
                #
                #     device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
                #     print(device_last)
                #     user1 = User.objects.filter(id=sender).values('first_name', 'last_name')
                #     print(user1)
                #     print(' Envoie ')
                #     cardsss = Card.objects.filter(id=id_card).values('institution__spot__latitude', 'institution__spot__longitude', 'file', 'institution__name')
                #     # cardsss = Request.objects.filter(card__institution__spot__id=id_card).values('event__spot__latitude', 'event__spot__longitude', 'institution__spot__latitude', 'institution__spot__longitude')
                #     # device_last.send_message({'message': 'my test message'}, collapse_key='something')
                #     print (cardsss)
                #
                #     # device_last.send_message(data={"title": "Nouvelle Invitation",
                #     #                           "sender": str(user1[0]['first_name'])+" " +str(user1[0]['last_name']),
                #     #                           "file":str('/media/')+str(cardsss['file']),
                #     #                           "latitude":str(cardsss[0]['institution__spot__latitude']),
                #     #                           "longitude": str(cardsss[0]['institution__spot__longitude'])
                #     #                           })
                #
                #     device_last.send_message(data={"title": "Nouvelle invitation",
                #                                    "sender": str(user1[0]['first_name']) + " " + str(user1[0]['last_name']),
                #                                    "file": str('/media/') + str(cardsss[0]['file']),
                #                                    "latitude": cardsss[0]['institution__spot__latitude'],
                #                                    "longitude": cardsss[0]['institution__spot__longitude'],
                #                                    "id_requete": last_reque1,
                #                                    "type":1,
                #                                    "name": str(cardsss[0]['institution__name']),
                #                                    "message": message,
                #                                    "date_receivers":date_receivers
                #                                    })
                #
                        #i += 1
                    #i += 1

                 # Fin ajout de code

                return Response(data={
                    'status': 0,
                    'message': 'Enregistrement à cet endroit effectif.'

                }
                )


            else:
                print (' Carte evenementielles ')
                print (cards['event__spot__id'])
                spot = Spot.objects.get(id=cards['event__spot__id'])
                print (spot)
                print (spot.id)

                print(' OK 2')
                requests.spot=spot
                print(' OK  3 3')

                requests.save()

                cardss = Card.objects.get(id=id_card)
                print(' OK 5')

                requests.card=cardss
                print(' OK  6')

                requests.with_card=True
                print(' OK 7')
                requests.date_sender=datetime.now()
                print(' OK 8')
                requests.date_receivers=date_receivers
                # requests.date_receivers=datetime.now()
                print(' OK 9')
                requests.message=message
                print(' OK 10 ')

                requests.save()
                print(' OK 11 ')

                last_requete = Request.objects.latest('id')
                print (' LAST REQUETTE ')
                last_reque = last_requete.pk
                print (last_reque)

                request_receivers = Request_Receivers()
                i = 0

                with transaction.atomic():
                    while i < (len(list_receiver)):
                        print (' ccccccccccccccccccc ')
                        print (list_receiver[i])

                        sender1 = User.objects.get(id=sender)
                        request_receivers.sender = sender1
                        print (' cc 1 ')

                        request_receivers.is_active = True
                        print (' cc 2 ')
                        # request_receivers.list_receivers.add(list_receivers[i])

                        req = Request.objects.get(id=last_reque)
                        Request.objects.latest('id')
                        print (' Requette ')
                        print (req)
                        request_receivers.receivers = req
                        print (' cc 4 ')

                        print (list_receiver)
                        print (list_receiver[i])

                        u = User.objects.get(id=list_receiver[i])
                        request_receivers.list_receivers = u

                        print (request_receivers.receivers)
                        print (' cc 3 ')

                        a = Request_Receivers(
                            sender=sender1,
                            list_receivers = u,
                            receivers = req,
                            is_active= True,
                        )

                        print(' cc 5 ')
                        a.save()
                        print(' cc 6 ')

                        # request_receivers.save()
                        print(' cc 7 ')

                        last_requete2 = Request_Receivers.objects.latest('id')
                        print(' LAST REQUETTE ')
                        last_reque3 = last_requete2.pk
                        print(last_reque3)

                        i += 1
                    print (' fin boucle ')

                    j = 0
                    while j < (len(list_receiver)):
                        # device = MyDevice.objects.get(user_id=list_users[i])

                        device = MyDevice.objects.filter(user_id=list_receiver[j]).values('reg_id')
                        print('Valeur de device')
                        print(device)

                        device1 = device[0]['reg_id']
                        print(device1)
                        print(' Dans la boucle 2')

                        device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
                        print(device_last)
                        user1 = User.objects.filter(id=sender).values('first_name', 'last_name')
                        print(user1)
                        print(' Envoie ')

                        # device_last.send_message({'message': 'my test message'}, collapse_key='something')

                        # cardsss = Request.objects.filter(id=id_card).values('spot__latitude', 'spot__longitude')

                        # device_last.send_message({'message': 'my test message'}, collapse_key='something')

                        #
                        # device_last.send_message(data={"title": "Nouvelle Invitation",
                        #                                "body": str(user1[0]['first_name']) + " " + str(
                        #                                    user1[0]['last_name']),
                        #                                "file": str(cardsss['file']),
                        #                                "destination": {
                        #                                    "latitude": str(cardsss[0]['spot__latitude']),
                        #                                    "longitude": str(cardsss[0]['spot__longitude'])
                        #                                }})

                        cardsss = Card.objects.filter(id=id_card).values('event__spot__latitude', 'event__spot__longitude', 'file', 'event__name')
                        # cardsss = Request.objects.filter(card__institution__spot__id=id_card).values('event__spot__latitude', 'event__spot__longitude', 'institution__spot__latitude', 'institution__spot__longitude')
                        # device_last.send_message({'message': 'my test message'}, collapse_key='something')
                        print (cardsss)

                        # device_last.send_message(data={"title": "Nouvelle Invitation",
                        #                           "sender": str(user1[0]['first_name'])+" " +str(user1[0]['last_name']),
                        #                           "file":str('/media/')+str(cardsss['file']),
                        #                           "latitude":str(cardsss[0]['institution__spot__latitude']),
                        #                           "longitude": str(cardsss[0]['institution__spot__longitude'])
                        #                           })
                        device_last.send_message(data={"title": "Nouvelle invitation",
                                                       "sender": str(user1[0]['first_name']) + " " + str(user1[0]['last_name']),
                                                       "file": str('/media/') + str(cardsss[0]['file']),
                                                       "latitude": cardsss[0]['event__spot__latitude'],
                                                       "longitude": cardsss[0]['event__spot__longitude'],
                                                       "id_requete": last_reque3,
                                                       "type": 1,
                                                       "name": str(cardsss[0]['event__name']),
                                                       "message": message,
                                                       "date_receivers": date_receivers
                                                       })



                        j += 1




                return Response(data={
                    'status': 0,
                    'message': 'Enregistrement à cet endroit effectif.'
                }
                )

        except:
            return Response(
                data={
                    'status': 1,
                    'message': 'Echec de l\'enregistrement à cet endroit.'})





# @api_view(['POST'])
# def jmrequest_joiner(request):
#
#     if request.method == 'POST':
#
#         id = request.data['id']
#         try:
#
#             requests = Request_Receivers.objects.filter(sender=id, is_active=False).last()
#
#             return Response(
#                 data={
#                     'status': 0,
#                     'message': 'Récupération éffectué',
#                     'requests_receivers':{
#                         'id': requests.id,
#                         'is_active': requests.is_active,
#                         'state': requests.state,
#                         # 'sender': requests.sender
#                         # 'requette': requests.receivers,
#                         # 'card': requests.card,
#                         # 'list_receivers': requests.list_receivers
#                     }
#                 }
#             )
#         except:
#             return Response(
#                 data={
#                     'status': 1,
#                     'message': 'Aucune information à propos de ce requette'})



@api_view(['POST'])
def jmrequest_joiner(request):

    if request.method == 'POST':

        id = request.data['id']
        try:

            requests = Request_Receivers.objects.filter(sender=id, is_active=False).last()
            serializer = Request_ReceiversSerializer(requests)
            print (' cc 2')
            res = {'status': 0, 'requests': serializer.data}
            #return Response(data=json.dumps(res), status=status.HTTP_200_OK)
            # return Response({"success": 0}, serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response(
                data={
                    'status': 1,
                    'message': 'Aucune information à propos cette requête.'})








@api_view(['POST'])
def invitation(request):
    """

   Cette Fonction permet de renvoyer l'ensemble des requettes de l'utilisateur
    """

    if request.method == 'POST':


        senders = request.data['sender']
        requests = Request_Receivers.objects.filter(sender=senders)
        serializer = Request_ReceiversSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def acept_decliner(request):

    if request.method == 'POST':

        id = request.data['id']
        value = request.data['val']

        requests = Request_Receivers.objects.get(id=id)




        if value == 1:
            requests.state = 'RECEIVED'
            requests.save()


            requests123 = Request_Receivers.objects.filter(id=id).values('sender',
                                                                         'sender__first_name',
                                                                         'sender__last_name',
                                                                         'sender__photo',
                                                                         'list_receivers',
                                                                         'list_receivers__first_name',
                                                                         'list_receivers__last_name',
                                                                         'receivers',
                                                                         'receivers__card__file',
                                                                         'receivers__card__institution__name',
                                                                         'receivers__card__institution__id',
                                                                         )

            # if requests123[0]['receivers__card__institution__id']!= 0:
            if requests123[0]['receivers__card__institution__id'] is not None:

                print('CARTE INSTITUTIONNELS')
                print('CARTE INSTITUTIONNELS')
                print('CARTE INSTITUTIONNELS')
                print('CARTE INSTITUTIONNELS')
                print('CARTE INSTITUTIONNELS')


                usersssss = User.objects.get(id=requests123[0]['sender'])

                device23 = MyDevice.objects.filter(user_id=usersssss).values('reg_id')
                print(device23)

                device34 = MyDevice.objects.filter(user_id=usersssss).values('reg_id')
                print('Valeur de device')
                print(device34)

                device12 = device34[0]['reg_id']
                print(device12)
                print(' Dans la boucle 2')

                device_last = MyDevice.objects.get(reg_id=device34[0]['reg_id'])
                print(device_last)

                device_last.send_message(data={
                    "receivers": str(requests123[0]['list_receivers__first_name']) + " " + str(requests123[0]['list_receivers__last_name']),
                    "sender": str(requests123[0]['sender__first_name']) + " " + str(requests123[0]['sender__last_name']),
                    "title": "Acceptez-vous l’invitation ?",
                    "type": 7,
                    "message": "a accepté votre invitation.",
                    "name_card": str(requests123[0]['receivers__card__institution__name']),
                    "file": str('/media/') + str(requests123[0]['receivers__card__file']),
                })

            else:
                print('CARTE SIMPLE')
                print('CARTE SIMPLE')
                print('CARTE SIMPLE')
                print('CARTE SIMPLE')
                print('CARTE SIMPLE')
                print('CARTE SIMPLE')
                print('CARTE SIMPLE')


                usersssss = User.objects.get(id=requests123[0]['sender'])

                device23 = MyDevice.objects.filter(user_id=usersssss).values('reg_id')
                print(device23)

                device34 = MyDevice.objects.filter(user_id=usersssss).values('reg_id')
                print('Valeur de device')
                print(device34)

                device12 = device34[0]['reg_id']
                print(device12)
                print(' Dans la boucle 2')

                device_last = MyDevice.objects.get(reg_id=device34[0]['reg_id'])
                print(device_last)

                device_last.send_message(data={
                    "receivers": str(requests123[0]['list_receivers__first_name']) + " " + str(
                        requests123[0]['list_receivers__last_name']),
                    "sender": str(requests123[0]['sender__first_name']) + " " + str(requests123[0]['sender__last_name']),
                    "title": "Acceptez-vous l’invitation ?",
                    "type": 8,
                    "message": "a accepté votre invitation."
                })

            return Response(
                data={
                    'status': 0,
                    'message': 'Acceptation de l’invitation effective.'})

        elif value == 0:
            requests.state = 'DECLINED'
            requests.save()

            requests123 = Request_Receivers.objects.filter(id=id).values('sender',
                                                                         'sender__first_name',
                                                                         'sender__last_name',
                                                                         'sender__photo',
                                                                         'list_receivers',
                                                                         'list_receivers__first_name',
                                                                         'list_receivers__last_name',
                                                                         'receivers',
                                                                         'receivers__card__file',
                                                                         'receivers__card__institution__name',
                                                                         'receivers__card__institution__id',
                                                                         )

            if requests123[0]['receivers__card__institution__id'] is not None:


                usersssss = User.objects.get(id=requests123[0]['sender'])

                device23 = MyDevice.objects.filter(user_id=usersssss).values('reg_id')
                print(device23)

                device34 = MyDevice.objects.filter(user_id=usersssss).values('reg_id')
                print('Valeur de device')
                print(device34)

                device12 = device34[0]['reg_id']
                print(device12)
                print(' Dans la boucle 2')

                device_last = MyDevice.objects.get(reg_id=device34[0]['reg_id'])
                print(device_last)

                device_last.send_message(data={
                    "receivers": str(requests123[0]['list_receivers__first_name']) + " " + str(
                        requests123[0]['list_receivers__last_name']),
                    "sender": str(requests123[0]['sender__first_name']) + " " + str(requests123[0]['sender__last_name']),
                    "title": "Déclinez-vous invitation ?",
                    "type": 7,
                    "message": "a décliné votre invitation",
                    "name_card": str(requests123[0]['receivers__card__institution__name']),
                    "file": str('/media/') + str(requests123[0]['receivers__card__file']),
                })
            else:

                usersssss = User.objects.get(id=requests123[0]['sender'])

                device23 = MyDevice.objects.filter(user_id=usersssss).values('reg_id')
                print(device23)

                device34 = MyDevice.objects.filter(user_id=usersssss).values('reg_id')
                print('Valeur de device')
                print(device34)

                device12 = device34[0]['reg_id']
                print(device12)
                print(' Dans la boucle 2')

                device_last = MyDevice.objects.get(reg_id=device34[0]['reg_id'])
                print(device_last)

                device_last.send_message(data={
                    "receivers": str(requests123[0]['list_receivers__first_name']) + " " + str(
                        requests123[0]['list_receivers__last_name']),
                    "sender": str(requests123[0]['sender__first_name']) + " " + str(requests123[0]['sender__last_name']),
                    "title": "Déclinez-vous invitation ?",
                    "type": 8,
                    "message": "a décliné votre invitation"
                })

            return Response(
                data={
                    'status': 0,
                    'message': 'Déclinaison de l’invitation effective.'})

        else:
            return Response(
                data={
                    'status': 1,
                    'message': 'Echec de la modification de la requête.'})




@api_view(['POST'])
def change_is_active_request_receivers(request):

    if request.method == 'POST':

        id = request.data['id']

        requests = Request_Receivers.objects.get(id=id)

        requests.is_active = True
        requests.save()
        return Response(
            data={
                'status': 0,
                'message': 'Modification effective.'})

    else:
        return Response(
            data={
                'status': 1,
                'message': 'Echec de la modification.'})






@api_view(['POST'])
@transaction.atomic
def jmrequest_to_bejoined(request):

    if request.method == 'POST':

        #telephone = request.data['telephone']
        latitude=request.data['latitude']
        longitude=request.data['longitude']
        sender=request.data['sender']
        list_receivers= request.data['receivers']

        try:

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


            z=0
            while z < (len(list_receivers)):
                # device = MyDevice.objects.get(user_id=list_users[i])

                device = MyDevice.objects.filter(user_id=list_receivers[z]).values('reg_id', 'is_active')
                print('Valeur de device')
                print(device)
                print(' voila ')
                print(len(device))
                # is_active=True,
                print(' valeur de is active')
                #print(device[z]['is_active'])




                if len(device) == 0:

                    print(' vide ')
                    print(' vide ')
                    print(' vide ')
                    print(' vide ')

                    device111 = MyDevice.objects.filter(user_id=sender).values('reg_id', 'is_active')

                    device_last = MyDevice.objects.get(reg_id=device111[0]['reg_id'])
                    print(device_last)
                    user1 = User.objects.filter(id=list_receivers[z]).values('first_name', 'last_name')
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
                    device_last.send_message(data={"title": "Echec de l'envoi",
                                                   "receivers": str(user1[0]['first_name']) + " " + str(
                                                       user1[0]['last_name']),
                                                   "type": 12,
                                                   "message": "n'a pas reçu votre requête de le rejoindre"
                                                   })

                    # z+=1

                else:
                    print('Debut else ')

                    device = MyDevice.objects.filter(user_id=list_receivers[z]).values('reg_id', 'is_active')
                    print('Valeur de device')
                    print(device)
                    print(' voila ')
                    print(len(device))


                    if device[0]['is_active'] == False:
                        print('False *****')
                        # print(device[z]['is_active'])
                        # device[z].is_active=True
                        print('True')
                        # device.save()
                        # device[0]['is_active']
                        #device.update(is_active=True)
                        print('Enregistrement effectué')




                    spot = Spot()
                    requests = Request()
                    request_receivers = Request_Receivers()

                    spot.latitude = latitude
                    spot.longitude = longitude
                    spot.save()

                    requests.spot = spot
                    requests.date_sender = datetime.now()
                    requests.tobejoined = True

                    requests.save()

                    last_requete = Request.objects.latest('id')
                    print(' LAST REQUETTE ')
                    last_reque = last_requete.pk
                    print(last_reque)

                    print(' ok 1')

                    print(' sender ')
                    sender1 = User.objects.get(id=sender)
                    request_receivers.sender = sender1
                    print(request_receivers.sender)
                    print(' ok 2')

                    print(list_receivers)
                    i = 0
                    print(' debut boucle ')
                    # with transaction.commit_on_success():


                    with transaction.atomic():

                        while z < (len(list_receivers)):
                            print(' ccccccccccccccccccc ')
                            print(list_receivers[z])
                            request_receivers.sender = sender1
                            print(' cc 1 ')
                            request_receivers.is_active = False
                            print(' cc 2 ')
                            # request_receivers.list_receivers.add(list_receivers[i])

                            u = User.objects.get(id=list_receivers[z])
                            request_receivers.list_receivers = u
                            print(request_receivers.list_receivers)
                            print(' cc 3 ')
                            # request_receivers.state= 'NULL'
                            # print (' cc 4 ')

                            req = Request.objects.get(id=last_reque)
                            Request.objects.latest('id')
                            print(' Requette ')
                            print(req)
                            request_receivers.receivers = req
                            print(' cc 4 ')
                            a = Request_Receivers(
                                sender=sender1,
                                list_receivers=u,
                                receivers=req,
                                is_active=False,
                            )
                            print(' cc 5 ')
                            a.save()
                            print(' cc 6 ')

                            last_requete1 = Request_Receivers.objects.latest('id')
                            print(' LAST REQUETTE ')
                            last_reque1 = last_requete1.pk
                            print(last_reque1)

                            # request_receivers.save()
                            print(' cc 7 ')
                            print(' cc 8 ')

                            device = MyDevice.objects.filter(user_id=list_receivers[z]).values('reg_id')
                            print('Valeur de device')
                            print(device)


                            if len(device) == 0:
                                print(' vide ')
                                print(' vide ')
                                print(' vide ')
                                print(' vide ')

                                device111 = MyDevice.objects.filter(user_id=sender).values('reg_id', 'is_active')

                                device_last = MyDevice.objects.get(reg_id=device111[0]['reg_id'])
                                print(device_last)
                                user1 = User.objects.filter(id=list_receivers[z]).values('first_name', 'last_name')
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
                                device_last.send_message(data={"title": "Echec de l'envoi",
                                                               "receivers": str(user1[0]['first_name']) + " " + str(
                                                                   user1[0]['last_name']),
                                                               "type": 12,
                                                               "message": "n'a pas reçu votre invitation"
                                                               })
                            else:







                                #device1 = device[0]['reg_id']
                                #print(device1)
                                print(' Dans la boucle 2')

                                device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
                                print(device_last)
                                user1 = User.objects.filter(id=sender).values('first_name', 'last_name')
                                print(user1)
                                print(' Envoie ')
                                # device_last.send_message({'message': 'my test message'}, collapse_key='something')

                                # device_last.send_message(data={"title":"Nouveau Invitation",
                                #                                "sender":str(user1[0]['first_name'])+" "+str(user1[0]['last_name']),
                                #                                "type":0,
                                #                                "latitude": latitude,
                                #                                "longitude": longitude
                                #                                })

                                # }
                                device_last.send_message(data={"title": "Nouvelle invitation",
                                                               "sender": str(user1[0]['first_name']) + " " + str(
                                                                   user1[0]['last_name']),
                                                               "type": 4,
                                                               "latitude": latitude,
                                                               "longitude": longitude,
                                                               "id_requette": last_reque1
                                                               })



                            z += 1
                        print(' fin boucle ')

                        # Ajout de code
                        # j = 0

                            # Fin ajout de code

                    print('Fin else ')
                z+=1

            return Response(data={
                'status': 0,
                'message': 'Enregistrement effectif.'})







        except :
            return Response(
                data={
                    'status':1,
                    'message':'Echec de l\'enregistrement.'})


# Ancien le bon code tobejoined
# @api_view(['POST'])
# @transaction.atomic
# def jmrequest_to_bejoined(request):
#
#     if request.method == 'POST':
#
#         #telephone = request.data['telephone']
#         latitude=request.data['latitude']
#         longitude=request.data['longitude']
#         sender=request.data['sender']
#         list_receivers= request.data['receivers']
#
#         try:
#             spot = Spot()
#             requests = Request()
#             request_receivers = Request_Receivers()
#
#             spot.latitude=latitude
#             spot.longitude=longitude
#             spot.save()
#
#             requests.spot=spot
#             requests.date_sender = datetime.now()
#             requests.tobejoined = True
#
#             requests.save()
#
#             last_requete = Request.objects.latest('id')
#             print (' LAST REQUETTE ')
#             last_reque = last_requete.pk
#             print (last_reque)
#
#             print(' ok 1')
#
#             print (' sender ')
#             sender1 = User.objects.get(id=sender)
#             request_receivers.sender= sender1
#             print (request_receivers.sender)
#             print(' ok 2')
#
#             print (list_receivers)
#             i = 0
#             print(' debut boucle ')
#             # with transaction.commit_on_success():
#
#
#             with transaction.atomic():
#
#                 while i < (len(list_receivers)):
#                     print (' ccccccccccccccccccc ')
#                     print (list_receivers[i])
#                     request_receivers.sender = sender1
#                     print (' cc 1 ')
#                     request_receivers.is_active = False
#                     print (' cc 2 ')
#                     # request_receivers.list_receivers.add(list_receivers[i])
#
#                     u = User.objects.get(id=list_receivers[i])
#                     request_receivers.list_receivers = u
#                     print (request_receivers.list_receivers)
#                     print (' cc 3 ')
#                     # request_receivers.state= 'NULL'
#                     # print (' cc 4 ')
#
#                     req = Request.objects.get(id=last_reque)
#                     Request.objects.latest('id')
#                     print (' Requette ')
#                     print (req)
#                     request_receivers.receivers = req
#                     print (' cc 4 ')
#                     a = Request_Receivers(
#                         sender=sender1,
#                         list_receivers = u,
#                         receivers = req,
#                         is_active= False,
#                     )
#                     print(' cc 5 ')
#                     a.save()
#                     print(' cc 6 ')
#
#                     # request_receivers.save()
#                     print(' cc 7 ')
#
#                     last_requete1 = Request_Receivers.objects.latest('id')
#                     print (' LAST REQUETTE ')
#                     last_reque1 = last_requete1.pk
#                     print (last_reque1)
#
#                     # request_receivers.save()
#                     print(' cc 8 ')
#
#
#                     i += 1
#                 print (' fin boucle ')
#
#                 j = 0
#                 while j < (len(list_receivers)):
#                     # device = MyDevice.objects.get(user_id=list_users[i])
#
#                     device = MyDevice.objects.filter(user_id=list_receivers[j]).values('reg_id')
#                     print('Valeur de device')
#                     print(device)
#
#                     device1 = device[0]['reg_id']
#                     print(device1)
#                     print(' Dans la boucle 2')
#
#                     device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
#                     print(device_last)
#                     user1 = User.objects.filter(id=sender).values('first_name', 'last_name')
#                     print(user1)
#                     print(' Envoie ')
#                     # device_last.send_message({'message': 'my test message'}, collapse_key='something')
#
#                     # device_last.send_message(data={"title":"Nouveau Invitation",
#                     #                                "sender":str(user1[0]['first_name'])+" "+str(user1[0]['last_name']),
#                     #                                "type":0,
#                     #                                "latitude": latitude,
#                     #                                "longitude": longitude
#                     #                                })
#
#                     # }
#                     device_last.send_message(data={"title": "Nouvelle invitation",
#                                                    "sender": str(user1[0]['first_name']) + " " + str(
#                                                        user1[0]['last_name']),
#                                                    "type": 4,
#                                                    "latitude": latitude,
#                                                    "longitude": longitude,
#                                                    "id_requette": last_reque1
#                                                    })
#
#                     j += 1
#
#             return Response(data={
#                 'status':0,
#                 'message':'Enregistrement de l’invitation effectif.'
#                 # 'requests': {
#                 #     'id': requests.id,
#                 #     'sender': requests.sender,
#                 #     'receivers': requests.receivers
#                 #     # 'spot':requests.spot
#                 #           },
#                                 }
#                     )
#         except :
#             return Response(
#                 data={
#                     'status':1,
#                     'message':'Echec d’enregistrement de l’invitation.'})
#








# Cartes crees
# @api_view(['POST'])
# def jmrequest_card_past(request):
#
#     user = request.data['user']
#
#     # cards = Card.objects.filter(owner=user)
#
#     cards = Card.objects.filter(owner=user).values('file', 'event__spot__id',
#                                                    'institution__spot__id',
#                                                    'event__spot__latitude',
#                                                    'event__spot__longitude',
#                                                    'institution__spot__latitude',
#                                                    'institution__spot__longitude',
#                                                    'event__name', 'institution__name',
#                                                    'event__date_begin', 'event__date_end',
#                                                    'institution__date_begin',
#                                                    'institution__date_end',
#                                                    'event__chatroom__content')
#
#
#
#     print(cards)
#     print(' Le premier ')
#     print(' Le premier ')
#     print(' Le premier ')
#     print(cards[0])
#
#     print(' Le second ')
#     print(' Le second ')
#     print(' Le second ')
#
#     print(cards[1])
#
#     print(' La taille de la carte ')
#     print(len(cards))
#
#     if request.method == "POST":
#
#         if len(cards) != 0:
#
#             i = 0
#             tableau = []
#
#             while i <= len(cards)-1:
#
#                 if cards[i]['event__spot__id'] == None :
#                     print (' Institutionnelle ')
#
#                     if cards[i]['institution__date_end'] <= datetime.now():
#                         tableau.append(cards[i])
#                         print(list(tableau))
#
#                     i += 1
#
#                 else:
#
#                     print(' METHOD POST EVENEMETIELLE ')
#
#                     if cards[i]['event__date_end'] < datetime.now():
#                         tableau.append(cards[i])
#                         print(list(tableau))
#
#                     i += 1
#
#
#             i+=1
#
#
#             return Response(
#                 data={
#                     'status': 0,
#                     'message': 'Success',
#                     'card': list(tableau)
#                 })
#
#         else:
#
#             return Response(
#                 data={
#                     'status': 0,
#                     'message': 'Pas d historique'})





@api_view(['POST'])
def jmrequest_card_past(request):

    user = request.data['user']

    if request.method == "POST":

        tableau = []

        request_receivers = Request_Receivers.objects.filter(list_receivers=user, state="RECEIVED",
                                                             receivers__with_card=True,
                                                             receivers__date_receivers__lt=timezone.now()).values(
            'receivers__card',
            'receivers',
            'receivers__message',
            'receivers__date_receivers',
            'receivers__card__file',
            'receivers__card__owner__first_name',
            'receivers__card__owner__last_name',
            'receivers__card__owner__photo',
            'receivers__card__institution__name',
            'receivers__card__institution__description',
            'receivers__card__institution__spot__latitude',
            'receivers__card__institution__spot__longitude',
            'receivers__card__institution__spot__name',
            'id',
            'sender__first_name',
            'sender__last_name',
            'sender__photo',

        ).distinct()
        print ('request_receivers')
        print (request_receivers)

        print (' COCOCOCOCOCO')
        print (' COCOCOCOCOCO')
        print (' COCOCOCOCOCO')
        print (' COCOCOCOCOCO')
        print (' COCOCOCOCOCO')

        if len(request_receivers) != 0:
            print (' COCOCOCOCOCO 1')
            print (' COCOCOCOCOCO 1')
            print (' COCOCOCOCOCO 1')
            print (' COCOCOCOCOCO 1')
            print (' COCOCOCOCOCO 1')

            k = 0

            while k < len(request_receivers):
                data = {
                    "card": request_receivers[k]['receivers__card'],
                    "id": request_receivers[k]['id'],
                    "receivers": request_receivers[k]['receivers'],
                    "message": str(request_receivers[k]['receivers__message']),
                    "date_receivers": str(request_receivers[k]['receivers__date_receivers']),
                    "card__file": str(request_receivers[k]['receivers__card__file']),
                    "card__owner__first_name": str(request_receivers[k]['receivers__card__owner__first_name']),
                    "card__owner__last_name": str(request_receivers[k]['receivers__card__owner__last_name']),
                    "card__owner__photo": str(request_receivers[k]['receivers__card__owner__photo']),
                    "card__institution__name": str(request_receivers[k]['receivers__card__institution__name']),
                    "card__institution__description": str(request_receivers[k]['receivers__card__institution__description']),
                    "card__institution__spot__latitude": request_receivers[k]['receivers__card__institution__spot__latitude'],
                    "card__institution__spot__longitude": request_receivers[k]['receivers__card__institution__spot__longitude'],
                    "card__institution__spot__name": str(request_receivers[k]['receivers__card__institution__spot__name']),
                    "sender__first_name": str(request_receivers[k]['sender__first_name']),
                    "sender__last_name": str(request_receivers[k]['sender__last_name']),
                    "sender__photo": str(request_receivers[k]['sender__photo']),
                }

                print ('data')
                print ('data')
                print ('data')
                print ('data')
                print ('data')
                print ('data')
                print ('data')
                print (data)
                print (' DEBUT  ')
                # print (data[k])
                print (' FIN ')
                print (' FIN ')

                tableau.append(data)
                # print (tableau)

                k += 1

        print(request_receivers)
        print('request_receivers')
        print('request_receivers')
        print('request_receivers')
        print('request_receivers')
        # print(len(request_receivers))




        cards = UserCardFavourite.objects.filter(sender=user).values('card', 'card__file', 'state',
                                                                     'card__institution', 'card__institution__name',
                                                                     'card__institution', 'card__institution__spot__id', 'card__institution__spot__latitude',
                                                                     'card__institution__spot__longitude',
                                                                     'card__event__spot__latitude', 'card__event__spot__longitude', 'card__event__date_begin',
                                                                     'card__event__date_end', 'card__event__spot__id', 'card__event__chatroom__content',
                                                                     'card__event__chatroom__userss__first_name', 'card__event__name', 'card__event__chatroom__id',
                                                                     'card__event__chatroom__userss__last_name', 'card__event__chatroom__userss__photo',
                                                                     ).annotate(card__event__chatroom__users=Count('card__event__chatroom__users'))
                                                                     #'card__event__chatroom__users')

        print (cards)

        if len(cards) != 0:
            i = 0
            # tableau = []

            while i < len(cards):

                if cards[i]['card__event__spot__id'] == None :
                    print (' Institutionnelle ')

                    #if cards[i]['card__institution__date_end'] <= datetime.now():
                        # tableau.append(cards[i])
                    #    print(list(tableau))

                    #    i += 1

                    #else:
                    #    i += 1
                    i += 1

                else:

                    print(' METHOD POST EVENEMETIELLE ')

                    if cards[i]['card__event__date_end'] <= timezone.now():
                        tableau.append(cards[i])
                        print(list(tableau))

                        i += 1

                    else:
                         i += 1


            i+=1
        else:
            tableau = []


        card = UserCard.objects.filter(users_receivers=user).values('card', 'card__file', 'state',
                                                                    'card__institution', 'card__institution__name',
                                                                    'card__institution', 'card__institution__spot__id',
                                                                    'card__institution__spot__latitude',
                                                                    'card__institution__spot__longitude',
                                                                    'card__event__spot__latitude',
                                                                    'card__event__spot__longitude',
                                                                    'card__event__date_begin', 'card__event__name',
                                                                    'card__event__date_end', 'card__event__spot__id', 'card__event__chatroom__content',
                                                                    'card__event__chatroom__userss__first_name', 'card__event__chatroom__userss__last_name',
                                                                    'card__event__chatroom__userss__photo', 'card__event__chatroom__id'
                                                                    ).annotate(card__event__chatroom__users=Count('card__event__chatroom__users'))

                                                                    # 'card__event__chatroom__userss__photo', 'card__event__chatroom__users')




        # print (card['card__event__chatroom__users'])

        print (' UserCard ')
        print (' UserCard ')
        print (' UserCard ')
        print (' UserCard ')
        print (' UserCard ')

        #print(card[0])

        print(' TABLEAU ')
        print(' TABLEAU ')
        print(' TABLEAU ')
        print(' TABLEAU ')
        # print(tableau[0])



        if len(card)!= 0:

            print (" cool ")
            print (" cool ")
            print (" cool ")
            print (" cool ")
            print (" cool ")

            z = 0
            while z < len(card):

                print(' LA BOUCLE ')
                print(' LA BOUCLE ')
                print(' LA BOUCLE ')
                print(' LA BOUCLE ')
                print(' LA BOUCLE ')
                print(card[z])

                if card[z] in tableau:
                    print(' COOL ')
                    print(' COOL ')
                    print(' COOL ')
                    print(' COOL ')
                    print(' COOL ')

                    z += 1

                else:


                    print (' NON COOL ')
                    print (' NON COOL ')
                    print (' NON COOL ')
                    print (' NON COOL ')
                    print (' NON COOL ')
                    print (' NON COOL ')



                    if card[z]['card__event__spot__id'] == None:
                        print (' Institutionnelle ')

                        #if card[z]['card__institution__date_end'] <= datetime.now() and (card[z]['state']=="RECEIVED"):
                        #if card[z]['card__institution__date_end'] <= datetime.now():
                            # tableau.append(card[z])
                        #    print(list(tableau))
                        #    z += 1
                        #else:
                        #    z += 1

                        z += 1


                    else:
                        print(' METHOD POST EVENEMETIELLE ')

                        if card[z]['card__event__date_end'] <= timezone.now() and (card[z]['state']=="RECEIVED"):

                        # if card[z]['card__event__date_end'] <= datetime.now():

                            tableau.append(card[z])
                            print(list(tableau))
                            z += 1
                        else:
                            z += 1



            z +=1
            l = tableau

            return Response(
                data={
                    'status': 0,
                    'message': 'La liste des cartes passées.',
                    'card': list(l)
                })

        else:


            if len(tableau) == 0:

                return Response(
                    data={
                        'status': 1,
                        'message': 'Aucune invitation passée.'
                    })
            else:
                l = tableau

                return Response(
                    data={
                        'status': 0,
                        'message': 'La liste des cartes passées.',
                        'card': list(l)
                    })

        # return Response(
        #     data={
        #         'status': 0,
        #         'message': 'Effectue avec Success',
        #         'card': list(l)
        #     })








@api_view(['POST'])
def jmrequest_card_next(request):

    user = request.data['user']

    if request.method == "POST":

        tableau = []

        request_receivers = Request_Receivers.objects.filter(list_receivers=user, state="RECEIVED",
                                                             receivers__with_card=True,
                                                             receivers__date_receivers__gt=timezone.now()).values(
            'receivers__card',
            'receivers',
            'receivers__message',
            'receivers__date_receivers',
            'receivers__card__file',
            'receivers__card__owner__first_name',
            'receivers__card__owner__last_name',
            'receivers__card__owner__photo',
            'receivers__card__institution__name',
            'receivers__card__institution__description',
            'receivers__card__institution__spot__latitude',
            'receivers__card__institution__spot__longitude',
            'receivers__card__institution__spot__name',
            'id',
            'sender__first_name',
            'sender__last_name',
            'sender__photo',
        ).distinct()
        print ('request_receivers')
        print (request_receivers)

        print (' COCOCOCOCOCO')
        print (' COCOCOCOCOCO')
        print (' COCOCOCOCOCO')
        print (' COCOCOCOCOCO')
        print (' COCOCOCOCOCO')

        if len(request_receivers) != 0:
            print (' COCOCOCOCOCO 1')
            print (' COCOCOCOCOCO 1')
            print (' COCOCOCOCOCO 1')
            print (' COCOCOCOCOCO 1')
            print (' COCOCOCOCOCO 1')

            k = 0

            while k < len(request_receivers):
                data = {
                    "card__id": request_receivers[k]['receivers__card'],
                    "id": request_receivers[k]['id'],
                    "receivers": request_receivers[k]['receivers'],
                    "message": str(request_receivers[k]['receivers__message']),
                    "date_receivers": str(request_receivers[k]['receivers__date_receivers']),
                    "card__file": str(request_receivers[k]['receivers__card__file']),
                    "card__owner__first_name": str(request_receivers[k]['receivers__card__owner__first_name']),
                    "card__owner__last_name": str(request_receivers[k]['receivers__card__owner__last_name']),
                    "card__owner__photo": str(request_receivers[k]['receivers__card__owner__photo']),
                    "card__institution__name": str(request_receivers[k]['receivers__card__institution__name']),
                    "card__institution__description": str(request_receivers[k]['receivers__card__institution__description']),
                    "card__institution__spot__latitude": request_receivers[k]['receivers__card__institution__spot__latitude'],
                    "card__institution__spot__longitude": request_receivers[k]['receivers__card__institution__spot__longitude'],
                    "card__institution__spot__name": str(request_receivers[k]['receivers__card__institution__spot__name']),
                    "sender__first_name": str(request_receivers[k]['sender__first_name']),
                    "sender__last_name": str(request_receivers[k]['sender__last_name']),
                    "sender__photo": str(request_receivers[k]['sender__photo']),
                }

                print ('data')
                print ('data')
                print ('data')
                print ('data')
                print ('data')
                print ('data')
                print ('data')
                print (data)
                print (' DEBUT  ')
                # print (data[k])
                print (' FIN ')
                print (' FIN ')

                tableau.append(data)
                print (tableau)

                k += 1

        print(request_receivers)
        print('request_receivers')
        print('request_receivers')
        print('request_receivers')
        print('request_receivers')
        print(len(request_receivers))









        cards = UserCardFavourite.objects.filter(sender=user).values('card', 'card__file', 'state',
                                                                     'card__institution', 'card__institution__name',
                                                                     'card__institution', 'card__institution__spot__id', 'card__institution__spot__latitude',
                                                                     'card__institution__spot__longitude',
                                                                     'card__event__spot__latitude', 'card__event__spot__longitude', 'card__event__date_begin',
                                                                     'card__event__date_end', 'card__event__spot__id', 'card__event__chatroom__content',
                                                                     'card__event__chatroom__userss__first_name', 'card__event__name', 'card__event__chatroom__id',
                                                                     'card__event__chatroom__userss__last_name', 'card__event__chatroom__userss__photo'
                                                                     ).annotate(card__event__chatroom__users=Count('card__event__chatroom__users'))

        print (cards)

        if len(cards) != 0:
            i = 0
            # tableau = []

            while i < len(cards):

                if cards[i]['card__event__spot__id'] == None :
                    print (' Institutionnelle ')

                    #if cards[i]['card__institution__date_end'] > datetime.now():
                        # tableau.append(cards[i])
                    #    print(list(tableau))

                    i += 1

                else:

                    print(' METHOD POST EVENEMETIELLE ')

                    if cards[i]['card__event__date_end'] > timezone.now():
                        tableau.append(cards[i])
                        print(list(tableau))

                    i += 1


            i+=1
        else:
            tableau = []


        card = UserCard.objects.filter(users_receivers=user).values('card', 'card__file', 'state',
                                                                    'card__institution', 'card__institution__name',
                                                                    'card__institution', 'card__institution__spot__id',
                                                                    'card__institution__spot__latitude',
                                                                    'card__institution__spot__longitude',
                                                                    'card__event__spot__latitude',
                                                                    'card__event__spot__longitude',
                                                                    'card__event__date_begin', 'card__event__name',
                                                                    'card__event__date_end', 'card__event__spot__id', 'card__event__chatroom__content',
                                                                    'card__event__chatroom__userss__first_name', 'card__event__chatroom__userss__last_name',
                                                                    'card__event__chatroom__userss__photo', 'card__event__chatroom__id'
                                                                    ).annotate(card__event__chatroom__users=Count('card__event__chatroom__users'))

        print (' UserCard ')
        print (' UserCard ')
        print (' UserCard ')
        print (' UserCard ')
        print (' UserCard ')

        print(len(card))

        print(' TABLEAU ')
        print(' TABLEAU ')
        print(' TABLEAU ')
        print(' TABLEAU ')
        # print(tableau[0])



        if len(card)!= 0:

            print (" cool ")
            print (" cool ")
            print (" cool ")
            print (" cool ")
            print (" cool ")

            z = 0
            while z < len(card):

                print(' LA BOUCLE ')
                print(' LA BOUCLE ')
                print(' LA BOUCLE ')
                print(' LA BOUCLE ')
                print(' LA BOUCLE ')
                print(card[z])

                if card[z] in tableau:
                    print(' COOL ')
                    print(' COOL ')
                    print(' COOL ')
                    print(' COOL ')
                    print(' COOL ')

                    z += 1

                else:


                    print (' NON COOL ')
                    print (' NON COOL ')
                    print (' NON COOL ')
                    print (' NON COOL ')
                    print (' NON COOL ')
                    print (' NON COOL ')



                    if card[z]['card__event__spot__id'] == None:
                        print (' Institutionnelle ')

                        #if card[z]['card__institution__date_end'] > datetime.now() and (card[z]['state']=="RECEIVED"):
                        #if card[z]['card__institution__date_end'] <= datetime.now():
                            # tableau.append(card[z])
                        #    print(list(tableau))
                            #z += 1
                        z += 1

                        #else:
                        #    z += 1


                    else:
                        print(' METHOD POST EVENEMETIELLE ')

                        if card[z]['card__event__date_end'] > timezone.now() and (card[z]['state']=="RECEIVED"):
                        # if card[z]['card__event__date_end'] <= datetime.now():
                            tableau.append(card[z])
                            print(list(tableau))
                            z += 1

                        else:
                            z += 1



            z +=1
            l = tableau

            if len (l)== 0:
                return Response(
                    data={
                        'status': 1,
                        'message': 'Aucune carte à venir.'
                    })
            else:

                return Response(

                    data={
                        'status': 0,
                        'message': 'La liste des cartes à venir.',
                        'card': list(l)
                    })





        else:


            if len(tableau) == 0:

                return Response(
                    data={
                        'status': 1,
                        'message': 'Aucune carte à venir.',
                    })
            else:
                l = tableau

                return Response(
                    data={
                        'status': 0,
                        'message': 'La liste des cartes à venir.',
                        'card': list(l)
                    })





@api_view(['POST'])
def jmrequest_card_wait(request):




    if request.method == "POST":

        tableau = []

        user = request.data['user']

        # requests = Request.objects.filter(receivers=)  receivers__date_receivers <= datetime.now()         , receivers__date_receivers__lte = datetime.now()
        request_receivers = Request_Receivers.objects.filter(list_receivers=user, state="NULL",
                                                             receivers__with_card=True,
                                                             receivers__date_receivers__gt=timezone.now()).values(
            'receivers__card',
            'receivers',
            'receivers__message',
            'receivers__date_receivers',
            'receivers__card__file',
            'receivers__card__owner__first_name',
            'receivers__card__owner__last_name',
            'receivers__card__owner__photo',
            'receivers__card__institution__name',
            'receivers__card__institution__description',
            'receivers__card__institution__spot__latitude',
            'receivers__card__institution__spot__longitude',
            'receivers__card__institution__spot__name',
            'id',
            'sender',
            'sender__first_name',
            'sender__last_name',
            'sender__photo',
        ).distinct()

        print ('request_receivers')
        # print (request_receivers)

        print (' COCOCOCOCOCO')
        print (' COCOCOCOCOCO')
        print (' COCOCOCOCOCO')
        print (' COCOCOCOCOCO')
        print (' COCOCOCOCOCO')


        if len(request_receivers)!=0:
            print (' COCOCOCOCOCO 1')
            print (' COCOCOCOCOCO 1')
            print(len(request_receivers))
            print(request_receivers)

            print (' COCOCOCOCOCO 1')
            print (' COCOCOCOCOCO 1')
            print (' COCOCOCOCOCO 1')

            k = 0

            while k < len(request_receivers):

                data = {
                    "card__id": request_receivers[k]['receivers__card'],
                    "receivers": request_receivers[k]['receivers'],
                    "id": request_receivers[k]['id'],
                    "message": str(request_receivers[k]['receivers__message']),
                    "date_receivers": str(request_receivers[k]['receivers__date_receivers']),
                    "card__file": str(request_receivers[k]['receivers__card__file']),
                    "card__owner__first_name": str(request_receivers[k]['receivers__card__owner__first_name']),
                    "card__owner__last_name": str(request_receivers[k]['receivers__card__owner__last_name']),
                    "card__owner__photo": str(request_receivers[k]['receivers__card__owner__photo']),
                    "card__institution__name": str(request_receivers[k]['receivers__card__institution__name']),
                    "card__institution__description": str(request_receivers[k]['receivers__card__institution__description']),
                    "card__institution__spot__latitude": request_receivers[k]['receivers__card__institution__spot__latitude'],
                    "card__institution__spot__longitude": request_receivers[k]['receivers__card__institution__spot__longitude'],
                    "card__institution__spot__name": str(request_receivers[k]['receivers__card__institution__spot__name']),
                    "sender": request_receivers[k]['sender'],
                    "sender__first_name": str(request_receivers[k]['sender__first_name']),
                    "sender__last_name": str(request_receivers[k]['sender__last_name']),
                    "sender__photo": str(request_receivers[k]['sender__photo']),
                    "type":"join me"
                }

                tableau.append(data)

                print ('data')
                print ('data')
                print ('data')
                # print(k)
                print ('data')
                print ('data')
                print ('data')
                print ('data')
                print (' DEBUT  ')
                # print (data[k])
                print (' FIN ')
                print (' FIN ')


                print (tableau)

                k += 1
        # print (request_receivers[0]['receivers__card__institution__spot__latitude'])
        print(request_receivers)
        print('request_receivers')
        print('request_receivers')
        print('request_receivers')
        print('request_receivers')
        print(len(request_receivers))

        if len(request_receivers) != 0:
            # tableau.append(request_receivers[0])

            j=0
            while j < (len(request_receivers)):
                # tableau.append(request_receivers[j])
                j += 1



        card = UserCard.objects.filter(users_receivers=user, state="NULL", card__event__date_end__gt=timezone.now()).values('card__id',
                                                                                  'card__file',
                                                                                  'state',
                                                                                  'card__owner__first_name',
                                                                                  'card__owner__last_name',
                                                                                  'card__owner__photo',
                                                                                  'card__institution__name',
                                                                                  'card__institution__spot__name',
                                                                                  'card__institution__spot__latitude',
                                                                                  'card__institution__spot__longitude',
                                                                                  'card__event__name',
                                                                                  'card__event__description',
                                                                                  'card__event__spot__name',
                                                                                  'card__event__spot__latitude',
                                                                                  'card__event__spot__longitude',
                                                                                  'card__event__date_begin',
                                                                                  'card__event__date_end',
                                                                                  'card__event__chatroom__content',
                                                                                  'card__event__chatroom__id',
                                                                                  'card__event__chatroom__userss__first_name',
                                                                                  'card__event__chatroom__userss__last_name',
                                                                                  'card__event__chatroom__userss__photo' ,
                                                                                  'id'
                                                                                  ).annotate(card__event__chatroom__users=Count('card__event__chatroom__users'))
        print (' USERCARD ')
        print (' USERCARD ')
        print (' USERCARD ')
        print (' USERCARD ')
        print (card)

        if len(card) != 0:
            # tableau.append(card[0])

            k = 0
            while k < (len(card)):
                data1 = {
                    "card__file": card[k]['card__file'],
                    "state": card[k]['state'],
                    "card__owner__first_name": str(card[k]['card__owner__first_name']),
                    "card__owner__last_name": str(card[k]['card__owner__last_name']),
                    "card__owner__photo": str(card[k]['card__owner__photo']),
                    "card__institution__name": card[k]['card__institution__name'],
                    "card__institution__spot__name": card[k]['card__institution__spot__name'],
                    "card__institution__spot__latitude": card[k]['card__institution__spot__latitude'],
                    "card__institution__spot__longitude": card[k]['card__institution__spot__longitude'],
                    "card__event__name": str(card[k]['card__event__name']),
                    "card__event__description": str(card[k]['card__event__description']),
                    "card__event__spot__name": card[k]['card__event__spot__name'],
                    "card__event__spot__latitude": card[k]['card__event__spot__latitude'],
                    "card__event__spot__longitude": card[k]['card__event__spot__longitude'],
                    "card__event__date_begin": str(card[k]['card__event__date_begin']),
                    "card__event__date_end": str(card[k]['card__event__date_end']),
                    "card__event__chatroom__id": str(card[k]['card__event__chatroom__id']),
                    "card__event__chatroom__userss__first_name": str(card[k]['card__event__chatroom__userss__first_name']),
                    "card__event__chatroom__userss__last_name": str(card[k]['card__event__chatroom__userss__last_name']),
                    "card__event__chatroom__userss__photo": str(card[k]['card__event__chatroom__userss__photo']),
                    "id": card[k]['id'],
                    "card__event__chatroom__users": str(card[k]['card__event__chatroom__users']),
                    "type":"partage"
                }

                tableau.append(data1)
                k += 1

        # tableau = request_receivers, card
        print (tableau)
        print (' Taille Tableau ')
        print (' Taille Tableau ')
        print (' Taille Tableau ')
        print (' Taille Tableau ')
        print (' Taille Tableau ')
        print (len(tableau))








        card12 = UserCard.objects.filter(users_receivers=user, state="NULL").values('card__id',
                                                                                    'card__file',
                                                                                    'state',
                                                                                    'card__owner__first_name',
                                                                                    'card__owner__last_name',
                                                                                    'card__owner__photo',
                                                                                    'card__institution__name',
                                                                                    'card__institution__spot__name',
                                                                                    'card__institution__spot__id',
                                                                                    'card__institution__spot__latitude',
                                                                                    'card__institution__spot__longitude',
                                                                                    'id',
                                                                                    'sender',
                                                                                    'sender__first_name',
                                                                                    'sender__last_name',
                                                                                    'sender__photo'
                                                                                    )
        print (' USERCARD ')
        print (' USERCARD ')
        print (' USERCARD ')
        print (' USERCARD ')
        print (card12)

        print (' USERCARD  +++++++')


        if len(card12) != 0:
            # tableau.append(card[0])

            k = 0
            while k < (len(card12)):
                print (' Dans la boucle ')
                if card12[k]['card__institution__spot__id'] != None:
                    print (' Dans la boucle Dnas le IF ')

                    data12 = {
                        "card__file": card12[k]['card__file'],
                        "state": card12[k]['state'],
                        "card__owner__first_name": str(card12[k]['card__owner__first_name']),
                        "card__owner__last_name": str(card12[k]['card__owner__last_name']),
                        "card__owner__photo": str(card12[k]['card__owner__photo']),
                        "card__institution__name": str(card12[k]['card__institution__name']),
                        "card__institution__spot__name": str(card12[k]['card__institution__spot__name']),
                        "card__institution__spot__latitude": card12[k]['card__institution__spot__latitude'],
                        "card__institution__spot__longitude": card12[k]['card__institution__spot__longitude'],
                        "id": card12[k]['id'],
                        "type": "partage",
                        "sender": card12[k]['sender'],
                        "sender__first_name": str(card12[k]['sender__first_name']),
                        "sender__last_name": str(card12[k]['sender__last_name']),
                        "sender__photo": str(card12[k]['sender__photo']),
                    }

                    tableau.append(data12)

                    k += 1

                k += 1

        # tableau = request_receivers, card
        print (tableau)
        print (' Taille Tableau ')
        print (' Taille Tableau ')
        print (' Taille Tableau ')
        print (' Taille Tableau ')
        print (' Taille Tableau ')
        print (len(tableau))



        if len(tableau)==0:
            return Response(
                data={
                    'status': 1,
                    'message': 'Aucune carte en attente de réponse.'
                })
        else:

            return Response(
                data={
                    'status': 0,
                    'message': 'La liste des cartes en attente.',
                    'card':list(tableau)
                })




@api_view(['POST'])
def joinme_tobejoined_send(request):
    if request.method == "POST":
        tableau = []

        user = request.data['user']

        request_receivers = Request_Receivers.objects.filter(sender=user, receivers__with_card=False).values('receivers',
                                                                                                             'id',
                                                                                                             'receivers__spot__latitude',
                                                                                                             'receivers__spot__longitude',
                                                                                                             'receivers__tobejoined',
                                                                                                             'state',
                                                                                                             'list_receivers',
                                                                                                             'list_receivers__first_name',
                                                                                                             'list_receivers__last_name',
                                                                                                             'list_receivers__photo').distinct()





        if len(request_receivers)  == 0:

            return Response(
                data={
                    'status': 1,
                    'message': 'Vous n\'avez pas envoyés d\'invitation.',
                })
        else:

            k = 0

            while k < len(request_receivers):
                data = {
                    "id": request_receivers[k]['id'],
                    "latitude": request_receivers[k]['receivers__spot__latitude'],
                    "longitude": request_receivers[k]['receivers__spot__latitude'],
                    "tobejoined": request_receivers[k]['receivers__tobejoined'],
                    "state": request_receivers[k]['state'],
                    "id_receivers": request_receivers[k]['list_receivers'],
                    "receivers__first_name": str(request_receivers[k]['list_receivers__first_name']),
                    "receivers__last_name": str(request_receivers[k]['list_receivers__last_name']),
                    "receivers__photo": str(request_receivers[k]['list_receivers__photo']),
                }

                tableau.append(data)

                print('data')
                print('data')
                print('data')
                # print(k)
                print('data')
                print('data')
                print('data')
                print('data')
                print(' DEBUT  ')
                # print (data[k])
                print(' FIN ')
                print(' FIN ')

                print(tableau)

                k += 1

        return Response(
                data={
                    'status': 0,
                    'message': 'La liste des invitations envoyées.',
                    'requests': list(tableau)
                })











@api_view(['POST'])
def joinme_tobejoined_receivers(request):
    if request.method == "POST":
        tableau = []

        user = request.data['user']

        request_receivers = Request_Receivers.objects.filter(list_receivers=user, receivers__with_card=False).values('receivers',
                                                                                                             'id',
                                                                                                             'receivers__spot__latitude',
                                                                                                             'receivers__spot__longitude',
                                                                                                             'receivers__tobejoined',
                                                                                                             'state',
                                                                                                             'sender',
                                                                                                             'sender__first_name',
                                                                                                             'sender__last_name',
                                                                                                             'sender__photo').distinct()

        print('request_receivers')
        print('request_receivers')
        print('request_receivers')
        print('request_receivers')
        print(request_receivers)





        if len(request_receivers)  == 0:

            return Response(
                data={
                    'status': 1,
                    'message': 'Vous n\'avez pas reçus d\'invitation.',
                })
        else:

            k = 0

            while k < len(request_receivers):
                data = {
                    "id": request_receivers[k]['id'],
                    "latitude": request_receivers[k]['receivers__spot__latitude'],
                    "longitude": request_receivers[k]['receivers__spot__latitude'],
                    "tobejoined": request_receivers[k]['receivers__tobejoined'],
                    "state": request_receivers[k]['state'],
                    "id_sender": request_receivers[k]['sender'],
                    "sender__first_name": str(request_receivers[k]['sender__first_name']),
                    "sender__last_name": str(request_receivers[k]['sender__last_name']),
                    "sender__photo": str(request_receivers[k]['sender__photo']),
                }

                tableau.append(data)

                print('data')
                print('data')
                print('data')
                # print(k)
                print('data')
                print('data')
                print('data')
                print('data')
                print(' DEBUT  ')
                # print (data[k])
                print(' FIN ')
                print(' FIN ')

                print(tableau)

                k += 1

        return Response(
                data={
                    'status': 0,
                    'message': 'La liste des invitations reçus.',
                    'requests':list(tableau)
                })



# joinme_tobejoined_send
@api_view(['POST'])
def joinme_tobejoined_send_new(request):

    if request.method == "POST":

        latitude = request.data['latitude']
        longitude = request.data['longitude']
        sender = request.data['sender']
        list_receivers = request.data['receivers']
        id_request = request.data['id_requests']

        try:



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

            requests = Request_Receivers.objects.get(id=id_request)
            print(requests.receivers.spot.latitude)
            print(requests.receivers.spot.longitude)
            requests.receivers.spot.latitude = latitude
            requests.receivers.spot.longitude = longitude
            requests.receivers.date_sender = datetime.now()

            requests.save()
            print('Fin save ')


            # Ajout de code
            j = 0
            while j < (len(list_receivers)):
                # device = MyDevice.objects.get(user_id=list_users[i])


                device000 = MyDevice.objects.filter(user_id=list_receivers[j]).values('reg_id')
                print('Valeur de device 1')
                print(device000)

                if len(device000) == 0:
                    print(' vide ')
                    print(' vide ')
                    print(' vide ')
                    print(' vide ')

                    device111 = MyDevice.objects.filter(user_id=sender).values('reg_id', 'is_active')

                    device_last = MyDevice.objects.get(reg_id=device111[0]['reg_id'])
                    print(device_last)
                    user1 = User.objects.filter(id=list_receivers[j]).values('first_name', 'last_name')
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
                    device_last.send_message(data={"title": "Echec de l'envoi",
                                                   "receivers": str(user1[0]['first_name']) + " " + str(
                                                       user1[0]['last_name']),
                                                   "type": 12,
                                                   "message": "n'a pas reçu votre invitation"
                                                   })
                    j += 1

                else:

                    device = MyDevice.objects.filter(user_id=list_receivers[j]).values('reg_id')
                    print('Valeur de device 2')
                    print(device)

                    device1 = device[0]['reg_id']
                    print(device1)
                    print(' Dans la boucle 2')

                    device_last = MyDevice.objects.get(reg_id=device[0]['reg_id'])
                    print(device_last)
                    user1 = User.objects.filter(id=sender).values('first_name', 'last_name')
                    print(user1)
                    print(' Envoie ')
                    # device_last.send_message({'message': 'my test message'}, collapse_key='something')

                    # device_last.send_message(data={"title":"Nouveau Invitation",
                    #                                "sender":str(user1[0]['first_name'])+" "+str(user1[0]['last_name']),
                    #                                "type":0,
                    #                                "latitude": latitude,
                    #                                "longitude": longitude
                    #                                })

                    # }
                    device_last.send_message(data={"title": "Nouveau Invitation",
                                                   "sender": str(user1[0]['first_name']) + " " + str(user1[0]['last_name']),
                                                   "type": 0,
                                                   "latitude": latitude,
                                                   "longitude": longitude,
                                                   "id_requette": id_request
                                                   })

                    j += 1

                # Fin ajout de code




            print(requests)
            return Response(data={
                'status': 0,
                'message': 'Envoi de la requête effective.'
            })




        except:
            return Response(
                data={
                    'status': 1,
                    'message': 'Echec de l\'envoi de la requête.'})
