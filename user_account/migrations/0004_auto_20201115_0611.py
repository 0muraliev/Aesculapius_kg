# Generated by Django 3.1.2 on 2020-11-15 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0003_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, choices=[(None, 'Не указан'), ('БК', 'Бишкек'), ('Ош', 'Ош'), ('ДА', 'Джалал-Абад'), ('ТК', 'Токмок'), ('ТС', 'Талас'), ('КЛ', 'Каракол'), ('НН', 'Нарын'), ('БН', 'Баткен')], max_length=2, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[(None, 'Не указан'), ('М', 'Мужчина'), ('Ж', 'Женщина')], max_length=1, verbose_name='Пол'),
        ),
    ]