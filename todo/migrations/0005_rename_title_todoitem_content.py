# Generated by Django 3.2.11 on 2022-06-20 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_alter_todoitem_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todoitem',
            old_name='title',
            new_name='content',
        ),
    ]
