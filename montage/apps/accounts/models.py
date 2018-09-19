from pathlib import Path

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core import validators
from django.db import models

USERNAME_VALID_TEXT = 'ユーザー名には半角英数、アンダースコアだけ使えます'
USERNAME_VALIDATOR = validators.RegexValidator(r'^[a-zA-Z0-9_]+$',
                                               USERNAME_VALID_TEXT)


def get_image_path(instance, filename):
    """画像の保存先を取得する

    :param instance: Userのインスタンス
    :param filename: プロフィール画像のファイルの名前
    """
    path = Path('user-icon') / str(instance.username) / filename
    return path.resolve()


class MontageUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, is_staff, is_superuser,
                     **extra_fields):
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
    twitter_id = models.CharField(
        'TwitterID', help_text='@から始まる名前.@は不要', max_length=150, blank=True)
    mail_confirmed = models.BooleanField(
        "メールアドレスが確認済みか",
        help_text="確認済みの場合True",
        default=False,
    )
    # profile_image = models.ImageField('プロフィール画像', upload_to=get_image_path, blank=True)
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

    def __str__(self):
        return self.username

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
