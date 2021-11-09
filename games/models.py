from django.db import models

import casinos.models
import payments.models
import players.models


class Game(models.Model):
    """ 
    Model Class for Game.
    """

    WIN_RATIO = 2
    MIN_NUMBER = 1
    MAX_NUMBER = 36

    dealer = models.ForeignKey(casinos.models.Dealer, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"%s - Game %d" % (self.dealer.casino, self.id)


class GameTime(models.Model):
    """ 
    Model Class for Game start and end time.
    """

    START = 1
    END = 0

    TYPE_CHOICES = (
        (START, "Start"),
        (END, "End")
    )

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    type = models.PositiveIntegerField(choices=TYPE_CHOICES)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        type_str = 'start' if self.type == self.START else 'end'
        return u"Game %d's %s time" % (self.game.id, type_str)


class BallThrow(models.Model):
    """ 
    Model Class for Ball Throw.
    """

    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(null=True)

    def __str__(self):
        return u"Result of Game %d" % (self.game.id)


class Bet(models.Model):
    """ 
    Model Class for Bet.
    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(players.models.Player,
                               on_delete=models.CASCADE)
    transaction = models.OneToOneField(payments.models.Transaction,
                                       on_delete=models.CASCADE)

    bet_number = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (u"%s's bet of Rs. %d on %d  on game %d"
                % (self.player.name, self.number, self.transaction.amount,
                   self.game.id))
