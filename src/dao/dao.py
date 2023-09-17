from pymongo.errors import DuplicateKeyError

import proto.entities.user_pb2 as user_pb
from base import Base
from dao.mongodb import MongoDBHelper
from errors import PopupError
from submodules.utils.logger import Logger

logger = Logger()


class UserDA(MongoDBHelper, Base):

    coll = "___user_db___users___"

    async def add_user(self, user):
        json_data = self.PH.to_dict(user)
        try:
            await self.insert_one(json_data)
        except DuplicateKeyError as ex:
            logger.error(ex)
            raise PopupError("Already add this user")

    async def update_user(self, user):
        matcher = {"id": user.id}
        json_data = self.PH.to_dict(user)
        await self.update_one(matcher, json_data)

    async def delete_user(self, user):
        matcher = {"id": user.id}
        return await self.delete_one(matcher)

    async def query_user(self, user):
        matcher = {"id": user.id}
        return await self.find_one(matcher)

    async def list_user(self):
        matcher = {}
        users = self.find_many(matcher)
        async for user in users:
            yield user

    async def get_user_by_id(self, id):
        matcher = {"id": id}
        user = await self.find_one(matcher)
        return self.PH.to_obj(user, user_pb.User)
