# Generated by Django 3.1.2 on 2020-10-17 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
            ],
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125, verbose_name='Название')),
                ('information', models.TextField(blank=True, verbose_name='Основная информация')),
                ('address', models.CharField(max_length=125, verbose_name='Адрес')),
                ('contact', models.IntegerField(max_length=125, verbose_name='Связаться с нами')),
                ('medical_departments', models.ManyToManyField(to='clinic.MedicalDepartment')),
            ],
        ),
    ]