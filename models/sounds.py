import collections
import random
import string
from datetime import datetime
from telegram import TelegramError
from persistence.firebase_persistence import FirebasePersistence
from utils import helper

store = FirebasePersistence()


class Sounds:

    def __init__(self):
        self._id = None
        self._data = {}

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _id: int):
        self._id = _id

    @property
    def name(self):
        return helper.safe_list_get(self._data, "name", None)

    @name.setter
    def name(self, name: str):
        raise TelegramError("Direct setter for name is denied")

    def save(self):
        store.sounds.child(str(self._id)).update(self._data)

    def tech_data(self):
        return self._data

    # Functions

    def load(self):
        if not self._id:
            raise TelegramError(f"Отсутстует id")

        _data = store.sounds.child(str(self._id)).get()
        if not _data:
            raise TelegramError(f"Нет данных по арт запросу с id: {self._id}")

        self._data = _data

    @staticmethod
    def get(_id: str, data=None):
        art_request = Sounds()
        art_request.id = _id
        if data:
            art_request._data = data
        else:
            art_request.load()

        return art_request

    @staticmethod
    def exists(_id: str):
        return bool(store.sounds.child(_id).get())

    @classmethod
    def all(cls, sort: str = "order", reverse=True):
        fb_goods = store.sounds.order_by_child("id").get()
        fb_goods = fb_goods if fb_goods else []
        return [cls.get(sound["id"], sound) for sound in fb_goods]

