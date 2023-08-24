from aiogram.contrib.fsm_storage.memory import BaseStorage
import sqlite3
import typing
import json


class SQLiteStorage(BaseStorage):

    def __init__(self, db_uri="./state.db"):
        self.db_uri = db_uri
        self.conn = sqlite3.connect(db_uri, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS state (
                user_id INT,
                chat_id INT,
                bucket TEXT,
                state TEXT,
                data TEXT
            )
        """)

    async def close(self):
        self.cursor.close()
        self.conn.close()

    async def wait_closed(self):
        pass

    def ensure_user(self, *,
                    chat: typing.Union[str, int, None] = None,
                    user: typing.Union[str, int, None] = None):

        self.cursor.execute("""
            SELECT user_id FROM state
            WHERE user_id=%d AND chat_id=%d
        """ % (int(user), int(chat)))
        result = self.cursor.fetchone()
        if not result:
            self.cursor.execute(
                "INSERT INTO state VALUES(%d, %d, '{}', '{}', '{}')"
                % (int(user), int(chat)))
            self.conn.commit()

    def json(self, value: typing.Union[str, dict]):
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False)
        elif isinstance(value, str):
            return json.loads(value)
        else:
            raise TypeError(
                "json method accepts only 'str' and 'dict' parameter types. Got '{}'".format(
            type(value)))

    async def fetch_from_db(self, *,
                            chat: typing.Union[str, int, None] = None,
                            user: typing.Union[str, int, None] = None,
                            field: str) -> list:
        self.check_address(chat=chat, user=user)
        self.cursor.execute("""
            SELECT %s FROM state
            WHERE user_id=%d AND chat_id=%d
        """ % (field, int(user), int(chat)))
        return self.cursor.fetchone()

    async def get_state(self, *,
                        chat: typing.Union[str, int, None] = None,
                        user: typing.Union[str, int, None] = None,
                        default: typing.Optional[str] = None) -> typing.Optional[str]:

        result = await self.fetch_from_db(chat=chat, user=user, field="state")
        return self.json(result[0]) if result else self.resolve_state(default)

    async def get_data(self, *,
                       chat: typing.Union[str, int, None] = None,
                       user: typing.Union[str, int, None] = None,
                       default: typing.Optional[typing.Dict] = None) -> typing.Dict:

        result = await self.fetch_from_db(chat=chat, user=user, field="data")
        return self.json(result[0]) if result else default

    async def set_state(self, *,
                        chat: typing.Union[str, int, None] = None,
                        user: typing.Union[str, int, None] = None,
                        state: typing.Optional[typing.AnyStr] = None):

        self.check_address(chat=chat, user=user)
        self.ensure_user(chat=chat, user=user)
        self.cursor.execute("""
            UPDATE state SET state='%s'
            WHERE user_id=%d AND chat_id=%d
        """ % (state, int(user), int(chat)))
        self.conn.commit()

    async def set_data(self, *,
                       chat: typing.Union[str, int, None] = None,
                       user: typing.Union[str, int, None] = None,
                       data: typing.Dict = None):

        self.check_address(chat=chat, user=user)
        self.ensure_user(chat=chat, user=user)
        if data:
            self.cursor.execute("""
                UPDATE state SET data='%s'
                WHERE user_id=%d AND chat_id=%d
            """ % (self.json(data), int(user), int(chat)))
        else:
            self.cursor.execute("DELETE FROM state WHERE user_id=%d AND chat_id=%d")
        self.conn.commit()

    async def update_data(self, *,
                          chat: typing.Union[str, int, None] = None,
                          user: typing.Union[str, int, None] = None,
                          data: typing.Dict = None,
                          **kwargs):
        data = data or {}
        temp_data = await self.get_data(chat=chat, user=user, default={})
        await self.set_data(chat=chat, user=user, data={**temp_data, **data})

    def has_bucket(self):
        return True

    async def get_bucket(self, *,
                         chat: typing.Union[str, int, None] = None,
                         user: typing.Union[str, int, None] = None,
                         default: typing.Optional[dict] = None) -> typing.Dict:

        result = await self.fetch_from_db(chat=chat, user=user, field="bucket")
        return self.json(result[0] if result else default)

    async def set_bucket(self, *,
                         chat: typing.Union[str, int, None] = None,
                         user: typing.Union[str, int, None] = None,
                         bucket: typing.Dict = None):

        self.check_address(chat=chat, user=user)
        self.ensure_user(chat=chat, user=user)
        if bucket:
            self.cursor.execute("""
                UPDATE state SET bucket='%s'
                WHERE user_id=%d AND chat_id=%d
            """ % (self.json(bucket), int(user), int(chat)))
            self.conn.commit()

    async def update_bucket(self, *,
                            chat: typing.Union[str, int, None] = None,
                            user: typing.Union[str, int, None] = None,
                            bucket: typing.Dict = None,
                            **kwargs):
        bucket = bucket or {}
        temp_bucket = await self.get_bucket(chat=chat, user=user, default={})
        await self.set_bucket(chat=chat, user=user, data={**temp_bucket, **bucket})
