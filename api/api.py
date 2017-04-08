import hashlib
import json
import logging
import time

import grequests
import requests
from requests.exceptions import ConnectTimeout

from .exceptions import MarvelApiException
import settings

logger = logging.getLogger(__name__)


class MarvelApi():
    """
    Requests wrapper to make api calls to the marvel API
    """
    def __init__(self):
        self.public_key = settings.PUBLIC_API_KEY
        self.private_key = settings.PRIVATE_API_KEY
        self.base_url = settings.BASE_API_URL

    def _generate_auth_params(self):
        """
        Handle marvel api auth logic to generate:

        ts: timestampe
        apikey: public api key
        hash: hash(ts + public key + private key)
        """
        ts = int(time.time())
        m = hashlib.md5()
        m.update(
            str(
                str(ts) +
                self.private_key +
                self.public_key
            ).encode())
        hash = m.hexdigest()
        return {
            'ts': ts,
            'apikey': self.public_key,
            'hash': hash
        }

    def request(
            self, method, url, params=None, data=None, async_req=False, timeout=None):
        """
        Make a request to the Marvel Api with given params, can also return
        an async request object for grequests to batch call if async_req = True

        Args:
            method: (str) standard HTTP method ('GET', 'POST')
            params: (dict) key values for url params
            data: (dict) body of POST requests
            async_req: (bool) if True return async request object to be completed later
            timeout: (int) seconds to fail wait before timing out a request
        Returns:
            Response object
        """
        params = params or {}

        auth_params = self._generate_auth_params()
        params.update(auth_params)

        url = self.base_url + url

        if async_req:
            request_func = grequests.request
        else:
            request_func = requests.request

        try:
            resp = request_func(
                method.upper(), url, params=params, data=data, timeout=timeout)
        except ConnectTimeout:
            logger.warning('Connection timed out for: {}'.format(
                url))
            resp = None

        return resp

    def _handle_resp_errors(self, resp):
        """
        Check for invalid / bad responses and raise error
        """
        if not resp or resp.status_code >= 400:
            # handle API error
            if resp:
                raise MarvelApiException(resp.content)
            else:
                raise MarvelApiException

    def get(self, url, params=None, async_req=False, timeout=None):
        """
        Make a single GET request to the marvel with url being the path
        and params being the url params
        """
        params = params or {}
        # default limit is 20 if none is set get max
        params.setdefault('limit', 100)

        resp = self.request(
            'GET', url, params, async_req=async_req, timeout=timeout)
        self._handle_resp_errors(resp)
        return json.loads(resp.content)

    def batch_get(self, url_list, param_list=None):
        """
        Use grequests to asynconously make multiple api calls to speed up the
        crawling of the API.

        Args:
            url_list: (list) list of API urls to call
            param_list: (list) list of dicts of url params

        Returns:
            (list) Response objects
        """
        param_list = param_list or [{} for x in range(len(url_list))]
        auth_params = self._generate_auth_params()

        for param in param_list:
            param.update(auth_params)

        async_calls = []
        for url, param in zip(url_list, param_list):
            async_calls.append(
                self.request('GET', url, param, async_req=True, timeout=10))
        resps = grequests.map(async_calls)

        for i, resp in enumerate(resps):
            try:
                self._handle_resp_errors(resp)
                resps[i] = json.loads(resp.content)
            except MarvelApiException:
                logger.warning('Request: url:{}, parmas:{} failed'.format(
                    url_list[i], str(param_list[i])))
                resps[i] = None

        return resps

