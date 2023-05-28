"""
支付宝当面付
"""

import json
from datetime import datetime
from base64 import encodebytes
from urllib.parse import quote_plus

from Cryptodome.Hash import SHA256 as CryptodomeSHA256
from Cryptodome.PublicKey import RSA as CryptodomeRSA
from Cryptodome.Signature import PKCS1_v1_5 as CryptodomePKCS1_v1_5
from Crypto.Cipher import AES
import requests

from submodules.utils.sys_env import SysEnv
from submodules.utils.idate import IDate
from submodules.utils.logger import Logger

logger = Logger()


class AlipayF2F:

    ALIPAY_GATE_WAY = "https://openapi.alipay.com/gateway.do"

    def __init__(self, subject=None):
        if subject is None:
            subject = "当面付"
        self.subject = subject
        self.APPID = SysEnv.get("ALIPAY_APPID")
        self.web_url = SysEnv.get("ALIPAY_WEB_URL")
        self.app_private_key_string = open(SysEnv.get("APP_PRIVATE_KEY_FILE")).read()
        self.alipay_public_key_string = open(SysEnv.get("ALIPAY_PUBLIC_KEY_FILE")).read()
        self.notify_url = f"{self.web_url}/alipay/notify"

    def create_common_params(self):
        params = {
            "app_id": self.APPID,
            "method": "alipay.trade.precreate",
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "notify_url": self.notify_url,
        }
        return params

    def prepay(self, transaction):
        params = self.create_common_params()
        params.update({
            "biz_content": {
                "out_trade_no": transaction.id,
                # TODO
                "total_amount": transaction.pay_fee / float(100),
                "subject": self.subject,
            }
        })
        params.update({
            "sign": self.__build_signed_string(params)
        })
        logger.info(f"prepay 请求参数: {params}")
        result = requests.post(f"{self.ALIPAY_GATE_WAY}?charset=utf-8", data=params)
        logger.info(f"prepay 请求返回: {result.text}")
        return result

    def rsa_sign(self, plaintext):
        """RSA 数字签名"""
        signer = CryptodomePKCS1_v1_5.new(CryptodomeRSA.importKey(
            self.app_private_key_string))
        hash_value = CryptodomeSHA256.new(plaintext)
        signature = signer.sign(hash_value)
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        logger.info(f"签名结果: {sign}")
        return sign

    def __build_signed_string(self, params):
        ordered_items = self.__ordered_data(params)
        raw_string = "&".join("{}={}".format(k, v) for k, v in ordered_items)
        logger.info(f"待签名字符串: {raw_string}")
        sign = self.rsa_sign(raw_string.encode("utf-8"))
        # unquoted_items = ordered_items + [('sign', sign)]
        # signed_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in unquoted_items)
        return sign

    def __ordered_data(self, data):
        for k, v in data.items():
            if isinstance(v, dict):
                data[k] = json.dumps(v, separators=(',', ':'))
        return sorted(data.items())
