from django.db import models
from rest_framework import serializers


# Register your models here.
class FinanceModel(models.Model):
    date_operation = models.DateField()
    reception = models.IntegerField()
    engagement = models.CharField(max_length=20)
    fournisseur = models.CharField(max_length=20)
    shipment_num = models.CharField(max_length=10, null=True)
    devise = models.CharField(max_length=10)
    receptionnaire = models.CharField(max_length=20)
    mt_engagement = models.FloatField()
    objet = models.CharField(max_length=20)
    mt_reception = models.FloatField()


class FinanceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceModel
        fields = "__all__"
