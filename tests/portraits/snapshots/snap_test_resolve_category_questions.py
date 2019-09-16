# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestResolveCategoryQuestions.test_it 1'] = {
    'data': {
        'categoryQuestions': [
            {
                'about': 'この質問は表示されます2',
                'id': '6'
            },
            {
                'about': 'この質問は表示されます1',
                'id': '5'
            }
        ]
    }
}
