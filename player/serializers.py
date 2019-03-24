from rest_framework import serializers
from .models import Player
from .tasks import update_ranked_data
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from operators.serializers import OperatorSelectSerializer


class BasePlayerSerializer(serializers.ModelSerializer):
    """
    The base serializer for players, includes image method
    Default current rank/mmr fetch behaviour checks if it needs updating
    then it will offset to a queued task
    """
    image = serializers.SerializerMethodField()
    current_rank = serializers.SerializerMethodField()
    current_mmr = serializers.SerializerMethodField()
    update = serializers.SerializerMethodField()

    def get_update(self, obj):
        if 'from_task' not in self.context:
            if obj.needs_metadata_fetch():
                update_ranked_data.apply_async((obj.id, self.context['region']))
                return True
            return False
        else:
            return False

    def get_current_mmr(self, obj):
        metadata = obj.get_metadata()
        if self.context['region'] == "NA":
            return metadata.NA_mmr
        elif self.context['region'] == "EU":
            return metadata.EU_mmr
        elif self.context['region'] == "AS":
            return metadata.AS_mmr
        else:
            return metadata.current_mmr

    def get_current_rank(self, obj):
        metadata = obj.get_metadata()
        if self.context['region'] == "NA":
            return metadata.NA_rank
        elif self.context['region'] == "EU":
            return metadata.EU_rank
        elif self.context['region'] == "AS":
            return metadata.AS_rank
        else:
            return metadata.current_rank

    def get_image(self, obj):
        return obj.player_image()

    class Meta:
        model = Player


class BasePlayerSerializerOperatorMixin(BasePlayerSerializer):
    attacker = serializers.SerializerMethodField()
    defender = serializers.SerializerMethodField()

    def get_attacker(self, obj):
        operator = obj.recommended_attacker(region=self.context['region'])
        if operator:
            return OperatorSelectSerializer(operator, many=False).data
        return None

    def get_defender(self, obj):
        operator = obj.recommended_defender(region=self.context['region'])
        if operator:
            return OperatorSelectSerializer(operator, many=False).data
        return None


class PlayerLeaderBoardSerializer(BasePlayerSerializerOperatorMixin):
    report_count = serializers.IntegerField(read_only=True)
    ranking = serializers.IntegerField(read_only=True)

    class Meta:
        model = Player
        fields = (
            'id', 'username', 'image', 'current_rank', 'report_count', 'ranking', 'update', 'attacker', 'defender')


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 25
    max_page_size = 500


class PageNumberPaginationDataOnly(PageNumberPagination):
    max_page_size = 1000
    page_size = 1000

    def get_paginated_response(self, data):
        return Response(data)
# TODO: Add celery for async metadata scanning of players
# TODO: Add Profile for people
# TODO: Add Most Wanted
# TODO: DEPLOY TO NETLIFY + HEROKU/DIGITALOCEAN??
# TODO: Add About, contact me, remove services?
