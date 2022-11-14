from flask import Blueprint, render_template, request
# from ivl_services import IVLServices
# from datetime import date, datetime
# import prettytable as pt

blueprint = Blueprint('api', __name__)

# @blueprint.route("/classifica", methods = ['GET'])
# def get_classifica():
#     data = IVLServices.get_classifica()

#     classifica = pt.PrettyTable(['Squadra', 'Pts'])
#     classifica.hrules = pt.ALL
#     for row in data:
#         classifica.add_row([row['name'], row['Punteggio']])

#     return render_template('classifica_table.html', classifica=classifica)

# @blueprint.route("/calendario", methods = ['GET'])
# def get_calendario():
#     req_data = request.args
#     id_squadra = req_data.get('id_squadra') # santa valeria
#     date_from = '2022-09-01T00:00:00.000Z'

#     data = IVLServices.get_calendar(date_from, id_squadra)
#     calendar_table = pt.PrettyTable(['HOME', 'VS', 'DATA/ORA', 'INDIRIZZO'], max_width = 10)
#     calendar_table.hrules = pt.ALL

#     for row in data:
#         d = datetime.strptime(row['DataGioco'], "%Y-%m-%d %H:%M:%S")
#         hour = d.strftime('%H:%M')
#         day = d.strftime('%d/%m/%Y')

#         if row['squadra_casa_id'] == id_squadra:
#             calendar_table.add_row(["X",row['SquadraOspite'], f"{day}\n{hour}"])
#         else:
#             calendar_table.add_row([" ",row['SquadraCasa'], f"{day}\n{hour}"])

#     print(calendar_table)

#     return render_template('calendario_table.html', calendar_table=calendar_table)
