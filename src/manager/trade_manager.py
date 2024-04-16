import proto.entities.payment_pb2 as payment_pb
from manager.base_manager import BaseManager
from dao.trade_dao import TradeDA
from errors import PopupError


class TradeManager(BaseManager):

    @property
    def dao(self):
        if self._dao is None:
            self._dao = TradeDA()
        return self._dao

    async def delete_trade(self, request):
        trade = payment_pb.Trade()
        trade.id = request.id
        await self.dao.delete_trade(trade)
        return trade

    async def query_trade(self, request):
        return await self.dao.get_trade_by_id(request.id)

    async def query_trade_by_order_id(self, request):
        async for trade in self.dao.get_trade_by_order_id(request.id):
            yield self.PH.to_obj(trade, payment_pb.Trade)

    async def list_trade(self, request):
        async for trade in self.dao.list_trade():
            yield self.PH.to_obj(trade, payment_pb.Trade)

    async def add_trade(self, request):
        # trade.id: 支付服务的唯一ID
        trade = self.create_obj(payment_pb.Trade)
        trade.pay_fee = request.pay_fee
        trade.order_id = request.id
        await self.dao.add_trade(trade)
        return trade

    async def update_trade(self, trade):
        self.update_obj(trade)
        return await self.dao.update_trade(trade)
