import os
from dotenv import load_dotenv
import requests
import telebot as tb
import prettytable as pt

load_dotenv()

APY_KEY = os.getenv('API_KEY')
bot = tb.TeleBot(APY_KEY);

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

bot.infinity_polling()
