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
	bot.reply_to(message, "Проверка прошла успешно!")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Short and Long day names
    day_short_en = ""
    # day_short_rus = ""
    day_long_rus = ""

    # Current week (even, odd)
    curr_week = utils.get_current_week()
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
                res = utils.pattern_res.format(
                    day_long_rus.title(), 
                    json.dumps(payload),
                )  
        bot.reply_to(message, res)

if __name__ == "__main__":
    print("Bot status: ACTIVE")
    bot.infinity_polling()