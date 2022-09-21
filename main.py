import os
import telebot

from helper import utils
from api import Api

bot = telebot.TeleBot(os.getenv("TOKEN"), parse_mode=None)
bot.backend_api = Api(os.getenv("API_BACKEND"))

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
    print(message.chat.id) # TODO
    req_full = message.text.lower()
    req_start = req_full.split()[0]
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
            bot.reply_to(message, utils.pattern_res.format(utils.get_weekday().title(), ""))
        
    elif utils.triggers["which"] in req_full and utils.triggers["office"] in req_full:
        bot.reply_to(message, utils.pattern_res.format(utils.get_weekday().title(), ""))
if __name__ == "__main__":
    print("Bot status: ACTIVE")
    bot.infinity_polling()