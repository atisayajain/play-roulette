from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_reverse_admin import ReverseModelAdmin

from . import models


class CasinoDealerInline(admin.TabularInline):

    def dealer_admin(self, obj):
        href = reverse('admin:casinos_dealer_change',
                        args=[obj.id])

        return mark_safe("<a href='%s' target='_blank'>%s</a>" % (href, obj.name))

    dealer_admin.short_description = "Dealer Admin"

    readonly_fields = ("name", "dealer_admin")
    fields = ("name", "dealer_admin")
    model = models.Dealer

    def get_queryset(self, request):
        qs = super(CasinoDealerInline, self).get_queryset(request)
        return qs


class CasinoAdmin(admin.ModelAdmin):
    #inlines = [CasinoDealerInline]
    pass


class DealerAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Casino, CasinoAdmin)
admin.site.register(models.Dealer, DealerAdmin)