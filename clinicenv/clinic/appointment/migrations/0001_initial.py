# Generated by Django 5.0 on 2024-01-15 18:32

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RomaninHolidays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnavailableDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('reason', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WorkingSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('interval', models.PositiveIntegerField(help_text='Enter the interval between appointments in minutes.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(60)])),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('age', models.PositiveIntegerField()),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('appointment_date', models.DateField()),
                ('status', models.CharField(choices=[('', '---------'), ('accepted', 'Accept'), ('refused', 'Refuse')], default='', max_length=10)),
                ('appointment_time', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.availabletime')),
            ],
        ),
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.UniqueConstraint(fields=('appointment_date', 'appointment_time'), name='date_time_uk'),
        ),
    ]
