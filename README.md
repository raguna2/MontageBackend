#### djangoの操作について

1. プロジェクトの新規作成
```docker-compose run web django-admin.py startproject montage .```

上記のようにすると、ディレクトリ配下に```manage.py```や ```montage/settings.py``` などの

ファイルを作ることができる。

2. settings.pyを編集
```settings.py
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'postgres',
        'PORT': 5432,
    }
}
```

3. ビルド(Dockerfileを配置しているディレクトリ上で実行)
```
>>> $ docker-compose build
```

4. サービスを起動
```
>>> $ docker-compose up -d
```

<注意点>

- Dockerfileについて

下記の14行目のようにWORKDIRで指定したところが、コンテナ内のメインディレクトリになる。

メインディレクトリにはmanage.pyが置いておかれていないと、```docker-compose run webserver python manage.py hogehoge```　としたときに実行出来ない。

そのため絶対にDockerfileの最後にはmanage.pyがあるディレクトリをWORKDIRにしておかないといけない。

```Dockerfile
       │ File: ./Dockerfile
───────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ # 元となるイメージを指定
   2   │ FROM python:3.7
   3   │ # バッファにデータを保持しない設定(1でなくても任意の文字でいい)
   4   │ ENV PYTHONUNBUFFERED 1
   5   │ # コンテナの中にディレクトリを作成
   6   │ RUN mkdir /app
   7   │ # 作業ディレクトリを指定
   8   │ WORKDIR /app
   9   │ # pipでインストールするパッケージをまとめたファイルを /appディレクトリにコピー
  10   │ COPY requirements.txt /app/
  11   │ RUN pip install -r requirements.txt
  12   │ # ローカルのDockerfileを設置したディレクトリ内のファイルをコンテナの/appディレクトリへコピー
  13   │ COPY . /app/
  14   │ WORKDIR /app/src  #ここ！！！！！
```

- Settings.pyについて

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'postgres',
          'USER': 'postgres',
          'HOST': 'postgres',　# ここがDockerfileのpostgresのサービス名と一致
          'PORT': 5432,
      }
  }
  ```

- アプリの作成
```docker-compose run webserver python manage.py startapp user ```

上記をdocker-compose.ymlのあるディレクトリ上で行うとdjangoのDockerfileでWORKDIRに指定したディレクトリ配下にアプリが作成される。settings.pyのアプリに追加することをお忘れなく

### その他docker-composeチートシート
- コンテナ内に入る ```docker-compose exec web bash```
- コンテナ作り直し ```docker-compose down```
- コンテナ作成 ```docker-compose build``` (docker-compose.ymlのあるディレクトリで)
- コンテナ起動```docker-compose up -d``` (docker-compose.ymlのあるディレクトリで)
- エラーログ確認```docker-compose logs web``` (docker-compose.ymlのあるディレクトリで)



