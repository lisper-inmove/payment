from pymongo.errors import DuplicateKeyError

import proto.entities.demo_pb2 as demo_pb
from base import Base
from dao.mongodb import MongoDBHelper
from errors import PopupError
from submodules.utils.logger import Logger

logger = Logger()


class DemoDA(MongoDBHelper, Base):

    coll = "___demo_db___demos___"

    async def add_demo(self, demo):
        json_data = self.PH.to_dict(demo)
        try:
            await self.insert_one(json_data)
        except DuplicateKeyError as ex:
            logger.error(ex)
            raise PopupError("Already add this demo")

    async def update_demo(self, demo):
        matcher = {"id": demo.id}
        json_data = self.PH.to_dict(demo)
        await self.update_one(matcher, json_data)

    async def delete_demo(self, demo):
        matcher = {"id": demo.id}
        return await self.delete_one(matcher)

    async def query_demo(self, demo):
        matcher = {"id": demo.id}
        return await self.find_one(matcher)

    async def list_demo(self):
        matcher = {}
        demos = self.find_many(matcher)
        async for demo in demos:
            yield demo

    async def get_demo_by_id(self, id):
        matcher = {"id": id}
        demo = await self.find_one(matcher)
        return self.PH.to_obj(demo, demo_pb.Demo)
