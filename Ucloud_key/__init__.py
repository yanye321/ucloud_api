# encoding=utf-8
import logging
import hashlib
from requests import Session
import json

API_URL = 'https://api.ucloud.cn/'

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler)


class UcAPIException(Exception):
    pass


class Ucloud(object):
    def __init__(self, public_key, private_key, timeout=None):
        self.public_key = public_key
        self.private_key = private_key
        self.timeout = timeout
        self._session = Session()
        # self._session.headers.update({"Content-Type": "application/json"})
        self.base_url = API_URL

    def _verfy_ac(self, params):
        items = params.items()
        items.sort()

        params_data = ""
        for key, value in items:
            params_data = params_data + str(key) + str(value)

        params_data = params_data + self.private_key

        '''use sha1 to encode keys'''
        hash_new = hashlib.sha1()
        hash_new.update(params_data)
        hash_value = hash_new.hexdigest()
        return hash_value

    def _parse_data(self, text):
        value = json.loads(text)
        if isinstance(value, dict):
            return value
        else:
            logger.warn('unable to parse json: %s' % text)
            return {}

    def _post(self, data=None, **kwargs):
        if data is None:
            data = {}
        data['PublicKey'] = self.public_key
        data['Signature'] = self._verfy_ac(data)

        r = self._session.post(self.base_url, data=data, **kwargs)
        r.raise_for_status()
        # if not r.ok:
        #    return False, r.reason
        value = self._parse_data(r.text)
        if value.get('RetCode') != 0:
            return False, value.get('Message', 'unkonwn error')
        else:
            return True, value

    def _do_request(self, action, params=None):
        post_data = params or {}
        post_data['Action'] = action
        logger.debug("post: %s", json.dumps(post_data))
        status, value = self._post(data=post_data)
        if not status or not value:
            logger.error(value)
            raise UcAPIException(value)
        else:
            return value

    def __getattr__(self, action):
        ''' 动态创建方法, 方法名为uc官方api指令'''

        def fn(*args, **kwargs):
            if args:
                if len(args) == 1 and isinstance(args[0], dict):
                    kwargs = args[0]
                else:
                    raise TypeError("only args must be dict type")
            return self._do_request(action, kwargs)

        return fn
