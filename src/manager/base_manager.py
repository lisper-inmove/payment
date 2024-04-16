from base import Base
from submodules.utils.misc import Misc
from submodules.utils.idate import IDate


class BaseManager(Base):

    def create_obj(self, cls):
        obj = cls()
        obj.id = Misc.uuid()
        if hasattr(obj, 'create_time'):
            obj.create_time = IDate.now_timestamp()
        if hasattr(obj, 'update_time'):
            obj.update_time = IDate.now_timestamp()
        return obj

    def update_obj(self, obj):
        if hasattr(obj, 'update_time'):
            obj.update_time = IDate.now_timestamp()
