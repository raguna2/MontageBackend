import json
import logging
import os

from django.core.cache import cache
from django.utils import timezone

import requests
from jose import jwk, jwt
from jose.backends.rsa_backend import RSAKey
from jose.utils import base64url_decode

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
API_IDENTIFIER = os.environ.get('AUTH0_API_IDENTIFIER')
ALGORITHMS = ["RS256"]

logger = logging.getLogger(__name__)


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header(auth_token):
    """AUTHトークンの検証

    Notes
    -----------------
    Bearer hogehoge形式のトークンを検証して下記ならNG

    1. bearerが先頭にない

    2. Bearer[スペース]トークン形式になっていない

    3. Bearer[スペース:トークン[スペース]他の文字列 形式になっている
    """
    logger.info('validate auth_token')
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
    logger.info('verified success!')

    id_token = parts[1]
    return id_token


def verify_payload(payload):
    # 有効期限チェック
    logger.info('verify payload')
    if timezone.now().timestamp() > payload['exp']:
        logger.error('Expired token.')
        raise AuthError({
            "code": "Expired token!",
            "description": "Expired token!"
        }, 401)

    logger.debug('exp の有効期限は問題なし')

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
    logger.info('get JWK')
    jwks = cache.get('auth0_jwk')

    if jwks:
        logger.info('cacheのjwkを利用します.')
        return jwks

    # キャッシュになければ取得する
    url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    response = requests.get(url)
    if response.status_code != 200:
        logger.error('jwkが取得できませんでした')
        raise AuthError(
            {
                "code": "jwk_not_found",
                "description": f"JWK is NOT FOUND from {url}"
            }, 401)

    jwks = json.loads(response.text)['keys']

    # 1時間キャッシュする
    cache.set('auth0_jwk', jwks, 3600)
    logger.info('JWK was cached!')

    return jwks


def get_public_key(id_token):
    jwks = get_json_web_keys()

    try:
        # JWTをデコードする
        unverified_header = jwt.get_unverified_header(id_token)
    except jwt.JWTError as e:
        logger.error(e)
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
        logger.error('kidがみつかりません')
        raise AuthError(
            {
                "code": "kid_not_found",
                "description": "kid is Not found in keys: {}".format(kid)
            }, 401)

    # 公開鍵を取得
    return jwk.construct(jwks[key_index])


def verify_signature(id_token):
    logger.info('verify signature')
    # 署名を検証する
    public_key: RSAKey = get_public_key(id_token)  # 公開鍵を取得
    message, signature = id_token.rsplit('.', 1)
    decoded_signature = base64url_decode(signature.encode('utf-8'))

    # 公開鍵
    if not public_key.verify(message.encode('utf-8'), decoded_signature):
        logger.error('Invalid token')
        raise AuthError({
            "code": "invalid_token",
            "description": "Token is invalid"
        }, 401)

    return True
