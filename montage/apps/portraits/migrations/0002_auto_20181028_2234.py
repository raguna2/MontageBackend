# Generated by Django 2.1.2 on 2018-10-28 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portraits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='is_personal',
            field=models.BooleanField(default=True, help_text='\n                  ユーザが独自に作成したものであればTrue,\n                  運営が作成したものならFalse\n                  ', verbose_name='個人的なものか'),
        ),
    ]
