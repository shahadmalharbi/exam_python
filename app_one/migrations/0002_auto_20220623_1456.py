# Generated by Django 2.2.4 on 2022-06-23 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='items',
        ),
        migrations.AddField(
            model_name='item',
            name='users',
            field=models.ManyToManyField(related_name='items', to='app_one.User'),
        ),
    ]
