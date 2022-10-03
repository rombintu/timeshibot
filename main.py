import os, json
import telebot

from helper import utils
from api import Api

bot = telebot.TeleBot(os.getenv("TOKEN"), parse_mode=None)
backend_api = Api(os.getenv("API_BACKEND") or "http://localhost:7000")

class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_chat_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id,message.from_user.id).status in \
            ['administrator', 'администратор', 'creator']
	
bot.add_custom_filter(IsAdmin())


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, utils.start)

# TODO
@bot.message_handler( content_types=["document"], is_chat_admin=True)
def handle_text_doc(message):
    chat_id = str(message.chat.id)
    ex_file = bot.download_file(bot.get_file(message.document.file_id).file_path)
    days_not_found = []
    week = 0
    js_payload = {}
    global_Errors = []
    res = "Успех!\nДни которые не были отправлены:\n{days}\nОшибки:\n{errors}"
    try:
        week = int(message.caption) % 2
    except TypeError:
        bot.reply_to(message, "Неправильный номер недели") # TODO
        return

    for i, day in enumerate(utils.short_days["en"]):
        try:
            js_payload[day] = utils.excel_parse(ex_file, sheet_name=day)
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
            week=utils.weeks[week],
            day=day,
            payload=req_payload
            )

            if err != None:
                res = utils.problems_DB
                bot.send_message(message.chat.id, res)
                return
            else:
                if payload["error"] != 0:
                    res = payload["message"]
                    print(res)
                    bot.send_message(message.chat.id, res)
    except Exception as error: # TODO
        global_Errors.append(str(error))
    bot.send_message(message.chat.id, res.format(
            days=", ".join(days_not_found),
            errors=" | ".join(global_Errors),
            )
        )

@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Short and Long day names
    day_short_en = ""
    # day_short_rus = ""
    day_long_rus = ""

    # Current week (even, odd)
    curr_week = utils.get_current_week() # TODO
    week_day_index = -1
    # Response
    res = ""
    res_flag = True
    # Costil for days
    index_day = -1

    chat_id = str(message.chat.id)
    # Full text of request
    req_full = message.text.lower()
    # First word
    req_start = req_full.split()[0]
    # Other words (list) of request
    req_other = req_full.split()[0:]
    if req_start in utils.triggers["lesson"]:
        
        index_day = utils.filter_by_day(req_other)
        
        # TOMORROW
        if utils.triggers["unday"][1] in req_other:
            week_day_index = utils.get_weekday(tomorrow=1, i=True)
        # TOMORROW+1
        elif utils.triggers["unday"][2] in req_other:
            week_day_index = utils.get_weekday(tomorrow=2, i=True)
        # YESTERDAY
        elif utils.triggers["unday"][3] in req_other:
            week_day_index = utils.get_weekday(tomorrow=-1, i=True)
        # TODAY
        else:
            week_day_index = utils.get_weekday(i=True)
        
    elif utils.triggers["which"] in req_full and utils.triggers["office"] in req_full:
        week_day_index = utils.get_weekday(i=True)
    else:
        res_flag = False

    if index_day >= 0:
        day_long_rus, _, day_short_en = utils.get_weekdays_by_index(index_day)
    elif week_day_index >=0:
        day_long_rus, _, day_short_en = utils.get_weekdays_by_index(week_day_index)

    if res_flag:
        payload, err = backend_api.GET(
            chat_id=chat_id, 
            week=curr_week, # TODO
            day=day_short_en,
            )

        if err != None:
            res = utils.problems_DB
        else:
            if payload["error"] == -1:
                res = utils.pattern_res.format(
                day_long_rus.title(), 
                utils.not_found,
            )
            else:
                buff = ""
                for s in payload["message"]["Subjects"]:
                    buff += utils.pattern_res_dig.format(
                        time=s["time"][:-3], # TODO
                        subject=s["title"],
                        teacher=s["teacher"],
                        office=s["office"],
                        comment=s["comment"]
                    ) + "\n"
                res = utils.pattern_res.format(
                    day_long_rus.title() +\
                        f'\n({utils.weeks_rus[payload["message"]["Week"]]} неделя)', 
                    buff, # TODO
                )  
        bot.reply_to(message, res)

if __name__ == "__main__":
    print("Bot status: ACTIVE")
    bot.infinity_polling()