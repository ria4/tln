# Generated by Django 3.2.11 on 2022-05-28 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('critique', '0012_alter_oeuvrespan_date_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='oeuvre',
            name='artists',
            field=models.ManyToManyField(related_name='liholihnl', related_query_name='lihyolkihnol', to='critique.Artiste'),
        ),
        migrations.AddField(
            model_name='oeuvre',
            name='image_url',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.AddField(
            model_name='oeuvre',
            name='imdb_id',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='oeuvre',
            name='mtype',
            field=models.CharField(choices=[('film', 'Film'), ('serie', 'Série'), ('album', 'Album'), ('jeu', 'Jeu'), ('livre', 'Livre'), ('bd', 'BD')], default='film', max_length=5),
        ),
        migrations.AddField(
            model_name='oeuvre',
            name='title_alt',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='oeuvre',
            name='title_vf',
            field=models.CharField(db_index=True, default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='oeuvre',
            name='title_vo',
            field=models.CharField(blank=True, db_index=True, max_length=200),
        ),
        migrations.AddField(
            model_name='oeuvre',
            name='year',
            field=models.SmallIntegerField(db_index=True, default=0),
            preserve_default=False,
        ),
    ]
