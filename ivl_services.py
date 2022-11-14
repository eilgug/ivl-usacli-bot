import requests
from datetime import date


class IVLServices():

    def __init__(self):
        self._base_url: str = 'https://ivl.usacli.it/'

    def _call_api(self, api: str, payload = None):
        res = requests.get(api, params=payload)
        return res.json();

    def get_territory(self):
        """
        Call 'ListaTerritoriPubblica' api

        @return: List of territory
        @rtype: json
        """
        api: str = self._base_url + 'ListaTerritoriPubblica'
        return self._call_api(api)

    def get_championship(self, territory: int, season_start = None, season_end = None):
        """Return championship list and data filtered by territory"""
        api: str = self._base_url + 'CampionatiData'

        payload = {
            "territorio_id" : territory,
            "inizio_stagione" : season_start,
            "fine_stagione" : season_end,
        }

        return self._call_api(api, payload)

    def get_groups(self, championship: int, territory: int = None, season_start = None, season_end = None, returnall:int = 1):
        """Return all groups filtered by championship"""
        api: str = self._base_url + 'GironiData'

        payload = {
            "territorio_id" : territory,
            "campionato_id" : championship,
            "inizio_stagione" : season_start,
            "fine_stagione" : season_end,
            "returnall" : returnall
        }

        return self._call_api(api, payload)

    def get_teams(self, championship: int):
        """Return teams registered to a championship"""
        api: str = self._base_url + 'SquadreIscritteACampionato/' + championship

        return self._call_api(api)

    def get_leaderboard(self, group: int, season_start = None, season_end = None):
        """Return leaderboard filtered by group_id"""
        api: str = self._base_url + 'Classifica/' + group

        payload = {
            "inizio_stagione" : season_start,
            "fine_stagione" : season_end,
        }

        return self._call_api(api, payload)

    # TODO: reduce number of params pass to function (maybe pass **args or a dict)
    def get_calendar(self, territory: int, championship: int, group: int, team: int, societa: int = None, season_start: str = None, season_end: str = None):
        """Return calendar filtered group_id and team"""

        api: str = self._base_url + 'PartiteData'

        current_year = date.today().year
        if season_end is None:
            season_end = f"{current_year + 1}-08-31"
        if season_start is None:
            season_start = f"{current_year}-09-01"

        payload = {
            "territorio_id" : territory,
            "campionato_id" : championship,
            "girone_id" : group,
            "societa_id" : societa,
            "squadra_id" : team,
            "inizio_stagione" : season_start,
            "fine_stagione" : season_end,
            "pubblicato" : 1,
        }

        return self._call_api(api, payload)
