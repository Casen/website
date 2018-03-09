from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Game(models.Model):
    ai_starts = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(default=None)
    winner = models.IntegerField(
        default=None,
        validators=[MaxValueValidator(1), MinValueValidator(2)]
    )



class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.IntegerField(
        default=None,
        validators=[MaxValueValidator(1), MinValueValidator(2)]
    )
    location = models.IntegerField(
        default=None,
        validators=[MaxValueValidator(63), MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
