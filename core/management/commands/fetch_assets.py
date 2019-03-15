from django.core.management.base import BaseCommand
from operators.models import Operator
from bs4 import BeautifulSoup
import requests


class Command(BaseCommand):
    help = 'Help Text'

    def handle(self, *args, **options):
        operators = Operator.objects.all()
        for operator in operators:
            print(f"Scanning Page for {operator.name}")
            url = f"https://rainbow6.ubisoft.com/siege/en-ca/game-info/operators/{operator.name.lower()}/index.aspx"

            r = requests.get(url)
            soup = BeautifulSoup(r.content)

            logo_content = soup.find("span", {"class": "op-badge"})
            if logo_content:
                logo_url = logo_content.find("img")['src']
            else:
                logo_content = soup.find("span", {"class": "ico"})
                logo_url = logo_content.find("img")['src']

            image_content = soup.find("div", {"class": "operator-header-pic"})
            if image_content:
                image_url = image_content.find("img")['src']
            else:
                image_content = soup.find("div", {"class": "operator-overview-pic"})
                image_url = image_content.find("img")['src']

            with open(f'assets/{operator.name.lower()}.png', 'wb') as f:
                r_logo = requests.get(logo_url, allow_redirects=True)
                f.write(r_logo.content)

            with open(f'assets/{operator.name.lower()}_full.png', 'wb') as f:
                r_image = requests.get(image_url, allow_redirects=True)
                f.write(r_image.content)

            operator.logo = f'{operator.name.lower()}.png'
            operator.image = f'{operator.name.lower()}._full.png'
            operator.save()
