#!/usr/bin/env python
# pylint: disable=C0116
import json
import logging
from pprint import pprint

from telegram import ReplyKeyboardMarkup, Update, ParseMode, TelegramError, ReplyKeyboardRemove, LabeledPrice
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.error_handler import error_handler
from models.sounds import Sounds
from persistence.firebase_persistence import FirebasePersistence
from settings import Settings
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext, PreCheckoutQueryHandler,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

store = FirebasePersistence()

CALLBACK_SOUND = "Sound"


def action_start(update: Update, context: CallbackContext) -> None:
    sounds = Sounds.all()
    markup_buttons = []
    i = 0
    batch = []
    for sound in sounds:
        batch.append(InlineKeyboardButton(text=sound.name, callback_data=f"{str(CALLBACK_SOUND)}:{sound.id}"))
        if i % 2 == 0:
            markup_buttons.append(batch)
            batch = []
        i += 1

    update.message.reply_text(
        text=f"Выбери звук:",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(markup_buttons))
    return None


# Main endpoint
def main() -> None:
    updater = Updater(Settings.bot_token(), persistence=store)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(MessageHandler(Filters.text, action_start))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
