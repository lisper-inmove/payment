import time
from fastapi import APIRouter

from errors import PopupError


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
        setattr(BaseRouter, "__setattr__", self.__setattr)

    async def create(self, request):
        raise PopupError("Method Not Supported")

    async def update(self, request):
        raise PopupError("Method Not Supported")

    async def delete(self, request):
        raise PopupError("Method Not Supported")

    async def query(self, request):
        raise PopupError("Method Not Supported")

    async def get_list(self, request):
        raise PopupError("Method Not Supported")

    def __setattr(self, name, value):
        raise Exception("Not Supported")
