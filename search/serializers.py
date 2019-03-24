from rest_framework import serializers

from player.serializers import BasePlayerSerializer, BasePlayerSerializerOperatorMixin
from player.models import Player


class SearchPlayerSerializer(BasePlayerSerializerOperatorMixin):
    class Meta:
        model = Player
        fields = ('username', 'current_rank', 'image',
                  'current_level', 'current_mmr', 'current_rank',
                  'attacker', 'defender', 'update')


class R6TabUserSerializer(BasePlayerSerializer):
    """
    Overrides get_current_rank because fetching 1 metadata with API call is not taxing
    """
    current_rank = serializers.SerializerMethodField()

    def get_current_rank(self, obj):
        if self.context['region'] == "NA" and self.context['metadata'].NA_rank:
            return self.context['metadata'].NA_rank

        elif self.context['region'] == "EU" and self.context['metadata'].EU_rank:
            return self.context['metadata'].EU_rank

        elif self.context['region'] == "AS" and self.context['metadata'].AS_rank:
            return self.context['metadata'].AS_rank

        else:
            return self.context['metadata'].current_rank

    class Meta:
        model = Player
        fields = ('username', 'current_rank', 'image')
