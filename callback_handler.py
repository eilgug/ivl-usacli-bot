from telebot import types, TeleBot, util as tb_util
from ivl_services import IVLServices
from rensponse_helper import get_response_table, text_wrapping, PrettyTableColumnAlign

def callback_leaderboard(call : types.CallbackQuery, bot: TeleBot):
    """
    Handle all step to get leaderboard.
    STEP:
        - territory
        - championship
        - group (if is only one return the leaderboard)

    @params:
        - call : CallbackQuery
            - data : str => "classifica|<step>|id"
    """

    ivl_service = IVLServices()
    call_data = call.data.split("|")

    if call_data[1] == 'territory':
        championship_data = ivl_service.get_championship(territory=call_data[2])
        options = {}
        for championship in championship_data:
            callback_data = f"classifica|championship|{championship['id']}"
            options[championship['name']] = {'callback_data' : callback_data}

        reply_markup = tb_util.quick_markup(options, 2)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=reply_markup)

    if call_data[1] == 'championship':
        groups_data = ivl_service.get_groups(championship=call_data[2])
        options = {}
        for groups in groups_data:
            callback_data = f"classifica|group|{groups['id']}"
            options[groups['name']] = {'callback_data' : callback_data}

        reply_markup = tb_util.quick_markup(options, 2)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=reply_markup)

    if call_data[1] == 'group':
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
