# Generated by Django 4.0.10 on 2024-02-08 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='type',
            field=models.CharField(choices=[('BudgetFile', 'Budget File'), ('PlanningFile', 'Planning File')], max_length=20),
        ),
    ]
