import time
from fastapi import APIRouter

from errors import PopupError
from submodules.utils.logger import Logger

logger = Logger()


class BaseRouter(APIRouter):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.post("/create")(self.create)
        self.post("/update")(self.update)
        self.post("/delete")(self.delete)
        self.post("/query")(self.query)
        self.post("/list")(self.list)
        members = dir(self)
        for member in members:
            if member.endswith("GET"):
                prefix = "_".join(member.split("_")[:-1])
                self.get(f"/{prefix}")(getattr(self, member))
            if member.endswith("POST"):
                prefix = "_".join(member.split("_")[:-1])
                self.post(f"/{prefix}")(getattr(self, member))

    async def create(self, request):
        raise PopupError("Method Not Supported")

    async def update(self, request):
        raise PopupError("Method Not Supported")

    async def delete(self, request):
        raise PopupError("Method Not Supported")

    async def query(self, request):
        raise PopupError("Method Not Supported")

    async def list(self, request):
        raise PopupError("Method Not Supported")

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        logger.warning(f"Every {name} will be shared by requests!!!")
