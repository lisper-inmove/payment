import proto.entities.demo_pb2 as demo_pb
from manager.base_manager import BaseManager
from dao.demo_dao import DemoDA
from errors import PopupError

class DemoManager(BaseManager):

    @property
    def dao(self):
        if self._dao is None:
            self._dao = DemoDA()
        return self._dao

    def create_demo(self, request):
        obj = self.create_obj(demo_pb.Demo)
        obj.name = request.name
        return obj

    async def delete_demo(self, request):
        demo = demo_pb.Demo()
        demo.id = request.id
        await self.dao.delete_demo(demo)
        return demo

    async def query_demo(self, request):
        return await self.dao.get_demo_by_id(request.id)

    async def update_demo(self, request):
        demo = await self.dao.get_demo_by_id(request.id)
        if not demo:
            raise PopupError("Demo Not Exists")
        demo.name = request.name
        return demo

    async def list_demo(self, request):
        async for demo in self.dao.list_demo():
            yield self.PH.to_obj(demo, demo_pb.Demo)

    async def add_demo(self, demo):
        return await self.dao.add_demo(demo)

    async def do_update_demo(self, demo):
        return await self.dao.update_demo(demo)
