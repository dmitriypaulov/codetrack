from aiogram.contrib.middlewares.i18n import I18nMiddleware as I18n
from aiogram import Dispatcher
from aiogram import types
from pathlib import Path
import typing


class I18nMiddleware(I18n):
    async def get_user_locale(self, action: str, args: typing.Tuple[typing.Any]) -> str:
        user: types.User = types.User.get_current()
        dispatcher: Dispatcher = Dispatcher.get_current()
        state = dispatcher.current_state(chat=user.id, user=user.id)

        data = await state.get_data({})
        return data.get("locale", "en")

i18n = I18nMiddleware(
    domain="codetrack",
    path=Path(__file__).parent.parent/"locales"
)
_ = i18n.lazy_gettext
LANGUAGES = [
    (_("🇺🇸 English"), "en"),
    (_("🇺🇦 Ukrainian"), "uk"),
]