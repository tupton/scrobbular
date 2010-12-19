from google.appengine.ext import db

class LastfmSession(db.Model):
    username = db.StringProperty(required=True)
    session_key = db.StringProperty(required=True)
    date_created = db.DateTimeProperty(auto_now_add=True)

def _get_session(username):
    """Get the session for a username"""
    query = LastfmSession.gql("WHERE username = :1 LIMIT 1", username)

    session = None
    results = query.fetch(1)
    if len(results) > 0:
        for result in results:
            session = result
            break

    return session

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
        session = LastfmSession(username=username, session_key=session_key)

    db.put(session)

