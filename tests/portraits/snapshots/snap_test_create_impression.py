# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCreateImpression.test_it 1'] = {
    'data': {
        'createImpression': {
            'impression': {
                'content': 'この回答が作られます',
                'id': '1'
            },
            'ok': True
        }
    }
}
