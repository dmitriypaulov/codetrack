from codetrack.i18n import _

MSG_START_NO_LOCALE = _("ℹ️ Before starting the bot you can set your interface language:")
MSG_START_WITH_LOCALE = lambda locale: _("""<b>Codetrack</b>

🧑‍💻 Save and share useful code snippets in <b>Telegram</b> completely for <b>free</b>
""", locale=locale)
MSG_START = _("""<b>Codetrack</b>

🧑‍💻 Save and share useful code snippets in <b>Telegram</b> completely for <b>free</b>
""")


# Button texts

BTN_CONTINUE_WITH_ENGLISH = _("Continue with English ☑️")