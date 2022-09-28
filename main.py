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
    chat_id = message.chat.id
    # Full text of request
    req_full = message.text.lower()
    # First word
    req_start = req_full.split()[0]
    # Other words (list) of request
    req_other = req_full.split()[0:]
    if req_start in utils.triggers["lesson"]:
        payload_filter = utils.filter_by_day(req_other)
        if payload_filter >= 0:
            bot.reply_to(message, utils.pattern_res.format(utils.days[payload_filter].title(), ""))
        # TOMORROW
        elif utils.triggers["unday"][1] in req_other:
            bot.reply_to(message, utils.pattern_res.format(utils.get_weekday(tomorrow=1).title(), ""))
        # TOMORROW+1
        elif utils.triggers["unday"][2] in req_other:
            bot.reply_to(message, utils.pattern_res.format(utils.get_weekday(tomorrow=2).title(), ""))
        # YESTERDAY
        elif utils.triggers["unday"][3] in req_other:
            bot.reply_to(message, utils.pattern_res.format(utils.get_weekday(tomorrow=-1).title(), ""))
        # TODAY
        else:
            payload, err = backend_api.GET(
                chat_id=str(chat_id), 
                week=utils.weeks[utils.get_current_week()], # TODO
                day=utils.get_weekday(short=True, en=True),
                )

            res = ""
            if err != None:
                res = utils.problems_DB
            else:
                res = utils.pattern_res.format(
                    utils.get_weekday().title(), 
                    json.dumps(payload),
                )
                
            bot.reply_to(message, res)
        
    elif utils.triggers["which"] in req_full and utils.triggers["office"] in req_full:
        bot.reply_to(message, utils.pattern_res.format(utils.get_weekday().title(), ""))
if __name__ == "__main__":
    print("Bot status: ACTIVE")
    bot.infinity_polling()