# Generated by Django 4.0.10 on 2024-02-10 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ProjectModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=20)),
                ('name', models.CharField(blank=True, max_length=80)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TaskModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('phase_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planning.phasemodel')),
                ('project_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planning.projectmodel')),
            ],
        ),
        migrations.RemoveField(
            model_name='task',
            name='phase_related',
        ),
        migrations.RemoveField(
            model_name='task',
            name='project_related',
        ),
        migrations.DeleteModel(
            name='Phase',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.AddField(
            model_name='phasemodel',
            name='project_related',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planning.projectmodel'),
        ),
    ]
