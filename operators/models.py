from django.db import models
from ranked.constants import OPERATOR_TYPE_CHOICES


# Create your models here.
class Operator(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(choices=OPERATOR_TYPE_CHOICES, max_length=24)
    logo = models.CharField(max_length=256, blank=True)
    image = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name
