from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram import Bot

from codetrack.i18n import LANGUAGES
from codetrack import messages


async def cmd_start(message: Message, state: FSMContext):
    user = message.from_user

    language_is_set = False
    data = await state.get_data({})
    if "locale" in data:
        language_is_set = True

    markup = InlineKeyboardMarkup()
    if not language_is_set:
        for language in LANGUAGES[1:]:
            markup.row(InlineKeyboardButton(
                text=language[0],
                callback_data=f"set_locale:{language[1]}"
            ))
        markup.row(InlineKeyboardButton(
            text=messages.BTN_CONTINUE_WITH_ENGLISH,
            callback_data="set_locale:en"
        ))
        message_text = messages.MSG_START_NO_LOCALE

    else:
        message_text = messages.MSG_START

    await Bot.get_current().send_message(
        user.id,
        message_text,
        reply_markup=markup,
    )