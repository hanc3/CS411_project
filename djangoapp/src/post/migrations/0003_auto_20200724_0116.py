# Generated by Django 3.0.8 on 2020-07-24 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20200724_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Like',
            field=models.IntegerField(),
        ),
    ]
