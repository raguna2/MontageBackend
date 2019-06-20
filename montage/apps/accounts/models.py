from pathlib import Path
import json
import os

from montage.apps.logging import logger_e
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core import validators
from django.db import models
from portraits.models.questions import Question

import cloudinary
from cloudinary.models import CloudinaryField
import requests
from requests_oauthlib import OAuth1Session

API_KEY = os.environ.get('SOCIAL_AUTH_TWITTER_KEY')
API_SECRET = os.environ.get('SOCIAL_AUTH_TWITTER_SECRET')
USERNAME_VALID_TEXT = 'ユーザー名には半角英数、アンダースコアだけ使えます'
USERNAME_VALIDATOR = validators.RegexValidator(r'^[a-zA-Z0-9_]+$',
                                               USERNAME_VALID_TEXT)


class MontageUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, is_staff, is_superuser,
                     **extra_fields):
        """通常ログインor Adminからのユーザ作成処理"""
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email):
        """Twitter認証時のユーザ作成処理"""
        user = self.model(
            username=username,
            is_staff=False,
            is_superuser=False,
        )
        user.save(using=self._db)
        self.sync_master_questions(user)
        user = self.set_user_params(user)
        return user

    def sync_master_questions(self, user):
        # 公式が作った質問のみを抽出
        master_questions = Question.objects.filter(is_personal=False)

        # マスタ質問と作成するユーザを紐付ける
        for q in master_questions:
            q.user.add(user)
            q.save()

    def set_user_params(self, user):
        # user情報を取得する場合
        twitter_api = OAuth1Session(API_KEY, API_SECRET)
        username = user.username
        res = twitter_api.get("=".join([
                'https://api.twitter.com/1.1/users/show.json?screen_name',
                username
        ]))
        res = json.loads(res.text)
        user.display_name = res['name']
        # 画像をcloudinaryに保存
        uploaded = self.upload_profile_img(res)
        user.profile_image = uploaded['secure_url']
        user.save(using=self._db)
        return user

    def upload_profile_img(self, res):
        """Twitterのプロフィール画像をcloudinaryにアップロードする

        Parameters
        ---------------
        res: Json
            TwitterAPIから取得したユーザ情報(JSON形式)

        Returns
        --------------
        uploaded: Dict[str]
            cloudinaryに保管された画像の情報

            主要なものは下記

            - public_id

            - width

            - height

            - format: ファイル形式(jpg)

            - resource_type: image

            - created_at: 作成日時

            - secure_url: 画像のURL(https)

        """
        base_image_url = res['profile_image_url'].rsplit('_', 1)[0]
        image_url_square = base_image_url + '_400x400' + '.jpeg'
        r = requests.get(image_url_square, stream=True)
        folder = os.environ.get('CLOUDINARY_UPLOAD_FOLDER')
        uploaded = cloudinary.uploader.upload(r.content, folder=folder)
        return uploaded

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True,
                                 **extra_fields)


class MontageUser(AbstractBaseUser, PermissionsMixin):
    objects = MontageUserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    # 下記に記載したものがcreatesuperuser実行時に効かれる
    REQUIRED_FIELDS = []
    username = models.CharField(
        'ユーザ名',
        max_length=30,
        unique=True,
        help_text='@で始まるユーザ名',
        validators=[validators.MinLengthValidator(3), USERNAME_VALIDATOR],
        error_messages={
            'unique': "すでに存在しているユーザ名です",
            'min': "名前が短すぎます"
        },
    )
    is_staff = models.BooleanField(
        'スタッフか?', help_text='is_staff', default=False)
    is_superuser = models.BooleanField(
        '管理者か?', help_text='is_superuser', default=False)
    display_name = models.CharField(
        'プロフィール名', help_text='30文字以内', max_length=30, blank=True)
    email = models.EmailField(
        'メールアドレス',
        help_text='255字以内.空文字可',
        max_length=255,
        unique=False,
        blank=True)
    date_of_birth = models.DateField(
        '誕生日', help_text='%yy-%MM-%dd形式.空白可', null=True, blank=True)
    mail_confirmed = models.BooleanField(
        "メールアドレスが確認済みか",
        help_text="確認済みの場合True",
        default=False,
    )
    first_name = models.CharField(
        '名字', help_text='first_name', max_length=30, default='', blank=True)
    last_name = models.CharField(
        '下の名前', help_text='last_name', max_length=30, default='', blank=True)
    is_active = models.BooleanField(
        '退会していないか?', help_text='is_active', default=True)
    created_date = models.DateTimeField(
        '登録日時', help_text='created_date', auto_now_add=True)
    modified_date = models.DateTimeField(
        '更新日時', help_text='modified_date', auto_now=True)
    profile_image = models.ImageField(
        'profile_image', help_text='プロフィール画像', blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(MontageUser, self).save(*args, **kwargs)

    @property
    def as_atsign(self):
        """@{username}として表示"""
        username = self.username
        return f'@{username}'

    def get_full_name(self):
        """フルネームを返す"""
        first_name = self.first_name
        last_name = self.last_name
        full_name = f'{first_name}{last_name}'
        return full_name.strip()

    def get_short_name(self):
        """名字だけ返す"""
        return self.first_name
