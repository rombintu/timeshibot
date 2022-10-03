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

def create_new_post(f):
    backend_api = Api("http://localhost:7000")
    chat_id = str(1001628108127)
    days_not_found = []
    week = 0
    js_payload = {}
    global_Errors = []
    for i, day in enumerate(utils.short_days["en"]):
        try:
            js_payload[day] = utils.excel_parse(f, sheet_name=day)
        except ValueError:
            days_not_found.append(utils.short_days["rus"][i])
            continue
    try:
        for day, subjects in js_payload.items():
            req_payload = [] 
            keys = list(subjects.keys())
            pre_values = list(subjects.values())
            values = []
            for v in pre_values:
                values.append(list(v.values()))

            for i in range(len(values[0])):
                tmp = {}
                for j, key in enumerate(keys):
                    tmp[key] = str(values[j][i])
                req_payload.append(tmp)
            
            payload, err = backend_api.POST(
            chat_id=chat_id, 
            week=utils.weeks[week], # TODO
            day=day,
            payload=req_payload
            )

            if err != None:
                res = utils.problems_DB
                print(res)
                return
            else:
                if payload["error"] != 0:
                    res = payload["message"]
                    print(res)
    except Exception as error:
        global_Errors.append(str(error))
    res = "Успех!\nДни которые не были отправлены:\n{days}\nОшибки:\n{errors}"
    print(res.format(
            days=", ".join(days_not_found),
            errors=" | ".join(global_Errors),
            )
        )

if __name__ == "__main__":
    # get_weekday()
    # testApiPOST()
    # testApiGET()
    file = open("./example.xlsx", "rb")
    create_new_post(file)
    file.close()