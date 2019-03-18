import requests
import json
import datetime
import pytz


class R6TabAPI:
    @staticmethod
    def find_by_username(username):
        username_query = f"https://r6tab.com/api/search.php?platform=uplay&search={username}"
        r = requests.get(username_query)
        data = json.loads(r.content)
        print("results", data)
        result_set = None

        for result in data['results']:
            if result['p_name'] == username:
                result_set = result

        return result_set

    @staticmethod
    def find_by_id(id):
        id_query = f"https://r6tab.com/api/player.php?p_id={id}"
        r = requests.get(id_query)
        data = json.loads(r.content)

        return data

    @staticmethod
    def update_meta(meta, data):
        if meta.player.username != data["p_name"]:
            meta.player.username = data["p_name"]
            meta.player.save()

        meta.current_mmr = int(data['p_currentmmr'])
        meta.current_rank = int(data['p_currentrank'])

        meta.NA_mmr = int(data['p_NA_currentmmr'])
        meta.NA_rank = int(data['p_NA_rank'])

        meta.EU_mmr = int(data['p_EU_currentmmr'])
        meta.EU_rank = int(data['p_EU_rank'])

        meta.AS_mmr = int(data['p_AS_currentmmr'])
        meta.AS_rank = int(data['p_AS_rank'])
        meta.last_queried = datetime.datetime.now(tz=pytz.UTC)
        meta.save()
        return meta

    @staticmethod
    def save_defaults(player, user_data):
        player.username = user_data['p_name']
        player.p_user = user_data['p_user']
        player.current_mmr = int(user_data['p_currentmmr'])
        player.current_rank = int(user_data['p_currentrank'])
        player.current_level = int(user_data['p_level'])
        player.last_queried = datetime.datetime.now(tz=pytz.UTC)
        player.save()
        return player
