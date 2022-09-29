from helper import utils
from api import Api

def print_help():
    for mess in utils.triggers["day"]:
        print(mess)

def get_weekday():
    print(utils.get_weekday(tomorrow=-1))
    print(utils.get_weekday(short=True, tomorrow=5))

def testApiGET():
    api = Api("http://localhost:7000/")
    payload = api.GET(
        chat_id="21ff12f12",
        week="0",
        day="mon",
    )
    print(payload)

def testApiPOST():
    api = Api("http://localhost:7000/")
    payload = api.POST(
        chat_id="21ff12f12",
        week="0",
        day="mon",
        action="create",
        payload=[
            {
                "time": "2018-12-10T13:49:51.141Z",
                "title": "eng",
                "office": "10",
                "teacher": "Ivandod 14"
            },
            {
                "title": "Информатика",
                "office": "00",
                "teacher": "Ivandod 122"
            }
        ]
    )
    print(payload)
    
if __name__ == "__main__":
    # get_weekday()
    # testApiPOST()
    # testApiGET()
    file = open("./example.xlsx", "rb")
    p = utils.excel_parse(file, sheet_name="wed")
    file.close()
    print(p)