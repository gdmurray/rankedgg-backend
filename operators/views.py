from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.http.response import JsonResponse
from .serializers import OperatorSelectSerializer
from .models import Operator
from django.db.models import Count, Q


# Create your views here.

class OperatorDropdownOptions(ListAPIView):
    serializer_class = OperatorSelectSerializer
    queryset = Operator.objects.all()


class OperatorListView(APIView):
    def get(self, request, *args, **kwargs):
        region = request.GET.get("region")
        if region:
            qs = list(Operator.objects.values('name', 'type', 'logo', 'image').annotate(
                report_count=Count('report', filter=Q(report__region=region))).order_by('-report_count'))
        else:
            qs = list(Operator.objects.values('name', 'type', 'logo', 'image').annotate(
                report_count=Count('report')).order_by('-report_count'))
        return JsonResponse(data=qs, safe=False)
