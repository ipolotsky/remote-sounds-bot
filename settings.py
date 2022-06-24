import os
import json
from utils import helper


class Settings:
    IS_TEST = False

    @staticmethod
    def fb_creds():
        with open(f"FB_CREDS{'_TEST' if Settings.IS_TEST else ''}.json") as file:
            return json.load(file)

    @staticmethod
    def db_url():
        return os.environ[f"FB_DB_URL{'_TEST' if Settings.IS_TEST else ''}"]

    @staticmethod
    def bot_token():
        return os.environ[f"BAD_FEST_BOT_TOKEN{'_TEST' if Settings.IS_TEST else ''}"]

    @staticmethod
    def bot_name() -> str:
        return "RemoteSoundsBot" if Settings.IS_TEST else "RemoteSoundsBot"