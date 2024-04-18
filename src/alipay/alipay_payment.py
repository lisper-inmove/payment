import json
from base64 import encodebytes

from Cryptodome.Hash import SHA256 as CryptodomeSHA256
from Cryptodome.PublicKey import RSA as CryptodomeRSA
from Cryptodome.Signature import PKCS1_v1_5 as CryptodomePKCS1_v1_5

from submodules.utils.idate import IDate
from submodules.utils.sys_env import SysEnv
from submodules.utils.logger import Logger
from submodules.utils.network_helper_v2 import NetworkHelper

from payment import Payment

logger = Logger()


class AlipayPayment(Payment):

    ALIPAY_GATEWAY = "https://openapi.alipay.com/gateway.do"

    APP_PRIVATE_KEY_STRING = open(SysEnv.get("APP_PRIVATE_KEY_FILE")).read()
    ALIPAY_PUBLIC_KEY_STRING = open(SysEnv.get("ALIPAY_PUBLIC_KEY_FILE")).read()
    APPID = SysEnv.get("ALIPAY_APPID")

    async def query(self, out_order_no):
        params = self.create_common_params()
        params.update({
            "method": "alipay.trade.query",
            "biz_content": {
                "out_trade_no": out_order_no
            }
        })
        params.update({
            "sign": self.build_signed_string(params)
        })
        url = f"{self.ALIPAY_GATEWAY}?charset=utf-8"
        result = await NetworkHelper().do_post_with_data(url, params)
        return result

    def create_common_params(self):
        params = {
            "app_id": self.APPID,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": IDate.now_withformat(),
            "version": "1.0",
            # "notify_url": self.generate_notify_url(),
        }
        return params

    def rsa_sign(self, plaintext):
        """RSA 数字签名"""
        signer = CryptodomePKCS1_v1_5.new(CryptodomeRSA.importKey(
            self.APP_PRIVATE_KEY_STRING))
        hash_value = CryptodomeSHA256.new(plaintext)
        signature = signer.sign(hash_value)
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        logger.info(f"签名结果: {sign}")
        return sign

    def build_signed_string(self, params):
        ordered_items = self.__ordered_data(params)
        raw_string = "&".join("{}={}".format(k, v) for k, v in ordered_items)
        logger.info(f"待签名字符串: {raw_string}")
        sign = self.rsa_sign(raw_string.encode("utf-8"))
        return sign

    def __ordered_data(self, data):
        for k, v in data.items():
            if isinstance(v, dict):
                data[k] = json.dumps(v, separators=(',', ':'))
        return sorted(data.items())
