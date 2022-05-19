from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

NULLABLE = {'blank': True, 'null': True}

class Skills(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Наименование')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'скилл'
        verbose_name_plural = 'скиллы'
        ordering = ('-name',)


class HhUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='Аватар')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', default=18)
    skills = models.ManyToManyField(Skills, verbose_name='Скиллы', blank=True)


class HhUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    OTHERS = 'O'

    GENDERS = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
        (OTHERS, 'Иное'),
    )

    user = models.OneToOneField(HhUser, null=False, unique=True, on_delete=models.CASCADE, db_index=True)
    tagline = models.CharField(max_length=128, verbose_name='Теги', blank=True)
    about_me = models.TextField(verbose_name='Обо мне')
    gender = models.CharField(choices=GENDERS, default=OTHERS, verbose_name='Пол', max_length=1)
    # skills = models.ManyToManyField(Skills, verbose_name='Скиллы', blank=True)

    @receiver(post_save, sender=HhUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            HhUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=HhUser)
    def update_user_profile(sender, instance, created, **kwargs):
        instance.hhuserprofile.save()
