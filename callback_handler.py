import constants as const
import json
from datetime import date, datetime
from telebot import types, TeleBot, util as tb_util
from ivl_services import IVLServices
from rensponse_helper import get_response_table, text_wrapping
from db import Db

def callback_preference(call: types.CallbackQuery, bot: TeleBot):
    """
    Handle all step to get all data to be stored as preference.
    STEP:
        - territory (t)
        - championship (c)
        - group (if is only one return the leaderboard) (g)
        - team (s)

    @params:
        - call : CallbackQuery
            - data : str => "classifica|<step>|id"
        - bot : Telebot => Injected from register_callback_handler
    """

    ivl_service = IVLServices()
    call_data = call.data.split("|")

    if call_data[1] == "R":
        db = Db(r"ivl_bot.db")
        db.create_connection()
        db.remove_preference(call.message.chat.id)
        db.close_connection()

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(chat_id=call.message.chat.id, text="Preferenze rimosse!")

    if call_data[1] == "0":
        territory_data = ivl_service.get_territory()
        options = {}
        for territory in territory_data:
            callback_data = f"{const.commands[const.PREFERENCE]}|{const.steps[const.TERRITORY]}|{territory['id']}"
            options[territory['name']] = {'callback_data' : callback_data}

        reply_markup = tb_util.quick_markup(options, 2)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(chat_id=call.message.chat.id, text="SELEZIONA UN TERRITORIO", reply_markup=reply_markup)

    if call_data[1] == const.steps[const.TERRITORY]:
        territory_id = call_data[2]
        championship_data = ivl_service.get_championship(territory=territory_id)
        extra_args = {"t" : territory_id}
        options = {}
        for championship in championship_data:
            callback_data = f"{const.commands[const.PREFERENCE]}|{const.steps[const.CHAMPIONSHIP]}|{championship['id']}|{str(extra_args)}"
            options[championship['name']] = {'callback_data' : callback_data}

        reply_markup = tb_util.quick_markup(options, 2)
        bot.edit_message_text(text="SELEZIONA UN CAMPIONATO", chat_id=call.message.chat.id, message_id=call.message.id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=reply_markup)

    if call_data[1] == const.steps[const.CHAMPIONSHIP]:
        championship_id = call_data[2]
        groups_data = ivl_service.get_groups(championship=championship_id)
        extra_args = eval(call_data[3])
        extra_args['c'] = championship_id
        options = {}
        for groups in groups_data:
            callback_data = f"{const.commands[const.PREFERENCE]}|{const.steps[const.GROUP]}|{groups['id']}|{str(extra_args)}"
            options[groups['name']] = {'callback_data' : callback_data}

        reply_markup = tb_util.quick_markup(options, 2)
        bot.edit_message_text(text="SELEZIONA UN GIRONE", chat_id=call.message.chat.id, message_id=call.message.id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=reply_markup)

    if call_data[1] == const.steps[const.GROUP]:
        group_id = call_data[2]
        extra_args = eval(call_data[3])
        extra_args['g'] = group_id
        teams_data = ivl_service.get_teams(championship=extra_args['c'])
        options = {}
        for teams in teams_data:
            callback_data = f"{const.commands[const.PREFERENCE]}|{const.steps[const.TEAMS]}|{teams['id']}|{str(extra_args)}"
            options[teams['name']] = {'callback_data' : callback_data}

        reply_markup = tb_util.quick_markup(options, 2)
        bot.edit_message_text(text="SELEZIONA UNA SQUADRA", chat_id=call.message.chat.id, message_id=call.message.id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=reply_markup)

    if call_data[1] == const.steps[const.TEAMS]:
        team_id = call_data[2]
        extra_args = eval(call_data[3])
        extra_args['s'] = team_id

        db = Db(r"ivl_bot.db")
        db.create_connection()
        db.set_or_update_preference(call.message.chat.id, json.dumps(extra_args))
        db.close_connection()

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(chat_id=call.message.chat.id, text="Le tue preferenze sono state aggiornate!")


def callback_leaderboard(call: types.CallbackQuery, bot: TeleBot):
    """
    Handle all step to get leaderboard.
    STEP:
        - territory
        - championship
        - group (if is only one return the leaderboard)

    @params:
        - call : CallbackQuery
            - data : str => "classifica|<step>|id"
        - bot : Telebot => Injected from register_callback_handler
    """

    ivl_service = IVLServices()
    call_data = call.data.split("|")

    if call_data[1] == const.steps[const.TERRITORY]:
        championship_data = ivl_service.get_championship(territory=call_data[2])
        options = {}
        for championship in championship_data:
            callback_data = f"{const.commands[const.LEADERBOARD]}|{const.steps[const.CHAMPIONSHIP]}|{championship['id']}"
            options[championship['name']] = {'callback_data' : callback_data}

        reply_markup = tb_util.quick_markup(options, 2)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=reply_markup)

    if call_data[1] == const.steps[const.CHAMPIONSHIP]:
        groups_data = ivl_service.get_groups(championship=call_data[2])
        options = {}
        for groups in groups_data:
            callback_data = f"{const.commands[const.LEADERBOARD]}|{const.steps[const.GROUP]}|{groups['id']}"
            options[groups['name']] = {'callback_data' : callback_data}

        reply_markup = tb_util.quick_markup(options, 2)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=reply_markup)

    if call_data[1] == const.steps[const.GROUP]:
        leaderboard = ivl_service.get_leaderboard(group=call_data[2])
        # delete query message
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

        # return leaderboard
        data = []
        for row in leaderboard:
            name = text_wrapping(row['name'])
            data.append( [ name, row['Punteggio'] ] )

        leaderboard_table = get_response_table( ['SQUADRA', 'PTS'], data)
        bot.send_message(chat_id=call.message.chat.id, text=leaderboard_table, parse_mode='html')


def callback_calendar_nextmatch(call: types.CallbackQuery, bot: TeleBot):
    """
    Handle all step to get calendar or the next match.
    STEP:
        - territory
        - championship
        - group (if is only one return the leaderboard)
        - team

    @params:
        - call : CallbackQuery
            - data : str => "classifica|<step>|id|extra_args"
        - bot : Telebot => Injected from register_callback_handler
    """

    ivl_service = IVLServices()
    call_data = call.data.split("|")
    command = call_data[0]

    if call_data[1] == const.steps[const.TERRITORY]:
        territory_id = call_data[2]
        championship_data = ivl_service.get_championship(territory=territory_id)
        extra_args = {"territory" : territory_id}
        options = {}
        for championship in championship_data:
            callback_data = f"{command}|{const.steps[const.CHAMPIONSHIP]}|{championship['id']}|{str(extra_args)}"
            options[championship['name']] = {'callback_data' : callback_data}

        reply_markup = tb_util.quick_markup(options, 2)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=reply_markup)

    if call_data[1] == const.steps[const.CHAMPIONSHIP]:
        championship_id = call_data[2]
        groups_data = ivl_service.get_groups(championship=championship_id)
        extra_args = eval(call_data[3])
        extra_args['championship'] = championship_id
        options = {}
        for groups in groups_data:
            callback_data = f"{command}|{const.steps[const.GROUP]}|{groups['id']}|{str(extra_args)}"
            options[groups['name']] = {'callback_data' : callback_data}

        reply_markup = tb_util.quick_markup(options, 2)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=reply_markup)

    if call_data[1] == const.steps[const.GROUP]:
        group_id = call_data[2]
        extra_args = eval(call_data[3])
        extra_args['group'] = group_id
        teams_data = ivl_service.get_teams(championship=extra_args['championship'])
        options = {}
        for teams in teams_data:
            callback_data = f"{command}|{const.steps[const.TEAMS]}|{teams['id']}|{str(extra_args)}"
            options[teams['name']] = {'callback_data' : callback_data}

        reply_markup = tb_util.quick_markup(options, 2)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=reply_markup)

    if call_data[1] == const.steps[const.TEAMS]:
        team_id = call_data[2]
        extra_args = eval(call_data[3])
        today = None
        if command == const.commands[const.NEXT_MATCH]:
            today = date.today()

        calendar = ivl_service.get_calendar(championship=extra_args['championship'], territory=extra_args['territory'], group=extra_args['group'], team=team_id, season_start=today)

        # delete query message
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        # return calendar/nextmatch
        if command == const.commands[const.CALENDAR]:
            data = []
            name = ""
            for row in calendar:
                d = datetime.strptime(row['DataGioco'], "%Y-%m-%d %H:%M:%S")
                hour = d.strftime('%H:%M')
                day = d.strftime('%d/%m/%y')

                if row['squadra_casa_id'] == int(team_id):
                    name = row['SquadraOspite']

                if row['squadra_ospite_id'] == int(team_id):
                    name = row['SquadraCasa']

                data.append( [ name, f"{day}\n{hour}"] )

            calendar_table = get_response_table( ['VS', 'DATA/ORA'], data, max_width=10)
            bot.send_message(chat_id=call.message.chat.id, text=calendar_table, parse_mode='html')

        if command == const.commands[const.NEXT_MATCH]:
            next_match_data = calendar[0]

            data = [[next_match_data['SquadraCasa'], next_match_data['SquadraOspite']]]
            res_message = get_response_table( ['CASA', 'OSPITI'], data, max_width=10)

            d = datetime.strptime(next_match_data['DataGioco'], "%Y-%m-%d %H:%M:%S")
            hour = d.strftime('%H:%M')
            day = d.strftime('%d/%m/%Y')
            res_message += f"\n\n<b>Data:</b> {day} | <b>Ora:</b> {hour}"

            bot.send_message(call.message.chat.id, res_message, parse_mode='html')
            bot.send_location(call.message.chat.id, next_match_data['Palestra_lat'], next_match_data['Palestra_long'])
