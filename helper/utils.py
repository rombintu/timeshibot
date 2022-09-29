from datetime import datetime

start = """
Добавь меня в группу и дай права на чтение сообщений
Я буду вашим верным помощником в организации расписания пар 😎
Весь мой код открыт и находится на https://github.com/rombintu/timeshibot"""

pattern_res = "Расписание на {}:\n{}"

problems_DB = "Проблемы с Базой данных 😢\nОбратитесь к администратору "
not_found = "Не найдено 🙈"
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


def get_weekday(short=False, tomorrow=0, en=False, i=False):
    weekday = datetime.today().weekday() + tomorrow
    if weekday > 6: weekday = weekday-7
    if i: return weekday
    if short:
        if en:
            return short_days["en"][weekday]
        else:
            return short_days["rus"][weekday]
    return days[weekday]

def get_weekdays_by_index(i):
    """
    Get (long_day_rus, short_day_rus, short_day_en)
    """
    return (
        days[i],
        short_days["rus"][i],
        short_days["en"][i],
    )

def get_current_week(): # TODO
    return weeks[0]

def filter_by_day(text=""):
    for i, (day, sday) in enumerate(zip(days, short_days["rus"])):
        if day in text or sday in text:
            return i
    return -1