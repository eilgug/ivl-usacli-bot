import os
import json

class PreferenceService:

    def __init__(self, file_name='preference'):
        self.file_name: str = f"{file_name}"

    def init_file(self):
        if not os.path.exists(f"{self.file_name}.json"):
            with open(f"{self.file_name}.json", "w+") as f:
                preference = {}
                preference['preference'] = {}
                f.write(json.dumps(preference))

    def get_preference(self, chat_id):
        with open(f"{self.file_name}.json", "r") as f:
            preference = json.load(f)

            if chat_id in preference['preference']:
                return preference['preferenze'][chat_id]
            else:
                return False

    def save_preference(self, chat_id, data):

        chat_id = str(chat_id)
        pref = {chat_id : data}

        with open(f"{self.file_name}.json", "r") as f:
            preference = json.load(f)

            preference['preference'][chat_id] = data


        with open(f"{self.file_name}.json", "w") as f:
            json.dump(preference, f)
