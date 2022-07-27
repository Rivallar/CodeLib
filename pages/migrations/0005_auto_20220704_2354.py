# Generated by Django 3.2.14 on 2022-07-04 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('pages', '0004_auto_20220704_2317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='parent',
        ),
        migrations.AddField(
            model_name='theme',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ('discipline', 'theme')}, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='theme',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]