# Generated by Django 3.0.8 on 2020-07-19 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200719_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='sticker',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='static/'),
        ),
        migrations.AlterField(
            model_name='sticker',
            name='body',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='sticker',
            name='head',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='sticker',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
