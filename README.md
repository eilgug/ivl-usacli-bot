# IVL US-ACLI BOT

## START PROJECT FOR DEVELOPMENT
> Setup environt install `requirements.txt` globally or in a virtual env and setup `API_KEY` env variable with your bot API key.

### START BOT WITHOUT FLASK

- Set variable env `ENVIRONMENT = 'dev'`
- Run bot `python <file-name>.py`

### START BOT WITH FLASK WITH NGROK

- Set variable env `ENVIRONMENT = 'prod'`
- Start ngrok envirorment with `ngrok http <flask-port>`
- Copy ngrock host address in `.env` file (Had `/` at the end of the url if missing)
- Run flask server `python <file-name>.py`
- Start bot calling `localhost:<port>`

## COMMANDS
`/classifica` ⇒ Return leaderboard of a selected tournament and group

`/calendario` ⇒ Return calender filtered by a specific team

`/nextmatch` ⇒ Return info (home team, guest team, date, hour and position) of the next match filtered by a specific team

`/preferenze` ⇒ Give you possibility to set your favourite *territory*, *championship*, *group* and *team* so you don't have to select them every time.

_made by [@eilgug](https://github.com/eilgug)_
_more info [here](https://eilgug.notion.site/IVL-US-ACLI-BOT-e2dbe44d4e35491f940e70a9ddc519c1)
