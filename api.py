import os
import requests

class Api:
    def __init__(self, route):
        self.route = route

    def GET(self, chat_id, week, day, action="get"):
        try:
            return requests.get(
                os.path.join(
                    self.route, chat_id, week, day, action)).json(), None
        except Exception as error:
            return {}, error

    def POST(self, chat_id, week, day, action, payload=[]):
        try:
            return requests.post(
                os.path.join(
                    self.route, chat_id, week, day, action), 
                    json=payload).json(), None
        except Exception as error:
            return {}, error