# Generated by Django 2.1.15 on 2020-06-15 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_auto_20200615_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign_report',
            name='campaign_id',
        ),
        migrations.RemoveField(
            model_name='useradmin_control',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='campaign_report',
        ),
        migrations.DeleteModel(
            name='control_campaigns',
        ),
        migrations.DeleteModel(
            name='useradmin_control',
        ),
    ]