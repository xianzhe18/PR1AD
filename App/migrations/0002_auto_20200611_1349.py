# Generated by Django 2.1.15 on 2020-06-11 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_level',
            field=models.IntegerField(choices=[(0, 'Level1(Manually)'), (1, 'Level2(Automatically)')], default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=255, verbose_name='Phone'),
        ),
    ]