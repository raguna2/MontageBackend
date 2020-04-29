import base64
import logging

from io import BytesIO
from typing import Optional

import requests
from montage.settings import STATIC_ROOT


from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageFilter


logger = logging.getLogger(__name__)


FONT_PATH = f"{STATIC_ROOT}/fonts/hiragino_maru_pron_w4.ttc"
SHARE_IMAGE_TEMPLATE = f'{STATIC_ROOT}/template/share_template.png'


def mask_circle_transparent(pil_img: Image, blur_radius: int, offset=0, fill_color=255) -> Image:
    """送られてきた画像を角丸にして返却する."""
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=fill_color)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    result = pil_img.copy()
    result.putalpha(mask)

    return result


def create_ogp_share_image(profile_img_url: str, question: str, answer: str) -> Optional[str]:
    """OGPシェア用の画像を作成する."""
    # テンプレート画像&プロフィール画像読み込み
    img = Image.open(SHARE_IMAGE_TEMPLATE)
    response = requests.get(profile_img_url)
    if not response.content:
        logger.error("failed to fetch user profile image from cloudinary. %s", profile_img_url)
        return

    profile_img = Image.open(BytesIO(response.content))

    # 質問と回答を書き込む
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font=FONT_PATH, size=22)
    draw.text((180, 105), question, (35, 35, 35), font=font)
    draw.text((200, 240), answer, (35, 35, 35), font=font)

    # プロフィール画像をリサイズする
    profile_img = ImageOps.fit(profile_img, (90, 90), Image.ANTIALIAS)
    profile_img = profile_img.convert("RGBA")

    # プロフィール画像を角丸にする
    rounded_profile_img = mask_circle_transparent(profile_img, 1)

    # プロフィール画像用の影を作成する
    shadow = Image.new("RGBA", rounded_profile_img.size, 0)
    ImageDraw.Draw(shadow)
    shadow = mask_circle_transparent(shadow, 3, fill_color=200)

    # プロフィール画像と影をテンプレートに合成する
    img.paste(shadow, (61, 211), shadow)
    img.paste(rounded_profile_img, (60, 207), rounded_profile_img)

    # Base64データに変換して返却する
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue())

    return img_str.decode('utf-8')
