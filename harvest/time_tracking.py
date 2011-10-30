import requests
from harvest.auth import get_auth_session, InvalidAuthSession
from harvest.utils import JSONObject, HarvestObjectDoesNotExist
import simplejson

class TimeTrackManager(object):
    def get(self, auth=None, id=None):
        session, domain = get_auth_session(auth)
        r = session.get(domain + "daily/show/%s" % id)
        if r.status_code == 404:
            raise HarvestObjectDoesNotExist()
        return TimeTrackEntry(simplejson.loads(r.content))
    
    def filter(self, auth=None, id=None, date=None):
        session, domain = get_auth_session(auth)
        objects = []
        if id:
            return [self.get(auth=auth, id=id)]
        elif date:
            dates = {
                'day_of_the_year': date.timetuple()[7],
                'year': date.year,
            }
            r = session.get(domain + "daily/%(day_of_the_year)s/%(year)s" % dates)
        else:
            r = session.get(domain + "daily/")
        for entry in simplejson.loads(r.content)["day_entries"]:
            objects.append(TimeTrackEntry(entry))
        return objects

class TimeTrackEntry(JSONObject):
    objects = TimeTrackManager()
    
    def __unicode__(self):
        return u"%s %s %s" % (self.client, self.task, self.id)
    
    def toggle(self, auth=None):
        session, domain = get_auth_session(auth)
        r = session.get(domain + "daily/timer/%s" % self.id)
        if r.status_code == 200:
            self.update_from_json(simplejson.loads(r.content))
            return True
        return False
        
    def delete(self, auth=None):
        pass
    def save(self, auth=None):
        pass