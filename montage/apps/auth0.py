import json

from montage.apps.logging import logger_d, logger_e
from django.core.cache import cache
from django.utils import timezone

import requests
from jose import jwk, jwt
from jose.utils import base64url_decode
from jose.backends.rsa_backend import RSAKey

AUTH0_DOMAIN = "montage.auth0.com"
API_IDENTIFIER = "RGVd2YKMt0igpii0SWSGPmYV2MiPtT7Z"
ALGORITHMS = ["RS256"]


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class Auth0Error(Exception):
    pass


def get_token_auth_header(auth_token):
    """AUTHトークンの検証

    Notes
    -----------------
    Bearer hogehoge形式のトークンを検証して下記ならNG

    1. bearerが先頭にない

    2. Bearer[スペース]トークン形式になっていない

    3. Bearer[スペース:トークン[スペース]他の文字列 形式になっている
    """
    parts = auth_token.split()

    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with"
                " Bearer"
            }, 401)
    elif len(parts) == 1:
        raise AuthError({
            "code": "invalid_header",
            "description": "Token not found"
        }, 401)
    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be"
                " Bearer token"
            }, 401)

    id_token = parts[1]
    return id_token


def verify_payload(payload):
    # 有効期限チェック
    if timezone.now().timestamp() > payload['exp']:
        logger_e.error('Expired token.')
        raise AuthError({
            "code": "Expired token!",
            "description": "Expired token!"
        }, 401)

    logger_d.debug('exp の有効期限は問題なし')

    if not payload['iss'] == f"https://{AUTH0_DOMAIN}/":
        raise AuthError({
            "code": "issuer is not matched.",
            "description": "iss is not matched."
        }, 401)

    if not payload['aud'] == API_IDENTIFIER:
        raise AuthError({
            "code": "issuer is not matched.",
            "description": "iss is not matched."
        }, 401)

    return True


def get_json_web_keys():
    """JWKを取得する"""
    # キャッシュから取得
    jwks = cache.get('auth0_jwk')

    if jwks:
        logger_d.debug('cacheのjwkを利用します.')
        return jwks

    # キャッシュになければ取得する
    url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    response = requests.get(url)
    if response.status_code != 200:
        logger_e.error('jwkが取得できませんでした')
        raise Auth0Error(f"Not found JWK {url}")

    jwks = json.loads(response.text)['keys']

    # 1時間キャッシュする
    cache.set('auth0_jwk', jwks, 3600)

    return jwks


def get_public_key(id_token):
    jwks = get_json_web_keys()

    try:
        # JWTをデコードする
        unverified_header = jwt.get_unverified_header(id_token)
    except jwt.JWTError as e:
        logger_e.error(e)
        raise AuthError({
            "code":
            "invalid_header",
            "description":
            "Invalid header. "
            "Use an RS256 signed JWT Access Tokenだよ"
        }, 401)

    if unverified_header["alg"] == "HS256":
        # 暗号化のアルゴリズムがRS256ではなくHS256ならエラーにする
        raise AuthError({
            "code":
            "invalid_header",
            "description":
            "Invalid header. "
            "Use an RS256 signed JWT Access Token"
        }, 401)

    kid = unverified_header['kid']
    # 公開鍵のセットから該当のkidを探す
    key_index = -1

    for i in range(len(jwks)):
        if kid == jwks[i]['kid']:
            key_index = i
            break

    # 公開鍵のセットから該当のkidが見つからなかった場合の処理
    if key_index == -1:
        logger_e.error('kidがみつかりません')
        raise Auth0Error('Not found kid in keys: {}'.format(kid))

    # 公開鍵を取得
    return jwk.construct(jwks[key_index])


def verify_signature(id_token):
    # 署名を検証する
    public_key: RSAKey = get_public_key(id_token)  # 公開鍵を取得
    message, signature = id_token.rsplit('.', 1)
    decoded_signature = base64url_decode(signature.encode('utf-8'))

    # 公開鍵
    if not public_key.verify(message.encode('utf-8'), decoded_signature):
        logger_e.error('Invalid token')
        raise Auth0Error('Invalid token')

    return True
