import os
import re
import time
import importlib.util
import inspect

from fastapi import APIRouter
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from submodules.utils.logger import Logger
from submodules.utils.sys_env import SysEnv
from errors import Error
from unify_response import UnifyResponse

logger = Logger()


class RouterHelper:

    pattern = re.compile('(?!^)([A-Z]+)')

    def __init__(self, app, directory):
        self.directory = directory
        self.routers = dict()
        self.app = app

    def load_router(self, path=None):
        """加载所有router."""
        if path is None:
            root_dir = SysEnv.get(SysEnv.APPROOT)
            path = os.path.join(root_dir, self.directory)
        for root, dirs, files in os.walk(path):
            for directory in dirs:
                self.load_router(os.path.join(root, directory))
            for _f in files:
                self.load_router_from_file(os.path.join(root, _f))

    def load_router_from_file(self, filepath):
        """加载某一个router."""
        if not filepath.endswith("py"):
            return
        spec = importlib.util.spec_from_file_location(self.directory, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for key, value in module.__dict__.items():
            if not inspect.isclass(value):
                continue
            if not issubclass(value, APIRouter):
                continue
            if value == APIRouter:
                continue
            if value.__name__ == "BaseRouter":
                continue
            snake_name = self.pattern.sub(r'_\1', value.__name__).lower()
            prefix = "-".join(snake_name.split("_")[:-1])
            router = value(prefix=f"/{prefix}")
            r = module.__dict__.get('router')
            self.app.include_router(router)
            logger.info(f"create router: {prefix} {router} {r}")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.3.124:9000"],  # 允许的源列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许的方法
    allow_headers=["*"],  # 允许的头部
)


@app.middleware("http")
async def cache_error(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
    except Error as e:
        result = UnifyResponse.R(rs=(e.code, e.msg))
        return JSONResponse(result)
    except Exception as e:
        logger.error(e)
        raise e
    process_time = time.time() - start_time
    logger.info(f"Api processTime: {request.url} {process_time}")
    return response

RouterHelper(app, "routers").load_router()
