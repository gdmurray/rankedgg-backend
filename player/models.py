from django.db import models
from django.db.models import Count
from operators.models import Operator
from django.dispatch import receiver
from django.db.models.signals import post_save
from ranked.constants import REGION_CHOICES, GLOBAL, METADATA_REFRESH_HOURS, ATTACKER, DEFENDER
import datetime
from search.R6TabAPI import R6TabAPI
from django.utils import timezone
from ranked.functions import timedelta_now_hours


# Create your models here.

class Player(models.Model):
    p_id = models.CharField(max_length=255)
    p_user = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    # image = models.CharField(max_length=512, null=True)
    current_level = models.IntegerField(null=True)
    current_mmr = models.IntegerField(null=True)
    current_rank = models.IntegerField(null=True)

    last_queried = models.DateTimeField(null=True)

    def player_image(self):
        return f"https://ubisoft-avatars.akamaized.net/{self.p_user}/default_146_146.png"

    def __str__(self):
        return self.username

    def recommend(self, reports):
        if reports:
            operators = reports.values_list('operator').annotate(report_count=Count('operator')).order_by(
                '-report_count')
            print(operators)
            if operators.count() >= 2:
                top = operators[0]
                second = operators[1]
                if top[1] == second[1]:
                    print("Same Ban Rate, Solve with all states")
                    operator = Operator.objects.get(id=top[0])
                    return operator
                elif top[1] > second[1]:
                    print("top is top")
                    operator = Operator.objects.get(id=top[0])
                    return operator
            elif operators.count() == 1:
                operator = Operator.objects.get(id=operators[0][0])
                print("only 1 report, return top")
                return operator
        return None

    def recommended_attacker(self):
        reports = Report.objects.filter(player_id=self.id, operator__type=ATTACKER)
        operator = self.recommend(reports)
        return operator

    def recommended_defender(self):
        reports = Report.objects.filter(player_id=self.id, operator__type=DEFENDER)
        operator = self.recommend(reports)
        return operator

    def fetch_metadata(self):
        metadata = PlayerMeta.objects.get(player_id=self.id)

        # Update Metadata if u need to

        if not metadata.last_queried or timedelta_now_hours(metadata.last_queried) > METADATA_REFRESH_HOURS:
            print("Metadata never queried or older than REFRESH threshold")
            fetched_data = R6TabAPI.find_by_id(self.p_id)
            metadata = R6TabAPI.update_meta(metadata, fetched_data)

        return metadata


class PlayerMeta(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    current_mmr = models.IntegerField(null=True)
    current_rank = models.IntegerField(null=True)

    NA_mmr = models.IntegerField(null=True)
    NA_rank = models.IntegerField(null=True)
    EU_mmr = models.IntegerField(null=True)
    EU_rank = models.IntegerField(null=True)
    AS_mmr = models.IntegerField(null=True)
    AS_rank = models.IntegerField(null=True)

    last_queried = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.player.username} metadata"


@receiver(post_save, sender=Player)
def player_created(sender, instance, created, *args, **kwargs):
    """
    Creates blank company metadata object upon company creation
    :param sender:
    :param instance:
    :param created:
    :param args:
    :param kwargs:
    :return:
    """
    if created:
        if not PlayerMeta.objects.filter(player=instance):
            PlayerMeta.objects.create(player=instance)


class Report(models.Model):
    sender_ip = models.GenericIPAddressField()
    player = models.ForeignKey(Player, null=False, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    region = models.CharField(choices=REGION_CHOICES, default=GLOBAL, max_length=10)
    created = models.DateTimeField(null=True, default=timezone.now)

    def __str__(self):
        return f"{self.operator.name} - {self.player.username}"
