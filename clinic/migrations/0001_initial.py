# Generated by Django 3.1.3 on 2020-11-22 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[(None, 'Оценить'), ('5', 'Отлично'), ('4', 'Хорошо'), ('3', 'Нормально'), ('2', 'Плохо'), ('1', 'Ужасно')], max_length=1, verbose_name='Оценка')),
                ('title', models.CharField(blank=True, max_length=50, verbose_name='Название')),
                ('text', models.TextField(blank=True, verbose_name='Отзыв(по желанию)')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='user_account.clinic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('user', 'clinic'), name='unique_review'),
        ),
    ]
