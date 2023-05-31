from submodules.utils.sys_env import SysEnv

try:
    from base_cls import BaseCls
except:
    class BaseCls:
        pass


class Payment(BaseCls):

    def generate_notify_url(self, spec=None):
        ret = f"https://{self.domain}/transaction/notify"
        # 如果是这种回调需要在view处特殊处理
        if spec is not None:
            ret = f"{ret}/{spec}"
        return ret
