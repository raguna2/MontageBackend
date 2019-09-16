#!/usr/bin/env python
import os
import sys
import logging


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # /montage/settings/dev.pyを設定ファイルにする設定
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "montage.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logger.error('インポートエラーです')
        raise ImportError(
            "インポートエラーです"
        ) from exc
    execute_from_command_line(sys.argv)
