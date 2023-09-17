import proto.entities.user_pb2 as user_pb
from manager.base_manager import BaseManager
from dao.user_dao import UserDA
from errors import PopupError

class UserManager(BaseManager):

    @property
    def dao(self):
        if self._dao is None:
            self._dao = UserDA()
        return self._dao

    def create_user(self, request):
        obj = self.create_obj(user_pb.User)
        obj.name = request.name
        return obj

    async def delete_user(self, request):
        user = user_pb.User()
        user.id = request.id
        await self.dao.delete_user(user)
        return user

    async def query_user(self, request):
        return await self.dao.get_user_by_id(request.id)

    async def update_user(self, request):
        user = await self.dao.get_user_by_id(request.id)
        if not user:
            raise PopupError("User Not Exists")
        user.name = request.name
        return user

    async def list_user(self, request):
        async for user in self.dao.list_user():
            yield self.PH.to_obj(user, user_pb.User)

    async def add_user(self, user):
        return await self.dao.add_user(user)

    async def do_update_user(self, user):
        return await self.dao.update_user(user)
