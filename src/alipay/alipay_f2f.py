"""
支付宝当面付
"""

from submodules.utils.logger import Logger
from submodules.utils.network_helper import NetworkHelper

from .alipay_payment import AlipayPayment

logger = Logger()


class AlipayF2F(AlipayPayment):

    def __init__(self, subject=None):
        if subject is None:
            subject = "当面付"
        self.subject = subject

    def prepay(self, out_order_no, pay_fee):
        params = self.create_common_params()
        params.update({
            "method": "alipay.trade.precreate",
            "biz_content": {
                "out_trade_no": out_order_no,
                # TODO
                "total_amount": pay_fee / float(100),
                "subject": self.subject,
            }
        })
        params.update({
            "sign": self.build_signed_string(params)
        })
        url = f"{self.ALIPAY_GATEWAY}?charset=utf-8"
        result = NetworkHelper().do_post_with_data(url, params)
        return result
