from django.db import models
from django.db.models.deletion import CASCADE

import payments.models


class Casino(models.Model):
    """ 
    Model Class for Casino.
    """

    name = models.TextField(max_length=80)
    account = models.OneToOneField(payments.models.Account, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"%s" % (self.name)


class Dealer(models.Model):
    """ 
    Model Class for Dealer.
    """

    name = models.TextField(max_length=80)
    casino = models.ForeignKey(Casino, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"%s" % (self.name)