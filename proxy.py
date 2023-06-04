from .alipay.alipay_f2f import AlipayF2F
from .alipay.alipay_payment import AlipayPayment


class QueryResult:

    def __getattr__(self, name):
        if self.__dict__.get(name):
            return self.__dict__.get(name)
        return None


class PrepayResult:

    def __getattr__(self, name):
        if self.__dict__.get(name):
            return self.__dict__.get(name)
        return None


class PaymentProxy:

    def alipay_f2f_prepay(self, transaction_id, pay_fee):
        obj = AlipayF2F()
        result = obj.prepay(
            transaction_id,
            pay_fee
        )
        resp = PrepayResult()
        resp.qrcode_url = result.get("alipay_trade_precreate_response").get("qr_code")
        return resp

    def query_alipay_trade(self, transaction_id):
        obj = AlipayPayment()
        result = obj.query(transaction_id)
        resp = QueryResult()
        resp.success = result.get("alipay_trade_query_response").get("code") == "10000"
        resp.third_party_id = result.get("alipay_trade_query_response").get("trade_no")
        resp.msg = result.get("alipay_trade_query_response").get("msg")
        resp.sub_msg = result.get("alipay_trade_query_response").get("sub_msg", "")
        return resp
