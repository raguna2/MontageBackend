from collections import namedtuple
from snapshottest import TestCase


Clown = namedtuple('Clown', ('name', 'nose_type'))


def test_clown(snapshot):
      clown = Clown('bozo', 'red and round')
      snapshot.assert_match(clown)
