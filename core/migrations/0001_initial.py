# Generated by Django 5.2.1 on 2025-05-20 05:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lancamento',
            fields=[
                ('id_lancamento', models.AutoField(primary_key=True, serialize=False)),
                ('data_hora_inicio', models.DateTimeField()),
                ('data_hora_fim', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Telemetria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField()),
                ('aceleracao_x', models.FloatField()),
                ('aceleracao_y', models.FloatField()),
                ('aceleracao_z', models.FloatField()),
                ('vel_angular_x', models.FloatField()),
                ('vel_angular_y', models.FloatField()),
                ('vel_angular_z', models.FloatField()),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('altitude', models.FloatField(blank=True, null=True)),
                ('vel_sob_solo', models.FloatField(blank=True, null=True)),
                ('shunt_voltage', models.FloatField(blank=True, null=True)),
                ('bus_voltage', models.FloatField(blank=True, null=True)),
                ('current_mA', models.FloatField(blank=True, null=True)),
                ('power_mW', models.FloatField(blank=True, null=True)),
                ('lancamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telemetrias', to='core.lancamento')),
            ],
            options={
                'ordering': ['data_hora'],
            },
        ),
    ]
