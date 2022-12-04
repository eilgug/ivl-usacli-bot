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
- `/start`
- `/alive`
- `/classifica`
- `/nextmatch`
- `/calendario`
- `/preferenze`

_made by [@eilgug](https://github.com/eilgug)_
