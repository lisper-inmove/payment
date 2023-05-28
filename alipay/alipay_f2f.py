"""
支付宝当面付
"""

from alipay import AliPay
from alipay.utils import AliPayConfig

from submodules.utils.sys_env import SysEnv


class AlipayF2F:

    def __init__(self, appid, subject=None):
        if subject is None:
            subject = "当面付"
        self.subject = subject
        self.APPID = SysEnv.get("ALIPAY_APPID")
        self.web_url = SysEnv.get("ALIPAY_WEB_URL")
        self.app_private_key_string = open(SysEnv.get("APP_PRIVATE_KEY_FILE")).read()
        self.alipay_public_key_string = open(SysEnv.get("ALIPAY_PUBLIC_KEY_FILE")).read()
        self.notify_url = f"{self.web_url}/alipay/notify"
        self.alipay = AliPay(
                appid=self.APPID,
                app_notify_url=self.notify_url,
                app_private_key_string=self.app_private_key_string,
                alipay_public_key_string=self.alipay_public_key_string,
                sign_type="RSA2",
                debug=False,
                config=AliPayConfig(timeout=30),
        )

    def prepay(self, transaction):
        order = self.alipay.api_alipay_trade_precreate(
            subject=self.subject,
            out_trade_no=transaction.id,
            total_amount=transaction.pay_fee,
            notify_url=self.notify_url,
        )
        return order
