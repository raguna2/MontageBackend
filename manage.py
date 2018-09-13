#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # /montage/settings/common.pyを設定ファイルにする設定
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "montage.settings.common")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "インポートエラーです"
        ) from exc
    execute_from_command_line(sys.argv)
