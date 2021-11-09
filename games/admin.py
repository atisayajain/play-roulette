from django.contrib import admin

from . import models


class GameAdmin(admin.ModelAdmin):
    pass


class GameTimeAdmin(admin.ModelAdmin):
    pass


class BallThrowAdmin(admin.ModelAdmin):
    pass


class BetAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Game, GameAdmin)
admin.site.register(models.GameTime, GameTimeAdmin)
admin.site.register(models.BallThrow, BallThrowAdmin)
admin.site.register(models.Bet, BetAdmin)