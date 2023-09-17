import proto.api.api_user_p2p as api_pb
from routers.base_router import BaseRouter
from manager.user_manager import UserManager
from submodules.utils.logger import Logger
from unify_response import UnifyResponse

logger = Logger()


# @router.post("/create")
# async def create_user(
#         request: api_pb.UserCreateRequest
# ):
#     manager = UserManager()
#     user = manager.create_user(request)
#     manager.add_user(user)
#     response = api_pb.UserCreateResponse()
#     response.id = user.id
#     response.name = user.name
#     return UnifyResponse.R(response)

# @router.post("/delete")
# async def delete_user(
#         request: api_pb.UserCreateRequest
# ):
#     manager = UserManager()
#     user = manager.create_user(request)
#     manager.add_user(user)
#     response = api_pb.UserCreateResponse()
#     response.id = user.id
#     response.name = user.name
#     return UnifyResponse.R(response)

# @router.post("/get")
# async def query_user(
#         request: api_pb.UserQueryRequest
# ):
#     manager = UserManager()
#     user = manager.get_user(request)
#     response = api_pb.UserCommonResponse()
#     response.id = user.id
#     response.name = user.name
#     return UnifyResponse.R(response)


class UserRouter(BaseRouter):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    async def create(self, request: api_pb.UserCreateRequest):
        manager = UserManager()
        user = manager.create_user(request)
        await manager.add_user(user)
        return UnifyResponse.R(self.__create_common_response(user))

    async def delete(self, request: api_pb.UserDeleteRequest):
        manager = UserManager()
        user = await manager.delete_user(request)
        return UnifyResponse.R(self.__create_common_response(user))

    async def query(self, request: api_pb.UserQueryRequest):
        manager = UserManager()
        user = await manager.query_user(request)
        return UnifyResponse.R(self.__create_common_response(user))

    async def update(self, request: api_pb.UserUpdateRequest):
        manager = UserManager()
        user = await manager.update_user(request)
        await manager.do_update_user(user)
        return UnifyResponse.R(self.__create_common_response(user))

    async def list(self, request: api_pb.UserListRequest):
        manager = UserManager()
        result = api_pb.UserListResponse()
        async for user in manager.list_user(request):
            result.users.append(self.__create_common_response(user))
        return UnifyResponse.R(result)

    async def tmp_GET(self):
        return UnifyResponse.R()

    async def tmp_POST(self, request: api_pb.UserCreateRequest):
        manager = UserManager()
        user = manager.create_user(request)
        await manager.add_user(user)
        response = api_pb.UserCommonResponse()
        response.id = user.id
        response.name = user.name
        return UnifyResponse.R(response)

    def __create_common_response(self, user):
        response = api_pb.UserCommonResponse()
        if user is None:
            return response
        response.id = user.id
        response.name = user.name
        response.createTime = user.createTime
        response.updateTime = user.updateTime
        return response
