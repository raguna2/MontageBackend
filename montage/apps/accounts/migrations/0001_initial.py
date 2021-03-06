# Generated by Django 2.1.8 on 2020-02-17 14:09

import apps.accounts.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MontageUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'min': '名前が短すぎます', 'unique': 'すでに存在しているユーザ名です'}, help_text='@で始まるユーザ名', max_length=30, unique=True, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.RegexValidator('^[a-zA-Z0-9_]+$', 'ユーザー名には半角英数、アンダースコアだけ使えます')], verbose_name='ユーザ名')),
                ('identifier_id', models.CharField(help_text='auth0のユーザID', max_length=30, unique=True, verbose_name='ユーザID')),
                ('is_staff', models.BooleanField(default=False, help_text='is_staff', verbose_name='スタッフか?')),
                ('is_superuser', models.BooleanField(default=False, help_text='is_superuser', verbose_name='管理者か?')),
                ('display_name', models.CharField(error_messages={'max': '名前が長すぎます'}, help_text='30文字以内', max_length=30, verbose_name='プロフィール名')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='created_date', verbose_name='登録日時')),
                ('modified_date', models.DateTimeField(auto_now=True, help_text='modified_date', verbose_name='更新日時')),
                ('profile_img_url', models.URLField(blank=True, help_text='プロフィール画像のURL', null=True, verbose_name='profile_img_url')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', apps.accounts.models.MontageUserManager()),
            ],
        ),
    ]
