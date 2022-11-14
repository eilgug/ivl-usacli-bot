import os
import telebot as tb
import callback_handler as ch
import constants as const
from telebot import types
from telebot.callback_data import *
import prettytable as pt
from dotenv import load_dotenv
from ivl_services import IVLServices

from flask import Flask, request
from api import blueprint

server = Flask(__name__)
server.register_blueprint(blueprint)

ivl_service = IVLServices()

load_dotenv()
API_KEY = os.getenv('API_KEY')
HOST = os.getenv('HOST');
bot = tb.TeleBot(API_KEY);


@bot.message_handler(commands=['alive'])
def test(message):
    bot.send_message(message.chat.id, "Hey! Sono vivo!");


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Ciao, ' + message.from_user.first_name + '!')


@bot.message_handler(commands=['classifica'])
def get_classifica(message):
    territory_data = ivl_service.get_territory()

    options = {}
    for territory in territory_data:
        callback_data = f"{const.commands[const.LEADERBOARD]}|{const.steps[const.TERRITORY]}|{territory['id']}"
        options[territory['name']] = {'callback_data' : callback_data}

    reply_markup = tb.util.quick_markup(options, 2)
    bot.send_message(message.chat.id, "Di che campionato vuoi conoscere la classifica?", reply_markup=reply_markup)

@bot.message_handler(commands=['calendario', 'nextmatch'])
def get_calendario_nextmatch(message):
    territory_data = ivl_service.get_territory()
    msg_text = ""
    if "calendario" in message.text:
        command = const.CALENDAR
        msg_text = "Di che squadra vuoi conoscere il calendario?"
    if "nextmatch" in message.text:
        command = const.NEXT_MATCH
        msg_text = "Di che squadra vuoi conoscere la prossima partita?"
    options = {}
    for territory in territory_data:
        callback_data = f"{const.commands[command]}|{const.steps[const.TERRITORY]}|{territory['id']}"
        options[territory['name']] = {'callback_data' : callback_data}

    reply_markup = tb.util.quick_markup(options, 2)
    bot.send_message(message.chat.id, msg_text, reply_markup=reply_markup)

# ---API---

@server.route('/' + API_KEY, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = tb.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=HOST + API_KEY)
    return "!", 200

@server.route("/stop")
def stop_webhook():
    bot.remove_webhook()
    bot.close()
    return "Bot stopped", 200


if __name__ == "__main__":
    bot.register_callback_query_handler(callback=ch.callback_leaderboard, func=lambda call: str(call.data).split(sep='|')[0] == const.commands[const.LEADERBOARD], pass_bot=True )
    bot.register_callback_query_handler(callback=ch.callback_calendar_nextmatch, func=lambda call: str(call.data).split(sep='|')[0] in [const.commands[const.CALENDAR], const.commands[const.NEXT_MATCH]], pass_bot=True )

    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    #bot.infinity_polling()
