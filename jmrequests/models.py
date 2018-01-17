from django.db import models
from users.models import User
from jmspots.models import Card, Spot


class Request(models.Model):

    # receivers = models.ManyToManyField('self', through='Request_Receivers', symmetrical=False) avant

    # receivers = models.ManyToManyField(User, through='Request_Receivers', symmetrical=False, through_fields='receivers')
    receivers = models.ManyToManyField(User, through='Request_Receivers', symmetrical=False, through_fields=('receivers', 'list_receivers'))

    ##### à commenter     receivers = models.ManyToManyField(User, through='Request_Receivers', symmetrical=False, through_fields='list_receivers')

    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True)
    date_sender = models.DateTimeField(null=True, blank=True)
    date_receivers = models.DateTimeField(null=True, blank=True)
    with_card = models.BooleanField(default=False)
    message = models.CharField(max_length=255, null=True, blank=True)
    in_progress = models.BooleanField(default=False) # Etat en cours de la requêtte
    tobejoined = models.BooleanField(default=False)

    def __str__(self):
        return str(self.spot)



    # def add_request(self, user):
    #     created = Request.objects.get_or_create(from_employee=self, to_employee__in=employee, )
    #     return pm


class Request_Receivers(models.Model):

    RECEIVED = 'RECEIVED'
    DECLINED = 'DECLINED'
    NULL = 'NULL'

    STATE_REQUEST = (
        (RECEIVED, 'RECEIVED'),
        (DECLINED, 'DECLINED'),
        (NULL, 'NULL'),
    )

    sender = models.ForeignKey(User, related_name='send_receivers')
    list_receivers = models.ForeignKey(User, related_name='list_receivers')
    receivers = models.ForeignKey(Request, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    state = models.CharField(max_length=20, choices=STATE_REQUEST, default=NULL)