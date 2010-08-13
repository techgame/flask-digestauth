#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from functools import wraps

import flask
from . import authdigest

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def requires_auth(authDb):
    return authDb.requires_auth

def requires_session_key(key='username', msg='Not authorized', status=401):
    def decorSessionVar(f):
        @wraps(f)
        def checkSessionVar(*args, **kw):
            if key not in flask.session:
                return Response(msg, status)
            else:
                return f(*args, **kw)

        return checkSessionVar

    return decorSessionVar

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from . import authdigest

class FlaskRealmDigestDB(authdigest.RealmDigestDB):
    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            request = flask.request
            if not self.isAuthenticated(request):
                return self.challenge()

            flask.session['username'] = request.authorization.username
            return f(*args, **kwargs)

        return decorated

