# Generated by Django 3.0.8 on 2020-07-20 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20200720_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sticker',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='pic/'),
        ),
    ]