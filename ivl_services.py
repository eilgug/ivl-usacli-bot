import requests

class IVLServices():

    _base_url = ""

    def get_classifica():
        res = requests.get("https://ivl.usacli.it/Classifica/158?_a=&inizio_stagione=2022-09-01T00:00:00.000Z&fine_stagione=2023-08-31T00:00:00.000Z")
        data = res.json()
        return data;

    def get_calendar(from_data, id_squadra = None):
        res = requests.get(f"https://ivl.usacli.it/PartiteData?girone_id=158&territorio_id=3&campionato_id=81&inizio_stagione={from_data}&fine_stagione=2023-08-31T00:00:00.000Z&societa_id=null&squadra_id={id_squadra}&pubblicato=1")
        data = res.json();
        return data
