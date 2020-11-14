from django.contrib.auth.forms import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField('Номер телефона', blank=True)
    itn = models.CharField('ИНН',
                           unique=True,
                           max_length=14,
                           validators=[
                               RegexValidator(regex='^\d{14}$',
                                              message='ИНН должен состоять из 14 цифр',
                                              code='nomatch')],
                           null=True,
                           blank=True)
    gender = models.CharField('Пол',
                              choices=(
                                  ('М', 'Мужчина'),
                                  ('Ж', 'Женщина')
                              ),
                              max_length=1,
                              blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    city = models.CharField('Город',
                            choices=(
                                ('БК', 'Бишкек'),
                                ('Ош', 'Ош'),
                                ('ДА', 'Джалал-Абад'),
                                ('ТК', 'Токмок'),
                                ('ТС', 'Талас'),
                                ('КЛ', 'Каракол'),
                                ('НН', 'Нарын'),
                                ('БН', 'Баткен'),
                            ),
                            max_length=2,
                            blank=True)
    blood_type = models.CharField('Группа крови', max_length=30, blank=True)
    photo = models.ImageField('Фото', upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Определение сигналов, чтобы модель Profile автоматически обновлялась при создании/изменении данных модели User.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()