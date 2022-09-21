import requests, json

class Api:
    def __init__(self, route):
        self.route = route

    def GET(self):
        return requests.get(self.route).json()

    def POST(self, params={}):
        return requests.post(self.route, data=json.dumps(params)).json()

    def get_timetable_by_week(self, chat, day):
        pass