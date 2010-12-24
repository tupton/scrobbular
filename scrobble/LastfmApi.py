import hashlib
import os
import sys
import time
import urllib
urllib.getproxies_macosx_sysconf = lambda: {}
import urllib2
import xml.dom.minidom

from LastfmSession import get_session_key, put_session_key

class LastfmApi(object):
    """An interface to the Last.fm API"""

    API_KEY = "24ff1477a4127b410d1f0b660c3049ee"
    API_SECRET = "3f5fd072347bce672b2f2e91a8ce3007"

    API_URL = "http://ws.audioscrobbler.com/2.0/"
    AUTH_URL = "http://www.last.fm/api/auth/"

    def __init__(self, username):
        self.username = username

    def _add_api_signature_to_params(self, params):
        """Calculate and add the API signature to the given parameters"""

        api_sig = self._get_api_signature(params)
        params['api_sig'] = api_sig
        return params

    def _build_auth_url(self, params, post=False):
        """Build a URL to send to the authorization end point"""

        return self._build_url(self.AUTH_URL, params, post)

    def _build_request_url(self, params, post=False):
        """Build a URL to send to the API end point"""

        return self._build_url(self.API_URL, params, post)

    def _build_param_string(self, params):
        """Build a param string from the given dictionary of params"""

        encoded = urllib.urlencode([(k, v) for k,v in params.iteritems()])
        return encoded

    def _build_url(self, base, params, post=False):
        """Build a request URL into an object that can be passed to urllib2.urlopen"""

        param_string = self._build_param_string(params)

        if post is True:
            url = urllib2.Request(url=base, data=param_string)
        else:
            url = base + '?' + self._build_param_string(params)

        return url

    def _get_api_signature(self, params):
        """Get the API signature for the given parameters"""

        keys = params.keys()
        keys.sort()
        sort = [(k, params.get(k)) for k in keys]
        to_hash = "".join(["" + k + str(v) for k,v in sort])
        to_hash = to_hash + self.API_SECRET
        md5 = hashlib.md5()
        md5.update(to_hash)
        return md5.hexdigest()

    def _handle_session_key_response(self, response):
        """Get a session key from a response"""

        dom = xml.dom.minidom.parseString(response)
        lfm = dom.getElementsByTagName('lfm')[0]
        if lfm.getAttribute('status').lower() == 'ok':
            session = lfm.getElementsByTagName('session')[0]
            session_key_tag = session.getElementsByTagName('key')[0]
            session_key = self._get_xml_text(session_key_tag.childNodes)
            return session_key
        else:
            print dom.toprettyxml()
            raise Exception('Bad response from Last.fm')

    def _handle_token_response(self, response):
        """Get a token from the given response"""

        dom = xml.dom.minidom.parseString(response)
        lfm = dom.getElementsByTagName('lfm')[0]
        if lfm.getAttribute('status').lower() == 'ok':
            token_tag = lfm.getElementsByTagName('token')[0]
            token = self._get_xml_text(token_tag.childNodes)
            return token
        else:
            print dom.toprettyxml()
            raise Exception('Bad response from Last.fm')

    def _get_xml_text(self, nodelist):
        """Get the text content of a given set of nodes (.childNodes of the element whose text you want)"""

        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    def _get_session_key(self):
        """Get the session key for a user"""

        username = self.username
        session_key = get_session_key(username)

        return session_key

    def _send_request(self, url):
        """Send a request and return the raw response"""

        response = urllib2.urlopen(url)
        text = response.read()
        return text

    def get_request_token_url(self):
        """Get a Last.fm request token"""

        host = os.environ['HTTP_HOST'] if os.environ.get('HTTP_HOST') else os.environ['SERVER_NAME']
        params = dict({'cb': 'http://' + host + '/auth?username=' + self.username, 'api_key': self.API_KEY})
        url = self._build_auth_url(params)
        return url

    def create_and_set_session_key(self, token):
        """Create a session key with the given token and set it in the datastore"""

        params = self._add_api_signature_to_params(dict({'method': 'auth.getsession',
            'api_key': self.API_KEY, 'token': token}))
        session_key = self._handle_session_key_response(self._send_request(self._build_request_url(params)))

        put_session_key(self.username, session_key)

        return session_key

    def scrobble(self, artist, track, duration, album=None):
        """Submit a track to Last.fm for the given username and password"""

        session_key = self._get_session_key()

        if session_key is None:
            return

        params = dict({'method': 'track.scrobble',
            'track': track, 'artist': artist, 'duration': duration,
            'timestamp': int(time.time() - int(duration)), 
            'api_key': self.API_KEY, 'sk': session_key})

        if album is not None:
            params['album'] = album

        params = self._add_api_signature_to_params(params)
        self._send_request(self._build_request_url(params, post=True))

    def update_now_playing(self, artist, track, duration=None, album=None):
        """Submit a track to Last.fm to update the now playing status"""

        session_key = self._get_session_key()

        if session_key is None:
            return

        params = dict({'method': 'track.updatenowplaying',
            'track': track, 'artist': artist,
            'api_key': self.API_KEY, 'sk': session_key})

        if duration is not None:
            params['duration'] = duration

        if album is not None:
            params['album'] = album

        params = self._add_api_signature_to_params(params)
        self._send_request(self._build_request_url(params, post=True))

