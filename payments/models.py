from django.db import models


class Account(models.Model):
    CASINO = 0
    PLAYER = 1
    PAYMENT_GATEWAY = 2

    TYPE_CHOICES = (
        (CASINO, "Casino"),
        (PLAYER, "Player"),
        (PAYMENT_GATEWAY, "Payment Gateway"),
    )

    type = models.PositiveIntegerField(choices=TYPE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def balance(self):
        amount_credited = Transaction.objects.filter(to_account=self).aggregate(models.Sum('amount'))['amount__sum'] or 0
        amount_debited = Transaction.objects.filter(from_account=self).aggregate(models.Sum('amount'))['amount__sum'] or 0
        return amount_credited - amount_debited

    def __str__(self):
        account_holder = ''

        if hasattr(self, 'casino'):
            account_holder = self.casino
        elif hasattr(self, 'player'):
            account_holder = self.player
        elif hasattr(self, 'paymentgateway'):
            account_holder = self.paymentgateway

        return u"%s's Account" % account_holder


class PaymentGateway(models.Model):
    name = models.CharField(max_length=80)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"%s" % self.name


class Transaction(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='from_account')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_account')
    amount = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"%s to %s" % (self.from_account, self.to_account)