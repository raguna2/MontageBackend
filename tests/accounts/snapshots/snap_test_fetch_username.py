# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_fetch_username 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 1,
                    'line': 1
                }
            ],
            'message': '''Syntax Error GraphQL (1:1) Unexpected Name "users"

1: users { username }
   ^
'''
        }
    ]
}
