# Generated by Django 4.0.10 on 2024-02-18 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0003_projectmodel_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmodel',
            name='cost',
            field=models.IntegerField(null=True),
        ),
    ]