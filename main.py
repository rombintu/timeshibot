import os
import telebot

from helper import utils

bot = telebot.TeleBot(os.getenv("TOKEN"), parse_mode=None)


class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_chat_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id,message.from_user.id).status in ['administrator']
	
bot.add_custom_filter(IsAdmin())


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, utils.start)

@bot.message_handler(content_types=['document'], is_chat_admin=True)
def handle_text_doc(message):
	pass

@bot.message_handler(content_types=["text"])
def handle_text(message):
    req = message.text.lower()
    if req.split()[0] in utils.triggers["lesson"]:
        # TOMMORROW
        if utils.triggers["unday"][1] in req:
            bot.reply_to(message, utils.pattern_res.format(utils.get_weekday(tomorrow=1).title(), ""))
        # TOMMORROW+1
        elif utils.triggers["unday"][2] in req:
            bot.reply_to(message, utils.pattern_res.format(utils.get_weekday(tomorrow=2).title(), ""))
        # YESTERDAY
        elif utils.triggers["unday"][3] in req:
            bot.reply_to(message, utils.pattern_res.format(utils.get_weekday(tomorrow=-1).title(), ""))
        # TODAY
        else:
            bot.reply_to(message, utils.pattern_res.format(utils.get_weekday().title(), ""))
    elif utils.triggers["which"] in req and utils.triggers["office"] in req:
        bot.reply_to(message, utils.pattern_res.format(utils.get_weekday().title(), ""))
if __name__ == "__main__":
    print("Bot status: ACTIVE")
    bot.infinity_polling()