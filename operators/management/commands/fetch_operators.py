from django.core.management.base import BaseCommand
from operators.models import Operator
from ranked.constants import ATTACKER, DEFENDER
from bs4 import BeautifulSoup
import requests


class Command(BaseCommand):
    help = 'Help Text'

    def handle(self, *args, **options):
        url = "https://rainbow6.ubisoft.com/siege/en-ca/game-info/operators.aspx"

        r = requests.get(url)
        soup = BeautifulSoup(r.content)

        attackers = soup.findAll("div", {"class": "attacker"})
        for atk in attackers:
            name = atk['data-key']
            print("for name ", name)
            operator, created = Operator.objects.get_or_create(name=name.capitalize(), type=ATTACKER)
            operator.image = f"{name}_full.png"
            operator.logo = f"{name}.png"
            operator.save()
        defenders = soup.findAll("div", {"class": "defender"})
        for defender in defenders:
            name = defender['data-key']
            print("for name ", name)
            operator, created = Operator.objects.get_or_create(name=name.capitalize(), type=DEFENDER)
            operator.image = f"{name}_full.png"
            operator.logo = f"{name}.png"
            operator.save()