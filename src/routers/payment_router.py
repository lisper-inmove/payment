import json

import proto.api.api_payment_pb2 as api_payment
import proto.entities.payment_pb2 as payment_pb

from fastapi import Request
from routers.base_router import BaseRouter
from submodules.utils.logger import Logger
from unify_response import UnifyResponse
from manager.trade_manager import TradeManager
from errors import SilentError

from alipay.alipay_f2f import AlipayF2F
from alipay.alipay_payment import AlipayPayment

from submodules.utils.protobuf_helper import ProtobufHelper


logger = Logger()


class PaymentRouter(BaseRouter):

    trade_manager = TradeManager()

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    async def prepay_POST(self, request: Request):
        data = await request.body()
        request = ProtobufHelper.to_obj_v2(data, api_payment.PrepayRequest)
        trade = await self.trade_manager.add_trade(request)
        if (trade.pay_method == payment_pb.PayMethod.ALIPAY_F2F):
            return await self.alipay_f2f_prepay(trade)
        raise SilentError("PayMethod not supported")

    async def alipay_f2f_prepay(self, trade):
        obj = AlipayF2F()
        result = obj.prepay(trade.id, trade.pay_fee)
        resp = api_payment.PrepayResponse()
        resp.qrcode_url = result.get("alipay_trade_precreate_response").get("qr_code")
        resp.trade_id = trade.id
        return UnifyResponse.R(ProtobufHelper.to_json(resp))

    async def trade_query_POST(self, request: Request):
        data = await request.body()
        request = ProtobufHelper.to_obj_v2(data, api_payment.TradeQueryRequest)
        trade = await self.trade_manager.query_trade(request)
        if not trade:
            raise SilentError("Trade not found")
        resp = None
        if trade.pay_method == payment_pb.ALIPAY_F2F:
            resp = await self.alipay_trade_query(trade)
        if resp is None:
            raise SilentError("Trade not found")
        return UnifyResponse.R(ProtobufHelper.to_json(resp))

    async def alipay_trade_query(self, trade):
        obj = AlipayPayment()
        result = obj.query(trade.id)
        resp = api_payment.TradeQueryResponse()
        resp.status = result.get("alipay_trade_query_response").get(
            "trade_status", "")
        resp.msg = result.get("alipay_trade_query_response").get("msg", "")
        resp.is_pay_success = result.get("alipay_trade_query_response").get(
            "trade_status") == "TRADE_SUCCESS"
        trade.trade_info = json.dumps(result)
        await self.trade_manager.update_trade(trade)
        return resp
