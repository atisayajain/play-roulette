from django.contrib import admin

from . import models


class AccountAdmin(admin.ModelAdmin):
    pass


class PaymentGatewayAdmin(admin.ModelAdmin):
    pass


class TransactionAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.PaymentGateway, PaymentGatewayAdmin)
admin.site.register(models.Transaction, TransactionAdmin)