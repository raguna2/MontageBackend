#!/usr/bin/env python
import os
import sys

from montage.apps.logging import logger_e

if __name__ == "__main__":
    # /montage/settings/dev.pyを設定ファイルにする設定
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "montage.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logger_e.error('インポートエラーです')
        raise ImportError(
            "インポートエラーです"
        ) from exc
    execute_from_command_line(sys.argv)
