import proto.api.api_demo_p2p as api_pb
from routers.base_router import BaseRouter
from manager.demo_manager import DemoManager
from submodules.utils.logger import Logger
from unify_response import UnifyResponse

logger = Logger()


class DemoRouter(BaseRouter):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    async def create(self, request: api_pb.DemoCreateRequest):
        manager = DemoManager()
        demo = manager.create_demo(request)
        await manager.add_demo(demo)
        return UnifyResponse.R(self.__create_common_response(demo))

    async def delete(self, request: api_pb.DemoDeleteRequest):
        manager = DemoManager()
        demo = await manager.delete_demo(request)
        return UnifyResponse.R(self.__create_common_response(demo))

    async def query(self, request: api_pb.DemoQueryRequest):
        manager = DemoManager()
        demo = await manager.query_demo(request)
        return UnifyResponse.R(self.__create_common_response(demo))

    async def update(self, request: api_pb.DemoUpdateRequest):
        manager = DemoManager()
        demo = await manager.update_demo(request)
        await manager.do_update_demo(demo)
        return UnifyResponse.R(self.__create_common_response(demo))

    async def list(self, request: api_pb.DemoListRequest):
        manager = DemoManager()
        result = api_pb.DemoListResponse()
        async for demo in manager.list_demo(request):
            result.demos.append(self.__create_common_response(demo))
        return UnifyResponse.R(result)

    async def tmp_GET(self):
        return UnifyResponse.R()

    async def tmp_POST(self, request: api_pb.DemoCreateRequest):
        manager = DemoManager()
        demo = manager.create_demo(request)
        await manager.add_demo(demo)
        response = api_pb.DemoCommonResponse()
        response.id = demo.id
        response.name = demo.name
        return UnifyResponse.R(response)

    def __create_common_response(self, demo):
        response = api_pb.DemoCommonResponse()
        if demo is None:
            return response
        response.id = demo.id
        response.name = demo.name
        response.createTime = demo.createTime
        response.updateTime = demo.updateTime
        return response
