from django.contrib import admin

from . import models


class PlayerAdmin(admin.ModelAdmin):
    pass

class PlayerCasinoAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.PlayerCasinoMap, PlayerCasinoAdmin)