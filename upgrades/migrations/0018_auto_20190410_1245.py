# Generated by Django 2.1.7 on 2019-04-10 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upgrades', '0017_auto_20190410_1047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(related_name='Books', to='upgrades.Author'),
        ),
    ]