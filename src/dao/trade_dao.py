import proto.entities.payment_pb2 as payment_pb
from pymongo.errors import DuplicateKeyError

from base import Base
from dao.mongodb import MongoDBHelper
from errors import PopupError
from submodules.utils.logger import Logger

logger = Logger()


class TradeDA(MongoDBHelper, Base):

    coll = "___payment_db___trades___"

    async def add_trade(self, trade):
        json_data = self.PH.to_dict(trade)
        try:
            await self.insert_one(json_data)
        except DuplicateKeyError as ex:
            logger.error(ex)
            raise PopupError("Already add this trade")

    async def update_trade(self, trade):
        matcher = {"id": trade.id}
        json_data = self.PH.to_dict(trade)
        await self.update_one(matcher, json_data)

    async def delete_trade(self, trade):
        matcher = {"id": trade.id}
        return await self.delete_one(matcher)

    async def query_trade(self, trade):
        matcher = {"id": trade.id}
        return await self.find_one(matcher)

    async def list_trade(self):
        matcher = {}
        async for trade in self.find_many(matcher):
            yield trade

    async def get_trade_by_id(self, id):
        matcher = {"id": id}
        trade = await self.find_one(matcher)
        return self.PH.to_obj(trade, payment_pb.Trade)

    async def get_trade_by_order_id(self, order_id):
        matcher = {"order_id": order_id}
        async for trade in self.find_many(matcher):
            yield trade
