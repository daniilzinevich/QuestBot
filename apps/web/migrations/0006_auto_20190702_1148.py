# Generated by Django 2.0 on 2019-07-02 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20180124_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='no_links_preview',
            field=models.NullBooleanField(verbose_name='Disable links preview'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='no_notifications',
            field=models.NullBooleanField(verbose_name='Disable notifications'),
        ),
    ]
