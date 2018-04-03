# encoding=utf-8
import logging
from requests import Session
import json

API_URL = 'https://api.ucloud.cn/'

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class UcAPIException(Exception):
    pass


class Ucloud(object):
    def __init__(self, user, password, timeout=None):
        self.user = user
        self.password = password
        self.timeout = timeout
        self._session = Session()
        self._session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        })
        self.base_url = API_URL
        self.auth = ''

    def login(self):
        data = {
            'Action': 'LoginByPassword',
            'UserEmail': self.user,
            'Password': self.password,
        }
        self.auth, value = self._post(data=data)
        if not self.auth:
            logger.info("username: %s login fail", self.user)
            raise UcAPIException(value)
        logger.info("username: %s login successfully ", self.user)

    def _parse_data(self, text):
        value = json.loads(text)
        if isinstance(value, dict):
            return value
        else:
            logger.warn('unable to parse json: %s' % text)
            return {}

    def _post(self, data=None, **kwargs):
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
        if not self.auth:
            logger.info("username: %s login fail", self.user)
            raise UcAPIException('auth fail')
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


