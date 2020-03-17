# Montage

## Quickstart

### 事前条件

以下の依存パッケージがインストールされていることを確かめてください。

- Docker CE 17.06.0+
- docker-compose 1.13.0+

まだであれば、 Docker は
[Download Docker for Mac](https://docs.docker.com/docker-for-mac/install/#download-docker-for-mac)
からダウンロードしてインストールできます。
※ Windowsは [Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/) を使ってください（Docker for Windows は Hyper-V が必要なので Windows 10 Home では利用できません）。
また、 docker-compose は `pip install docker-compose` でインストールできます。

# sideSonar

## 設定ファイル

| ファイル名  | 用途                        |
|-------------|-----------------------------|
| `tox.ini`   | tox, pytest, flake8 の設定  |
| `mypy.ini`  | mypy の設定                 |


### docker-compose

docker-composeの設定ファイルは下記です。

| ファイル名                    | 環境             | 利用方法       |
|-----------------|----------------------|----------------------|
| `docker-compose.yml`  | すべて      | `docker-compose [ARG...]`|


## 開発環境手順

### 準備

アプリを起動する前に、 `.env` を作成します。 `.env`を作成するには`example.env`をコピーし、値を設定する必要があります。

 `.env` は docker-compose から読まれて、必要な値がコンテナに渡されます。
設定値については環境変数のセクションを参照してください。

```console
$ cp example.env .env
$ editor .env
```

## 環境変数

環境変数は、 `.env` ファイルで設定します。設定例は `example.env` に記載されています。

*warning*: 環境変数を追加した場合は、 `docker-compose.yml` への反映も行ってください

| variable                      | description                             |
|-------------------------------|-----------------------------------------|
| `SIDEUSONAR_PORT`                 | アプリが listen する TCP のポート番号   |
| `SIDEUSONAR_DB_NAME`              | データベース名                          |
| `SIDEUSONAR_DB_USER`              | データベースの認証に使うユーザー名      |
| `SIDEUSONAR_DB_PASSWORD`          | データベースの認証に使うパスワード      |
| `SIDEUSONAR_DB_ENGINE`            | データベースエンジン (例: `mysql`)      |
| `SIDESONAR_DB_URL_FOR_READ_ONLY`  | 読み取り用データベース名                |
| `SIDEUSONAR_DJANGO_LOG_LEVEL`     | django のログレベル (例: `DEBUG`)       |
| `SIDEUSONAR_DJANGO_DEBUG`         | django setting の `DEBUG`               |
| `SIDEUSONAR_DJANGO_SECRET_KEY`    | django setting の `SECRET_KEY`          |
| `SIDEUSONAR_DJANGO_ALLOWED_HOSTS` | django setting の `ALLOWED_HOSTS`       |
| `AWS_REGION`                      | デプロイ先AWSのリージョン               |
| `AWS_COGNITO_USER_POOL_ID`        | AWS CognitoのユーザpoolID               |
| `AWS_COGNITO_CLIENT_ID`           | AWS CognitoのクライアントID             |
| `AWS_SIDESONAR_AWS_ACCESS_KEY`    | AWS のアクセスキー                      |
| `AWS_SIDESONAR_AWS_ACCESS_SECRET` | AWS のアクセスキーシークレット          |
| `AWS_STORAGE_BUCKET_NAME`         | S3のバケット名                          |
| `COMING_SOON_FILE`                | S3から取得するCOMING_SOONファイル名     |
| `SIDESONAR_DJANGO_CORS_ORIGIN_WHITELIST` | Access-Control-Allow-Origin で許可する Origin のリスト |
| `SIDESONAR_DJANGO_CORS_ORIGIN_ALLOW_ALL` | すべての Origin を許可する。有効化すると USONAR_DJANGO_CORS_ORIGIN_WHITELIST は無視される |
| `SIDESONAR_API_URL` | sideSonar APIのエンドポイントURL |
| `LBC_MATCHING_API_BASE_PATH` | LBCマッチAPIのベースエンドポイント |
| `VISIT_CARD_IMAGE_BUCKET_NAME` | 名刺画像保管用S3バケット名 |
| `API_LBC_SERVICE_STORAGE_BUCKET_NAME` |  LBCに関連する情報を保管するS3バケット名 |
| `USONAR_CONFIG_FILE_NAME` | usonarの設定ファイル名 |
| `DEAL_STATUS_URL` | 取引状況を取得するURL |


### アプリの起動

```console
$ docker-compose up -d
```

`http://localhost:8000/` からアプリへアクセスできます。


### Postgresコンテナについて

docker上でtoxを用いたテストを行うときにsidesonarユーザに

test_postgresデータベースへの権限を付与する必要があります。(下記手順)


#### 権限設定

docker-compose.ymlのあるディレクトリ上で`docker-compose exec postgres psql -U postgres -W postgres`

※パスワードはpasswordです

postgres実行画面になるので下記実行

`GRANT ALL PRIVILEGES ON test_postgres.* TO 'postgres'@'%';`

ctrl + Dで抜ける

### 動作確認

```console
# 下記実行しテストが実行できればOK
$ docker-compose run --rm web tox
```


## コンテナの管理

### イメージのビルド
```console
# docker-compose.ymlのあるディレクトリ上で
$ docker-compose build
```

### コンテナの起動

```console
# docker-compose.ymlのあるディレクトリ上で
$ docker-compose up -d
```

### コンテナの再起動

```console
# docker-compose.ymlのあるディレクトリ上で
$ docker-compose restart web
```

### コンテナの起動確認方法
STATUSがexited: 起動していない

STATUSがup: 起動している
```conosole
# プロセスの確認
$ docker ps -a
```

### コンテナの停止

```console
$ docker-compose stop
```

### 起動中のコンテナの削除

```console
$ docker-compose down
```

上記コマンドを実行しても、データベース用のボリュームは維持されます。
データベース用のボリュームまで削除したい場合は、 `-v` オプションを追加してください。

### アプリコンテナのリビルド
```
$ docker-compose down web
$ docker-compose build web
```

リビルドは、 `requirements.txt` へ変更があった際に必要です。

### コンテナログの確認方法

```console
# webコンテナの場合
$ docker-compose logs web

# mysqlコンテナの場合
$ docker-compose logs mysql

# 直近200行確認
$ docker-compose logs --tail="200" web
```

## django コマンドを実行する
django コマンドを実行するには、 `docker-compose run` サブコマンドを使います。
`--rm` オプションをつけることでコマンド実行後コンテナを残さずにコマンドを実行できます。

### django コマンドの `shell` を実行する
```
$ docker-compose run --rm web python manage.py shell
Starting app_db_1 ... done
Python 3.6.5 (default, Mar 31 2018, 01:05:42)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

### django コマンドの `shell` を、tox環境で実行する
tox環境で実行することにより、testsの中のコードを実行することができる。
そのため、動作確認のためにfactories.pyのクラスを使って簡単なデータを作ることが可能になる。

```
$ docker-compose run --rm web .tox/py37/bin/python manage.py shell --pythonpath=tests
Starting montage_db_1 ... done                                                                                                                                                                Python 3.7.4 (default, Jul 13 2019, 14:27:50)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

## テストを実行する
- テストはtoxで実行します。設定内容はtox.iniを参照してください。

```
# 実行方法
$ docker-compose run --rm web tox
```

`requirements.txt` に更新があったとき、ImportErrorが発生する場合があります。
そういった場合は `-r` (recreateオプション)を付与することで該当パッケージがインストールされます。
```
# 実行方法
$ docker-compose run --rm web tox -r
```

繰り返し同じテスト実行する場合、`--reuse-db`オプションで、DBのスキーマ構築を省略できます。
これにより、toxの実行時間を短縮することができます。
```
# 実行方法
$ docker-compose run --rm web tox -- --reuse-db
```

### マイグレーション
```
$ docker-compose run --rm web python manage.py migrate
```

### スーパユーザの作成
```
$ docker-compose run --rm web python manage.py createsuperuser
```
