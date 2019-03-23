from rest_framework import serializers
from .models import Player
from rest_framework.pagination import PageNumberPagination


class BasePlayerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.player_image()

    class Meta:
        model = Player


class PlayerLeaderBoardSerializer(BasePlayerSerializer):
    report_count = serializers.IntegerField(read_only=True)
    ranking = serializers.IntegerField(read_only=True)
    current_rank = serializers.SerializerMethodField()

    def get_current_rank(self, obj):
        metadata = obj.fetch_metadata()
        if self.context['region'] == "NA":
            return metadata.NA_rank
        elif self.context['region'] == "EU":
            return metadata.EU_rank
        elif self.context['region'] == "AS":
            return metadata.AS_rank
        else:
            return obj.current_rank

    class Meta:
        model = Player
        fields = ('username', 'image', 'current_rank', 'report_count', 'ranking')


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 25
    max_page_size = 500

# TODO: Query By Region, add a specific region MMR to the Search
# TODO: Add celery for async metadata scanning of players
# TODO: split the CSS up
# TODO: Add Profile for people
# TODO: add Homepage
# TODO: Add Most Wanted
# TODO: DEPLOY TO NETLIFY + HEROKU/DIGITALOCEAN??
# TODO: Add About, contact me, remove services?
# TODO: Deploy to Netlify => ranked.wtf :)
