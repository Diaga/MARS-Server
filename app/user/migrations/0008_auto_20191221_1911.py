# Generated by Django 2.2.9 on 2019-12-21 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20191221_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, default='male', max_length=255),
        ),
    ]
