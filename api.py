import requests, json
from cachetools import cached, TTLCache

class Api:
    def __init__(self, route):
        self.route = route

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def GET(self):
        return requests.get(self.route).json()

    def POST(self, params={}):
        return requests.post(self.route, data=json.dumps(params)).json()

    def get_timetable_by_week(self, chat, day):
        pass