# Generated by Django 4.0.4 on 2022-06-20 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='created_time',
            field=models.DateField(default='2000-08-09'),
        ),
    ]
