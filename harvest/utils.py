    
class JSONObject(object):
    def update_from_json(self, json_dict):
        for key, value in json_dict.items():
            setattr(self, key, value)
            
    def __init__(self, json_dict):
        self.update_from_json(json_dict)
        
            
    def __repr__(self):
        return u"<%s: %s>" % (self.__class__.__name__, self.__unicode__())
        
class HarvestObjectDoesNotExist(Exception):
    pass