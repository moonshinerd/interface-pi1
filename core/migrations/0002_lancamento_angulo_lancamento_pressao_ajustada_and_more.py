# Generated by Django 5.2.1 on 2025-05-25 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lancamento',
            name='angulo',
            field=models.FloatField(default=45.0),
        ),
        migrations.AddField(
            model_name='lancamento',
            name='pressao_ajustada',
            field=models.FloatField(default=53.03),
        ),
        migrations.AddField(
            model_name='lancamento',
            name='pressao_recomendada',
            field=models.FloatField(default=53.03),
        ),
        migrations.AddField(
            model_name='lancamento',
            name='volume_agua',
            field=models.FloatField(default=750.0),
        ),
    ]
