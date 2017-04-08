import time

from freezegun import freeze_time
import pytest

from .api import MarvelApi


class TestMarvelApiUnitTests():

    def setup_method(self, method):
        self.api = MarvelApi()

    @pytest.mark.parametrize("key", [
        'ts', 'apikey', 'hash'
    ])
    def test_api_generate_auth_keys_correct(self, key):
        auth_params = self.api._generate_auth_params()

        assert key in auth_params

    def test_api_auth_ts(self):
        t0 = time.time()
        auth_params = self.api._generate_auth_params()
        t1 = time.time()

        assert int(auth_params['ts']) <= int(t1)
        assert int(auth_params['ts']) >= int(t0)

    @freeze_time('2017-04-02')
    def test_api_hash(self):
        auth_params = self.api._generate_auth_params()
        assert auth_params['hash'] == 'acde5009a697e6e1ce6ef7dd3ad0a305'

    def test_generate_auth_params(self):
        pass

    def test_marvel_api_call_made(self):
        pass

    def test_async_request_returned(self):
        pass

    def test_async_requests_made(self):
        pass


