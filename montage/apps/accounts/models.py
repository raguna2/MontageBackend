import json
import os
from pathlib import Path

import cloudinary
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core import validators
from django.db import models

import requests
from montage.apps.logging import logger_d, logger_e
from portraits.models.questions import Question

USERNAME_VALID_TEXT = 'ユーザー名には半角英数、アンダースコアだけ使えます'
USERNAME_VALIDATOR = validators.RegexValidator(r'^[a-zA-Z0-9_]+$', USERNAME_VALID_TEXT)


class MontageUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, identifier_id, password, is_staff, is_superuser,
                     **extra_fields):
        """通常ログインor Adminからのユーザ作成処理"""
        logger_d.info('通常ログインor Adminからのユーザ作成処理')
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(
            username=username,
            identifier_id=identifier_id,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, identifier_id, display_name, profile_img_url=None):
        """Twitter認証時のユーザ作成処理"""
        logger_d.info('Twitter認証時のユーザ作成処理')
        if not profile_img_url:
            profile_img_url = ''
        user = self.model(
            username=username,
            identifier_id=identifier_id,
            display_name=display_name,
            profile_img_url=profile_img_url,
            is_staff=False,
            is_superuser=False,
        )
        user = self.set_picture(user, profile_img_url)
        try:
            user.save(using=self._db)
        except Exception as e:
            logger_e.error('create_userでエラーです')
            logger_e.error(e)

        self.sync_master_questions(user)
        return user

    def sync_master_questions(self, user):
        # 公式が作った質問のみを抽出
        master_questions = Question.objects.filter(is_personal=False)

        # マスタ質問と作成するユーザを紐付ける
        for q in master_questions:
            q.user.add(user)
            q.save()

    def set_picture(self, user, picture):
        # 画像をcloudinaryに保存
        uploaded = self.upload_profile_img(picture)

        if uploaded:
            user.profile_img_url = uploaded['secure_url']
        else:
            user.profile_img_url = None

        return user

    def upload_profile_img(self, picture):
        """Twitterのプロフィール画像をcloudinaryにアップロードする

        Parameters
        ---------------
        picture: str
            小さいサイズのプロフィール画像のURL

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
        image_url_square = picture.replace('_normal', '_400x400')
        uploaded = None

        response = requests.get(image_url_square, stream=True)
        if response.status_code == 200:
            folder = os.environ.get('CLOUDINARY_UPLOAD_FOLDER')
            uploaded = cloudinary.uploader.upload(
                response.content,
                folder=folder,
            )
        else:
            logger_e.error('プロフィール画像取得のレスポンスコードが200ではありません.')

        return uploaded

    def create_superuser(self, username, identifier_id, password, **extra_fields):
        return self._create_user(username, identifier_id, password, True, True,
                                 **extra_fields)


class MontageUser(AbstractBaseUser, PermissionsMixin):
    objects = MontageUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =['identifier_id']
    # 下記に記載したものがcreatesuperuser実行時に効かれる
    username = models.CharField(
        'ユーザ名',
        max_length=30,
        help_text='@で始まるユーザ名',
        validators=[validators.MinLengthValidator(3), USERNAME_VALIDATOR],
        error_messages={
            'unique': "すでに存在しているユーザ名です",
            'min': "名前が短すぎます"
        },
        unique=True,
    )
    identifier_id = models.CharField(
        'ユーザID',
        unique=True,
        max_length=30,
        help_text='auth0のユーザID',
    )
    is_staff = models.BooleanField(
        'スタッフか?', help_text='is_staff', default=False)
    is_superuser = models.BooleanField(
        '管理者か?', help_text='is_superuser', default=False)
    display_name = models.CharField(
        'プロフィール名',
        help_text='30文字以内',
        max_length=30,
        blank=False,
        error_messages={
            'max': "名前が長すぎます"
        },
    )
    date_of_birth = models.DateField(
        '誕生日', help_text='%yy-%MM-%dd形式.空白可', null=True, blank=True)
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
    profile_img_url = models.URLField(
        'profile_img_url', help_text='プロフィール画像のURL', blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(MontageUser, self).save(*args, **kwargs)
