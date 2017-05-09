"""
HMAC Auth plugin for HTTPie.

"""
import datetime
import base64
import hashlib
import hmac
import urllib

from httpie.plugins import AuthPlugin

try:
    from urlparse import urlparse
    from urllib import unquote

except ImportError:
    from urllib.parse import urlparse
    from urllib.parse import unquote

__version__ = '0.2.0'
__author__ = 'Nick Satterly'
__licence__ = 'MIT'


class HmacAuth:
    def __init__(self, username, password):
        self.access_id = username
        self.access_key = password.encode('ascii')

    def __call__(self, r):

        method = r.method

        content_type = r.headers.get('content-type')
        if not content_type:
            content_type = ''

        content_md5 = r.headers.get('content-md5')
        if not content_md5:
            if content_type:
                m = hashlib.md5()
                m.update(r.body)
                content_md5 = base64.encodestring(m.digest())
                r.headers['Content-MD5'] = content_md5
            else:
                content_md5 = ''

        httpdate = r.headers.get('date')
        if not httpdate:
            now = datetime.datetime.utcnow()
            httpdate = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
            r.headers['Date'] = httpdate

        url = urlparse(r.url)

        netloc = url.netloc
        pos = r.url.index(netloc) + len(netloc)
        path = r.url[pos:]

        path = unquote(path)
        if isinstance(path, bytes):
            path = path.decode('utf8')
        if path.startswith('/api'):
            path = path[4:]

        string_to_sign = '\n'.join([method, content_md5, content_type, httpdate, path])
        if not isinstance(string_to_sign, bytes):
            string_to_sign = string_to_sign.encode('utf-8')
        digest = hmac.new(self.access_key, string_to_sign, hashlib.sha1).digest()
        signature = base64.encodestring(digest).rstrip()
        if isinstance(signature, bytes):
            signature = signature.decode('utf-8')

        if self.access_id == '':
            r.headers['Authorization'] = 'ODPS %s' % signature
        elif self.access_key == '':
            raise ValueError('HMAC secret key cannot be empty.')
        else:
            r.headers['Authorization'] = 'ODPS %s:%s' % (self.access_id, signature)

        return r


class HmacAuthPlugin(AuthPlugin):

    name = 'ODPS token auth'
    auth_type = 'odps'
    description = 'Sign requests using a ODPS compliant method'

    def get_auth(self, username, password):
        return HmacAuth(username, password)
