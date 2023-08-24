from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Bot

from codetrack import messages


async def btn_set_locale(call: CallbackQuery, state: FSMContext):
    user = call.from_user

    bot = Bot.get_current()
    locale = call.data.split(":")[1]
    await state.update_data({"locale": locale})


    markup = InlineKeyboardMarkup()
    message_text = messages.MSG_START_WITH_LOCALE(locale)

    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(
        user.id,
        message_text,
        reply_markup=markup,
    )