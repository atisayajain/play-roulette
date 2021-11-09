from django.db import models

import payments.models
import casinos.models


class Player(models.Model):
    """ 
    Model Class for Player.
    """

    name = models.TextField(max_length=80)
    account = models.OneToOneField(payments.models.Account, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"%s" % self.name


class PlayerCasinoMap(models.Model):
    """ 
    Model Class to map Player and Casino.
    """

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    casino = models.ForeignKey(casinos.models.Casino, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)