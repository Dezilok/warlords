# Generated by Django 2.1.7 on 2019-04-08 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upgrades', '0010_auto_20190408_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upgrades',
            name='icon',
            field=models.ImageField(blank=True, upload_to='upgrades/images/'),
        ),
    ]
