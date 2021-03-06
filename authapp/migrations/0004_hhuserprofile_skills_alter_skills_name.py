# Generated by Django 4.0.3 on 2022-05-19 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_skills_remove_hhuser_activate_key_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hhuserprofile',
            name='skills',
            field=models.ManyToManyField(blank=True, null=True, to='authapp.skills', verbose_name='Скиллы'),
        ),
        migrations.AlterField(
            model_name='skills',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='Наименование'),
        ),
    ]
