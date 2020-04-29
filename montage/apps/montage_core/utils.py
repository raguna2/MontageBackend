import os
from typing import Optional

import cloudinary


def upload_base64_img_to_cloudinary(base64_img: str) -> Optional[str]:
    """base64形式の画像をCloudinaryへアップロードする."""
    folder = os.environ.get('CLOUDINARY_UPLOAD_SHARE_FOLDER', 'share')
    uploaded = cloudinary.uploader.upload(base64_img, folder=folder)
    return uploaded.get('secure_url')

