from helper import utils
from api import Api

def print_help():
    for mess in utils.triggers["day"]:
        print(mess)

def get_weekday():
    print(utils.get_weekday(tomorrow=-1))
    print(utils.get_weekday(short=True, tomorrow=5))


if __name__ == "__main__":
    get_weekday()