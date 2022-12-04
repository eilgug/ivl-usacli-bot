import os
import json
from datetime import date, datetime
from db import Db
import telebot as tb
import constants as const
import callback_handler as ch
from rensponse_helper import preference_response, get_response_table, text_wrapping

from dotenv import load_dotenv
from telebot.callback_data import *
from ivl_services import IVLServices
from preference_service import PreferenceService
from flask import Flask, request


server = Flask(__name__)

ivl_service = IVLServices()
db = Db(r"ivl_bot.db")

load_dotenv()
API_KEY = os.getenv('API_KEY')
HOST = os.getenv('HOST')
ENV = os.getenv('ENVIRONMENT', 'dev')

bot = tb.TeleBot(API_KEY)

@bot.message_handler(commands=['alive'])
def test(message):
    bot.send_message(message.chat.id, "Hey! Sono vivo!");


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Ciao, ' + message.from_user.first_name + '!')


@bot.message_handler(commands=['classifica'])
def get_classifica(message):
    db.create_connection()
    data = db.get_preference(message.chat.id)

    if data:
        data = json.loads(data[0])
        leaderboard = ivl_service.get_leaderboard(data["g"])
        # return leaderboard
        data = []
        for row in leaderboard:
            name = text_wrapping(row['name'])
            data.append( [ name, row['Punteggio'] ] )

        leaderboard_table = get_response_table( ['SQUADRA', 'PTS'], data)
        bot.send_message(chat_id=message.chat.id, text=leaderboard_table, parse_mode='html')
    else:
        territory_data = ivl_service.get_territory()

        options = {}
        for territory in territory_data:
            callback_data = f"{const.commands[const.LEADERBOARD]}|{const.steps[const.TERRITORY]}|{territory['id']}"
            options[territory['name']] = {'callback_data' : callback_data}

        reply_markup = tb.util.quick_markup(options, 2)
        bot.send_message(message.chat.id, "Di che campionato vuoi conoscere la classifica?", reply_markup=reply_markup)

@bot.message_handler(commands=['calendario', 'nextmatch'])
def get_calendario_nextmatch(message):
    db.create_connection()
    data = db.get_preference(message.chat.id)

    if data:
        preference = json.loads(data[0])

        today = None
        if "nextmatch" in message.text:
            today = date.today()

        calendar = ivl_service.get_calendar(preference["t"], preference["c"], preference["g"], preference["s"], season_start=today)
        if "calendario" in message.text:
            # return leaderboard
            data = []
            for row in calendar:
                d = datetime.strptime(row['DataGioco'], "%Y-%m-%d %H:%M:%S")
                hour = d.strftime('%H:%M')
                day = d.strftime('%d/%m/%y')

                if row['squadra_casa_id'] == int(preference["s"]):
                    name = row['SquadraOspite']

                if row['squadra_ospite_id'] == int(preference["s"]):
                    name = row['SquadraCasa']

                data.append( [ name, f"{day}\n{hour}"] )

            calendar_table = get_response_table( ['VS', 'DATA/ORA'], data, max_width=10)
            bot.send_message(chat_id=message.chat.id, text=calendar_table, parse_mode='html')

        if "nextmatch" in message.text:
            next_match_data = calendar[0]

            data = [[next_match_data['SquadraCasa'], next_match_data['SquadraOspite']]]
            res_message = get_response_table( ['CASA', 'OSPITI'], data, max_width=10)

            d = datetime.strptime(next_match_data['DataGioco'], "%Y-%m-%d %H:%M:%S")
            hour = d.strftime('%H:%M')
            day = d.strftime('%d/%m/%Y')
            res_message += f"\n\n<b>Data:</b> {day} | <b>Ora:</b> {hour}"

            bot.send_message(message.chat.id, res_message, parse_mode='html')
            bot.send_location(message.chat.id, next_match_data['Palestra_lat'], next_match_data['Palestra_long'])
    else:
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

@bot.message_handler(commands=['preferenze'])
def preferenze(message):
    chat_id = message.chat.id
    db.create_connection()

    data = db.get_preference(chat_id)

    if data:
        options = {}
        callback_data_modify = f"{const.commands[const.PREFERENCE]}|0"
        callback_data_remove = f"{const.commands[const.PREFERENCE]}|R"
        options['Modifica'] = {'callback_data' : callback_data_modify}
        options['Rimuovi'] = {'callback_data' : callback_data_remove}
        reply_markup = tb.util.quick_markup(options, 1)

        data = json.loads(data[0])

        territory = ivl_service.get_territory(int(data["t"]))
        championship = ivl_service.get_championship(territory=int(data["t"]), id=int(data["c"]))
        group = ivl_service.get_groups(championship=int(data["c"]), territory=int(data["t"]), id=int(data["g"]))
        team = ivl_service.get_teams(championship=data["c"], id=int(data["s"]))

        message = preference_response(territory["name"], championship["name"], group["name"], team["name"])

        bot.send_message(chat_id, message, reply_markup=reply_markup, parse_mode='html')
    else:
        options = {}
        callback_data = f"{const.commands[const.PREFERENCE]}|0"
        options['Aggiungi'] = {'callback_data' : callback_data}

        reply_markup = tb.util.quick_markup(options, 1)
        bot.send_message(chat_id, "Ancora non ci sono preferenze... aggiungile!", reply_markup=reply_markup)

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
    bot.register_callback_query_handler(callback=ch.callback_preference, func=lambda call: str(call.data).split(sep='|')[0] == const.commands[const.PREFERENCE], pass_bot=True )

    #preference_service.init_file()
    db.create_connection()
    db.init_db()
    db.close_connection()

    if ENV == 'dev':
        bot.infinity_polling()

    if ENV == 'prod':
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
