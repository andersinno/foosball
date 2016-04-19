from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from foosball.users.models import User


class Table(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name=_("name"))
    description = models.TextField(blank=True, verbose_name=_("description"))

    def __str__(self):
        return self.name


class Game(TimeStampedModel):
    created_by = models.ForeignKey(
        User, related_name="games_created", editable=False, null=True, verbose_name=_("created by")
    )
    modified_by = models.ForeignKey(
        User, related_name="games_modified", editable=False, null=True, verbose_name=_("modified by")
    )

    played_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("played at"),
        help_text=_("Time when the game was played")
    )

    table = models.ForeignKey(Table, blank=True, null=True, related_name="games", verbose_name=_("table"))

    class Meta:
        ordering = ['-played_at']

    def __str__(self):
        return " - ".join(map(str, self.teams.all()))


class Team(models.Model):
    UNKNOWN = 0
    RED = 1
    BLUE = 2
    SIDE_CHOICES = (
        (UNKNOWN, _("Unknown")),
        (RED, _("Red")),
        (BLUE, _("Blue")),
    )
    side = models.IntegerField(db_index=True, choices=SIDE_CHOICES, default=UNKNOWN, verbose_name=_("side"))

    game = models.ForeignKey(Game, related_name="teams", on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        verbose_name=_("score"),
        help_text=_("Team's score in the game"),
        validators=[MaxValueValidator(limit_value=10)]
    )
    players = models.ManyToManyField(User)

    def __str__(self):
        return "%s (%s)" % (
            self.score,
            ", ".join(map(str, self.players.all()))
        )
