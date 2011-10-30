import simplejson
import requests

auth_session = None # Give users the posibility to make us save their session, while the program runs

class InvalidAuthSession(Exception):
    pass
    
class WrongHarvestCredentials(Exception):
    pass

def get_auth_session(auth=None):
    if auth:
        return [auth.session, auth.domain]
    elif not auth and auth_session:
        return auth_session
    elif not auth and not auth_session:
        raise InvalidAuthSession("Not authentication session provided")

class HarvestAuthentication(object):
    domain = None
    session = None
    def __init__(self, username, password, subdomain, save=False):
        self.domain = 'https://%s.harvestapp.com/' % subdomain
        self.session = requests.session(headers={'Accept': 'application/json'}, auth=(username, password))
        if save:
            auth_session = [self.session, self.domain]
        r = self.session.get(self.domain + "account/who_am_i")
        try:
            simplejson.loads(r.content)
        except simplejson.JSONDecodeError:
            raise WrongHarvestCredentials()