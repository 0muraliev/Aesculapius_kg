# Generated by Django 3.1.3 on 2020-11-22 14:22

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import location_field.models.plain
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_clinic', models.BooleanField(default=False, verbose_name='clinic status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125, verbose_name='Название')),
                ('slug', models.SlugField(max_length=125, unique=True)),
                ('information', models.TextField(blank=True, verbose_name='Основная информация')),
                ('image', models.ImageField(blank=True, null=True, upload_to='clinics', verbose_name='Изображение')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('location', location_field.models.plain.PlainLocationField(max_length=63)),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Связаться с нами')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
                ('slug', models.SlugField(max_length=125, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Номер телефона')),
                ('itn', models.CharField(blank=True, max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='ИНН должен состоять из 14 цифр', regex='^\\d{14}$')], verbose_name='ИНН')),
                ('gender', models.CharField(blank=True, choices=[(None, 'Не указан'), ('М', 'Мужчина'), ('Ж', 'Женщина')], max_length=1, verbose_name='Пол')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('city', models.CharField(blank=True, choices=[(None, 'Не указан'), ('БК', 'Бишкек'), ('Ош', 'Ош'), ('ДА', 'Джалал-Абад'), ('ТК', 'Токмок'), ('ТС', 'Талас'), ('КЛ', 'Каракол'), ('НН', 'Нарын'), ('БН', 'Баткен')], max_length=2, verbose_name='Город')),
                ('blood_type', models.CharField(blank=True, max_length=30, verbose_name='Группа крови')),
                ('photo', models.ImageField(blank=True, upload_to='users/%Y/%m/%d', verbose_name='Фото')),
                ('favorite_clinic', models.ManyToManyField(blank=True, related_name='favorite_clinics', to='user_account.Clinic', verbose_name='Избранные клиники')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='clinic',
            name='medical_departments',
            field=models.ManyToManyField(related_name='clinics', to='user_account.MedicalDepartment'),
        ),
    ]
