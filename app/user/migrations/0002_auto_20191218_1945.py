# Generated by Django 2.2.3 on 2019-12-18 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Admin'),
        ),
        migrations.AlterField(
            model_name='user',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Doctor'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nurse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Nurse'),
        ),
        migrations.AlterField(
            model_name='user',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Patient'),
        ),
    ]
