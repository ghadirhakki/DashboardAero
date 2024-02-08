from django.db import models


# Register your models here.
class FinanceModel(models.Model):
    date_operation = models.DateField()
    reception = models.IntegerField(primary_key=True)
    engagement = models.CharField(max_length=20)
    fournisseur = models.CharField(max_length=20)
    shipment_num = models.CharField(max_length=10, null=True)
    devise = models.CharField(max_length=10)
    receptionnaire = models.CharField(max_length=20)
    mt_engagement = models.FloatField()
    objet = models.CharField(max_length=20)
    mt_reception = models.FloatField()
