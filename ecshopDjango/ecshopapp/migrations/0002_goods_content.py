# Generated by Django 4.2.11 on 2024-03-21 04:07

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ecshopapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='content',
            field=mdeditor.fields.MDTextField(default=None, verbose_name='商品詳細'),
        ),
    ]
