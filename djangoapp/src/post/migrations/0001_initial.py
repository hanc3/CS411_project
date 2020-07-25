# Generated by Django 3.0.8 on 2020-07-24 20:11

from django.db import migrations, models
import django.db.models.deletion
from django_add_default_value import AddDefaultValue


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appUser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='post',
            fields=[
                ('Post_id', models.AutoField(primary_key=True, serialize=False)),
                ('Pub_date', models.DateTimeField(verbose_name='data posted')),
                ('Apartment', models.CharField(max_length=60)),
                ('Post_title', models.TextField()),
                ('Description', models.TextField(blank=True)),
                ('Move_in_date', models.DateField()),
                ('Move_out_date', models.DateField()),
                ('Duration', models.IntegerField()),
                ('Price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('Exist', models.BooleanField(default=True)),
                ('Bedroom', models.IntegerField()),
                ('Bathroom', models.IntegerField()),
                ('Likes', models.IntegerField()),
                ('Username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appUser.appUser')),
            ],
        ),
        AddDefaultValue(
            model_name='post',
            name='Likes',
            value=0
        ),
        AddDefaultValue(
            model_name='post',
            name='Exist',
            value=True
        )
    ]