import upyog as upy

from agentflow.model.base import BaseModel
from agentflow.config import CONST, DEFAULT

class BaseStore(BaseModel):
    # TODO: implement required within BaseModel -> BaseObject.
    _REQUIRED = {
        "methods": [
            {
                "name": "ainsert_message",
                "async": True
            }
        ]
    }

class Store(BaseStore):
    def __init__(self, *args, **kwargs):
        super_  = super(BaseStore, self)
        super_.__init__(*args, **kwargs)

        self._setup()

    def _setup(self):
        path_db  = DEFAULT["AF_PATH_STORE_LOCAL"]
        self._db = upy.get_db_connection(path_db)

    async def ainsert_session(self, session):
        """
            Insert a Session into the Store.
        """
        db      = self._db
        table   = db[CONST["AF_TABLE_SESSION"]]

        session_id = session.session_id
        table.insert({
            "session_id": session_id
        })

    async def aget_messages(self, where=None, **kwargs):
        """
            Fetch messages from the Store.
        """
        db    = self._db
        table = db[CONST["AF_TABLE_MESSAGE"]]

        messages = table.find(where=where, **kwargs)

        return upy.sequencify(messages)

    async def ainsert_message(self, message):
        """
            Insert a message into the Store.
        """
        db = self._db

        session = message.session
        if session:
            session_id  = session.session_id
            session_ref = db[CONST["AF_TABLE_SESSION"]].find_one(
                session_id=session_id
            )

        actions = None
        if hasattr(message, "actions") and message.actions:
            actions = upy.dump_json(message.actions)

        table   = db[CONST["AF_TABLE_MESSAGE"]]
        table.insert({
            "role": message.role, "content": message.content,
            "session_id": session_id,
            "actions": actions
        })