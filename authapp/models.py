from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

NULLABLE = {'blank': True, 'null': True}


class Skills(models.Model):
    """Модель навыков"""
    name = models.CharField(max_length=64, unique=True, verbose_name='Наименование')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'скилл'
        verbose_name_plural = 'скиллы'
        ordering = ('name',)


class HhUser(AbstractUser):
    """Профиль пользователя"""
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='Аватар')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', default=18)
    skills = models.ManyToManyField(Skills, verbose_name='Скиллы', blank=True)


class HhUserProfile(models.Model):
    """Дополнительна информация из профиля пользователя"""
    MALE = 'M'
    FEMALE = 'W'
    OTHERS = 'O'

    GENDERS = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
        (OTHERS, 'Иное'),
    )

    patronymic = models.CharField(max_length=150, verbose_name='Отчество', **NULLABLE)
    user = models.OneToOneField(HhUser, null=False, unique=True, on_delete=models.CASCADE, db_index=True)
    # по-хорошему, языки и хобби так же как и скиллы должны быть ManyToManyField, но не стал плодить сущности
    languages = models.CharField(max_length=200, verbose_name='Языки', **NULLABLE)
    hobbies = models.CharField(max_length=200, verbose_name='Хобби', **NULLABLE)
    about_me = models.TextField(verbose_name='Обо мне', **NULLABLE)
    gender = models.CharField(choices=GENDERS, default=OTHERS, verbose_name='Пол', max_length=1)


    @receiver(post_save, sender=HhUser)
    def create_user_profile(sender, instance, created, **kwargs):
        """Сигнал на создание профиля"""
        if created:
            HhUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=HhUser)
    def update_user_profile(sender, instance, created, **kwargs):
        """Сигнал на обновление профиля"""
        instance.hhuserprofile.save()
