# Generated by Django 3.2.14 on 2022-07-14 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0016_auto_20220714_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discipline',
            name='slug',
            field=models.SlugField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='theme',
            name='slug',
            field=models.SlugField(blank=True, max_length=250),
        ),
    ]