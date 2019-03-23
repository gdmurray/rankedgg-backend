from rest_framework import serializers
from .models import Operator

class OperatorSelectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'type', 'logo', 'image')
        model = Operator


