# Generated by Django 2.2.9 on 2019-12-21 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20191218_2017'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'default_related_name': 'users'},
        ),
        migrations.AlterField(
            model_name='user',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='user.Admin'),
        ),
        migrations.AlterField(
            model_name='user',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='user.Doctor'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nurse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='user.Nurse'),
        ),
        migrations.AlterField(
            model_name='user',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='user.Patient'),
        ),
    ]
