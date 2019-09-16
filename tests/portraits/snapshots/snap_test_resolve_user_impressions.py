# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestResolveUserImpressions.test_it 1'] = {
    'data': {
        'userImpressions': [
            {
                'content': 'この回答は表示されます3',
                'id': '9',
                'question': {
                    'about': '5?',
                    'category': {
                        'id': 'Q2F0ZWdvcnlOb2RlOjM=',
                        'name': 'サンプルカテゴリ'
                    },
                    'id': '11'
                }
            },
            {
                'content': 'この回答は表示されます2',
                'id': '7',
                'question': {
                    'about': '3?',
                    'category': {
                        'id': 'Q2F0ZWdvcnlOb2RlOjM=',
                        'name': 'サンプルカテゴリ'
                    },
                    'id': '9'
                }
            },
            {
                'content': 'この回答は表示されます1',
                'id': '4',
                'question': {
                    'about': '1?',
                    'category': {
                        'id': 'Q2F0ZWdvcnlOb2RlOjM=',
                        'name': 'サンプルカテゴリ'
                    },
                    'id': '7'
                }
            }
        ]
    }
}
