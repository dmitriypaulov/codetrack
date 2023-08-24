from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram import Bot

from codetrack.i18n import LANGUAGES
from codetrack.i18n import _


async def cmd_start(message: Message, state: FSMContext):
    user = message.from_user

    print("start")
    language_is_set = False
    data = await state.get_data({})
    if "locale" in data:
        language_is_set = True

    if not language_is_set:
        markup = InlineKeyboardMarkup()
        for language in LANGUAGES[1:]:
            markup.row(InlineKeyboardButton(
                text=language[0],
                callback_data=f"set_locale:{language[1]}"
            ))
        markup.row(InlineKeyboardButton(
            text=_("Continue with English ☑️"),
            callback_data="set_locale:en"
        ))
        message_text = _("ℹ️ Before starting the bot you can set your interface language:")

    else:
        markup = InlineKeyboardMarkup()
        message_text = _("""<b>Codetrack</b>

🧑‍💻 Save and share useful code snippets in <b>Telegram</b> completely for <b>free</b>
                        """)

    await Bot.get_current().send_message(
        user.id,
        message_text,
        reply_markup=markup,
    )