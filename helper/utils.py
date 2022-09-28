from datetime import datetime

start = """
Добавь меня в группу и дай права на чтение сообщений
Я буду вашим верным помощником в организации расписания пар 😎
Весь мой код открыт и находится на https://github.com/rombintu/timeshibot"""
pattern_res = "Расписание на {}:\n{}"

weeks = ["even", "odd"]

days = [
    "понедельник",
    "вторник",
    "среду",
    "четверг",
    "пятницу",
    "субботу",
    "воскресенье",
    ]

short_days = { 
    "rus": ["пн", "вт", "ср", "чт", "пт", "сб", "вс"],
    "en" : ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
}


triggers = {
    "lesson": ["пары", "расписание"],
    "which" : "какой",
    "office": "кабинет",
    "unday" : ["сегодня", "завтра", "послезавтра", "вчера"],
    "day"   : [*days, *short_days["rus"]],
    }


def get_weekday(short=False, tomorrow=0, en=False):
    weekday = datetime.today().weekday() + tomorrow
    if weekday > 6: weekday = weekday-7
    if short:
        if en:
            return short_days["en"][weekday]
        else:
            return short_days["rus"][weekday]
    return days[weekday]

def filter_by_day(text=""):
    for i, (day, sday) in enumerate(zip(days, short_days["rus"])):
        if day in text or sday in text:
            return i
    return -1