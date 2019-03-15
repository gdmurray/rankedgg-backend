from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import OperatorSelectSerializer
from .models import Operator


# Create your views here.

class OperatorDropdownOptions(ListAPIView):
    serializer_class = OperatorSelectSerializer
    queryset = Operator.objects.all()
