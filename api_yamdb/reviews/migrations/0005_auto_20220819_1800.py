# Generated by Django 2.2.16 on 2022-08-19 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220819_1748'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'default_related_name': 'titles', 'ordering': ('name',), 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
    ]