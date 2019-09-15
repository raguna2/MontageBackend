# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestFetchUsers.test_it[user_data0] 1'] = {
    'data': {
        'users': [
            {
                'displayName': 'ユーザ1',
                'id': '1',
                'identifierId': 'admin|0000001',
                'username': 'RAGUNA1'
            },
            {
                'displayName': 'ユーザ2',
                'id': '2',
                'identifierId': 'admin|0000002',
                'username': 'RAGUNA2'
            },
            {
                'displayName': 'ユーザ3',
                'id': '3',
                'identifierId': 'admin|0000003',
                'username': 'RAGUNA3'
            },
            {
                'displayName': 'ユーザ4',
                'id': '4',
                'identifierId': 'admin|0000004',
                'username': 'RAGUNA4'
            }
        ]
    }
}
