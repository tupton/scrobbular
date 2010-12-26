import string

from random import choice

from google.appengine.api import users
from google.appengine.ext import db

class LastfmSession(db.Model):
    user = db.UserProperty(required=True)
    user_id = db.StringProperty(required=True)
    session_key = db.StringProperty(required=True)
    secret = db.StringProperty(required=True)
    date_created = db.DateTimeProperty(auto_now_add=True)

def _get_session(username):
    """Get the session for a user"""

    user = users.User(username)
    query = LastfmSession.gql("WHERE user = :1 LIMIT 1", user)

    session = None
    results = query.fetch(1)
    if len(results) > 0:
        for result in results:
            session = result
            break

    return session

def create_new_secret():
    """Generate a new secret"""

    secret = ''.join([choice(string.letters + string.digits) for i in range(8)])
    return secret

def get_session_key(username):
    """Get the session key for a given username"""

    session_key = None
    session = _get_session(username)
    if session is not None:
        session_key = session.session_key

    return session_key

def put_session_key(username, session_key):
    """Create or replace the session key for a given username"""
    
    session = _get_session(username)
    if session is not None:
        session.session_key = session_key
    else:
        session = LastfmSession(username=username, session_key=session_key, secret=create_new_secret())

    db.put(session)

def get_secret(username):
    """Get the secret for a user"""

    secret = None
    session = _get_session(username)
    if session is not None:
        secret = session.secret

    return secret

def put_secret(username, secret):
    """Set a secret for a user"""

    session = _get_session(username)
    if session is not None:
        session.secret = secret
    else:
        session = LastfmSession(username=username, session_key=session_key, secret=create_new_secret())

    db.put(session)
    
def delete_session(username):
    """Delete the session record for the given user"""

    session = _get_session(username)
    if session is not None:
        db.delete(session)

