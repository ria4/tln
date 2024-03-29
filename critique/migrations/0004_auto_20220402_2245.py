# Generated by Django 3.2.11 on 2022-04-02 20:45

from django.db import migrations, models
from django.db.models import Q
import django.db.models.deletion


def populate_cinema_fields(apps, schema_editor):
    Cinema = apps.get_model('critique', 'Cinema')
    Seance = apps.get_model('critique', 'Seance')
    seances_to_edit = []
    for seance in Seance.objects.order_by('date'):
        cinema_origin = seance.cinema
        cinemas = Cinema.objects.filter(Q(name_short=cinema_origin)|Q(name=cinema_origin))
        if len(cinemas) == 1:
            seance.cinema_pk = cinemas[0]
            seance.save()
            print(seance)
        else:
            seances_to_edit.append(seance)
    print('#####################')
    for seance in seances_to_edit:
        print(seance)


class Migration(migrations.Migration):

    dependencies = [
        ('critique', '0003_auto_20220329_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='seance',
            name='cinema_name_long_override',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='seance',
            name='cinema_name_short_override',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='seance',
            name='cinema_pk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='seances', related_query_name='seance', to='critique.cinema'),
        ),
        migrations.RunPython(populate_cinema_fields),
        migrations.AddField(
            model_name='seance',
            name='cinema_unsure',
            field=models.BooleanField(default=False),
        ),
    ]
