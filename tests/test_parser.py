import pytest
from sympathor.parser import ParsePaths


class TestParser():
    @pytest.fixture(params=[
        ('tests/files/test_ok_1.svg', True),  # multiple paths
        ('tests/files/test_ok_2.svg', True),  # no paths
        ('tests/files/test_ok_3.svg', True),  # no svg tag
        ('tests/files/test_ok_4.svg', True),  # no xml tag
        ('tests/files/test_ok_5.svg', True),  # plain path
        ('tests/files/test_not_ok_1.svg', False),  # no namespace
        ('tests/files/test_not_ok_2.svg', False),  # parse error
        ('M 0 0 C 10,10 20,10 30,0 Z', True),
    ])
    def source(self, request):
        return {'str': request.param[0], 'valid': request.param[1]}

    def test_basics(self, source):
        if source['valid']:
            paths = ParsePaths(source['str'])
            if len(paths) > 0:
                assert paths[0]
        else:
            with pytest.raises(ValueError):
                paths = ParsePaths(source['str'])
