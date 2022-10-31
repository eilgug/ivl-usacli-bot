import os
from flask import Flask, request
from dotenv import load_dotenv
import requests
import telebot as tb
import prettytable as pt

server = Flask(__name__)
load_dotenv()

API_KEY = os.getenv('API_KEY')
HOST = os.getenv('HOST');
bot = tb.TeleBot(API_KEY);

@bot.message_handler(commands=['alive'])
def test(message):
    bot.reply_to(message, "Hey! Sono vivo!");

@bot.message_handler(commands=['classifica'])
def get_classifica(message):
    res = requests.get("https://ivl.usacli.it/Classifica/158?_a=&inizio_stagione=2022-09-01T00:00:00.000Z&fine_stagione=2023-08-31T00:00:00.000Z")
    data = res.json()

    classifica = pt.PrettyTable(['Squadra', 'Pts'], max_width=15)
    classifica.hrules = pt.ALL
    for row in data:
        classifica.add_row([row['name'], row['Punteggio']])

    print(classifica)

    bot.send_message(message.chat.id, "Ecco la classifica:")
    bot.send_message(message.chat.id, f"<pre>{classifica}</pre>", parse_mode='html')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

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
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
