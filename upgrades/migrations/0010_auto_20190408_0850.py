# Generated by Django 2.1.7 on 2019-04-08 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upgrades', '0009_auto_20190408_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upgrades',
            name='exp_for_update',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='upgrades',
            name='gold_for_sale',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='upgrades',
            name='gold_for_update',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
