from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import FinanceModel, FinanceModelSerializer
from rest_framework.response import Response

# Create your views here.


@api_view()
def financial_records_list(request):
    if request.method == "GET":
        records = FinanceModel.objects.all()
        serializer = FinanceModelSerializer(records, many=True)
        return Response(serializer.data)


@api_view()
def financial_records_per_proj(request, ref):
    if request.method == "GET":
        records = FinanceModel.objects.filter(engagement=ref)
        serializer = FinanceModelSerializer(records, many=True)
        return Response(serializer.data)
