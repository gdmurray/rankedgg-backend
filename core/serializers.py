from rest_framework import serializers
from .models import Player, PlayerMeta
from ranked.constants import METADATA_REFRESH_HOURS
from operators.serializers import OperatorSelectSerializer


class BasePlayerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.player_image()

    class Meta:
        model = Player


class R6TabUserSerializer(BasePlayerSerializer):
    current_rank = serializers.SerializerMethodField()

    def get_current_rank(self, obj):
        if self.context['region'] == "NA":
            return self.context['metadata'].NA_rank
        elif self.context['region'] == "EU":
            return self.context['metadata'].EU_rank
        elif self.context['region'] == "AS":
            return self.context['metadata'].AS_rank
        else:
            return obj.current_rank

    class Meta:
        model = Player
        fields = ('username', 'current_rank', 'image')


class SearchPlayerSerializer(BasePlayerSerializer):
    current_rank = serializers.SerializerMethodField()
    current_mmr = serializers.SerializerMethodField()
    attacker = serializers.SerializerMethodField()
    defender = serializers.SerializerMethodField()

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

    def get_current_mmr(self, obj):
        metadata = obj.fetch_metadata()
        if self.context['region'] == "NA":
            return metadata.NA_mmr
        elif self.context['region'] == "EU":
            return metadata.EU_mmr
        elif self.context['region'] == "AS":
            return metadata.AS_mmr
        else:
            return obj.current_mmr

    def get_attacker(self, obj):
        operator = obj.recommended_attacker()
        if operator:
            return OperatorSelectSerializer(operator, many=False).data
        return None

    def get_defender(self, obj):
        operator = obj.recommended_defender()
        if operator:
            return OperatorSelectSerializer(operator, many=False).data
        return None

    class Meta:
        model = Player
        fields = ('username', 'current_rank', 'image',
                  'current_level', 'current_mmr', 'current_rank',
                  'attacker', 'defender')

# TODO: Query By Region, add a specific region MMR to the Search
# TODO: Add celery for async metadata scanning of players
# TODO: split the CSS up
# TODO: Add Profile for people
# TODO: add Homepage
# TODO: Add Most Wanted
# TODO: DEPLOY TO NETLIFY + HEROKU/DIGITALOCEAN??
# TODO: Add About, contact me, remove services?
# TODO: Deploy to Netlify => ranked.wtf :)
