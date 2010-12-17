#! /usr/bin/env python
import sys
import os
import argparse
import ConfigParser
import lastfm
import sqlite3
import webbrowser

API_KEY = "24ff1477a4127b410d1f0b660c3049ee"
API_SECRET = "3f5fd072347bce672b2f2e91a8ce3007"

class LastfmSessionDb(object):
    """An interface to the lastfm session database"""
    def __init__(self):
        self.conn = None

    def get_connection(self):
        if (self.conn is None):
            self.conn = sqlite3.connect('/usr/local/share/pylastfm/sqlite3/session.db')

        return self.conn

    def get_cursor(self):
        conn = self.get_connection()
        return conn.cursor()

    def get_session_key(self, username):
        """Fetch the session key from the db"""
        c = self.get_cursor()
        u = (username, )
        c.execute("select session from lastfm_session where username = ? limit 1", u)
        row = c.fetchone()
        # TODO
        c.close()

    def set_session_key(self, username, session_key):
        """Put the session key in the db"""
        c = db.get_cursor()
        c.execute("insert (username, session_key) into lastfm_session values (?, ?)", username, session_key)
        c.commit()
        c.close()


def create_arg_parser():
    """Create an option parser for last.fm-specific options"""

    parser = argparse.ArgumentParser(description="Submit scrobbles and now playing updates to Last.fm")

    parser.add_argument('track', action='store',
            help='the name of the track to submit')
    parser.add_argument('artist', action='store',
            help='the artist of the track to submit')
    parser.add_argument('-p', '--now-playing', action='store_true',
            help='if this option is given, the track is submitted as a now playing update instead of being scrobbled')

    parser.add_argument('--config', type=file, default=open(os.environ['HOME'] + '/.pylastfm.conf', 'r'),
            help='the config to use instead of %(default)s')

    return parser

def get_credentials(config):
    """Get the credentials from the given config file"""
    cp = ConfigParser.RawConfigParser()
    cp.readfp(config)
    
    username = cp.get('global', 'username')

    return username

def get_session_key(username):
    """Get the session key for a user"""
    db = LastfmSessionDb()
    session_key = db.get_session_key(username)
    if session_key is None:
        api = lastfm.Api(API_KEY, API_SECRET)
        webbrowser.open_new(api.auth_url) # Open a browser and ask for authentication
        raw_input('press <ENTER> after giving permission')
        api.set_session_key()
        session_key = api.session_key

    return session_key

def submit_to_lastfm(username, artist, track, now_playing=False):
    """Submit a track to lastfm for the given username and password"""
    session_key = get_session_key(username)
    api = lastfm.Api(API_KEY, API_SECRET, session_key)

    user = api.get_authenticated_user()
    print user

def main(argv):
    parser = create_arg_parser()
    args = parser.parse_args()

    username = get_credentials(args.config) 

    submit_to_lastfm(username, args.artist, args.track, args.now_playing)

if __name__ == '__main__':
    main(sys.argv[1:])
