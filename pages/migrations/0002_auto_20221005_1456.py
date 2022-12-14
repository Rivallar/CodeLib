# Generated by Django 3.2.14 on 2022-10-05 11:56

from django.db import migrations, models
import pages.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discipline',
            name='title',
            field=models.CharField(max_length=250, unique=True, validators=[pages.validators.exclude_slash]),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=250, validators=[pages.validators.exclude_slash]),
        ),
        migrations.AlterField(
            model_name='theme',
            name='title',
            field=models.CharField(max_length=250, validators=[pages.validators.exclude_slash]),
        ),
    ]
