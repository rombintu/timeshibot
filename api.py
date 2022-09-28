import os
from typing import List
import requests

class Api:
    def __init__(self, route):
        self.route = route

    def GET(self, chat_id, week, day, action="get"):
        return requests.get(
            os.path.join(
                self.route, chat_id, week, day, action)).json()

    def POST(self, chat_id, week, day, action, payload=[]):
        return requests.post(
            os.path.join(
                self.route, chat_id, week, day, action), 
                json=payload).json()
