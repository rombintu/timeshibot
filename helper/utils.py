from datetime import datetime

start = """
Добавь меня в группу и дай права на чтение сообщений
Я буду вашим верным помощником в организации расписания пар 😎
Весь мой код открыт и находится на https://github.com/rombintu/timeshibot"""
pattern_res = "Расписание на {}:\n{}"

days = [
    "понедельник",
    "вторник",
    "среда",
    "четверг",
    "пятница",
    "суббота",
    "воскресенье",
]

short_days = [
    "пн", "вт", "ср", "чт", "пт", "сб", "вс",
]

triggers = {
    "lesson": ["пары", "расписание"],
    "which" : "как",
    "office": "каб",
    "unday" : ["сегодня", "завтра", "послезавтра", "вчера"],
    "day"   : [*days, *short_days],
    }


def get_weekday(short=False, tomorrow=0):
    weekday = datetime.today().weekday() + tomorrow
    if weekday > 6: weekday = weekday-7
    if short:
        return short_days[weekday]
    return days[weekday]