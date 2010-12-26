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

def _get_session(user):
    """Get the session for a user"""

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

def get_session_key(user):
    """Get the session key for a given user"""

    session_key = None
    session = _get_session(user)
    if session is not None:
        session_key = session.session_key

    return session_key

def put_session_key(user, session_key):
    """Create or replace the session key for a given user"""
    
    session = _get_session(user)
    if session is not None:
        session.session_key = session_key
    else:
        session = LastfmSession(user=user, user_id=user.user_id(), session_key=session_key, secret=create_new_secret())

    db.put(session)

def get_secret(user):
    """Get the secret for a user"""

    secret = None
    session = _get_session(user)
    if session is not None:
        secret = session.secret

    return secret

def put_secret(user, secret):
    """Set a secret for a user"""

    session = _get_session(user)
    if session is not None:
        session.secret = secret
        db.put(session)
    
def delete_session(user):
    """Delete the session record for the given user"""

    session = _get_session(user)
    if session is not None:
        db.delete(session)

