# Generated by Django 3.0.8 on 2020-07-19 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200719_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sticker',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]