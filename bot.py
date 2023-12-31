from codetrack.i18n import i18n, _
from codetrack.storage import SQLiteStorage
from pathlib import Path
from aiogram import Dispatcher
from aiogram import executor
from aiogram import Bot
import os

from handlers.commands.start import cmd_start
from handlers.buttons.set_locale import btn_set_locale



TOKEN = os.environ.get("CT_BOT_TOKEN")
STORAGE_URI = os.environ.get(
    "CT_BOT_STORAGE_URI",
    (Path(__file__).parent/"state.db").absolute()
)

bot = Bot(
    token=TOKEN,
    parse_mode="HTML",
    disable_web_page_preview=True
)
dispatcher = Dispatcher(bot, storage=SQLiteStorage(STORAGE_URI))
dispatcher.middleware.setup(i18n)

dispatcher.register_message_handler(cmd_start, commands=["start"], state="*")
dispatcher.register_callback_query_handler(btn_set_locale,
    lambda call: call.data.startswith("set_locale:"), state="*")

executor.start_polling(dispatcher)
