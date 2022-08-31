from app.models.consts import EnumOrderClass, EnumOrderType, EnumOrderStatus
from pprint import pprint


def test_execute_matching_orders__last_bid_closes_2__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, "cls": EnumOrderClass.LIMIT}
    # ----- ASKS -----
    ask = stock.add_order({**cmn, "type": EnumOrderType.ASK, "price": 700, "volume": 100})
    stock.add_order({**cmn, "type": EnumOrderType.ASK, "price": 600, "volume": 100})
    stock.add_order({**cmn, "type": EnumOrderType.ASK, "price": 500, "volume": 100})
    # ----- BIDS -----
    bid = stock.add_order({**cmn, "type": EnumOrderType.BID, "price": 650, "volume": 250})
    assert ask.volume == 100
    assert ask.status == EnumOrderStatus.ACTIVE
    assert bid.volume == 50
    assert bid.status == EnumOrderStatus.ACTIVE
    assert stock.order_book.asks == [ask]
    assert stock.order_book.bids == [bid]
    assert stock.price == 600
    assert stock.volume == 200


def test_execute_matching_orders__last_bid_lt__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, "cls": EnumOrderClass.LIMIT}
    # ----- ASKS -----
    ask = stock.add_order({**cmn, "type": EnumOrderType.ASK, "price": 500, "volume": 130})
    # ----- BIDS -----
    bid = stock.add_order({**cmn, "type": EnumOrderType.BID, "price": 650, "volume": 1})
    assert ask.volume == 129
    assert ask.status == EnumOrderStatus.ACTIVE
    assert bid.volume == 0
    assert bid.status == EnumOrderStatus.CLOSED
    assert stock.order_book.asks == [ask]
    assert stock.order_book.bids == []
    assert stock.price == 500
    assert stock.volume == 1


def test_execute_matching_orders__last_bid_eq__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, "cls": EnumOrderClass.LIMIT}
    # ----- ASKS -----
    ask = stock.add_order({**cmn, "type": EnumOrderType.ASK, "price": 500, "volume": 130})
    # ----- BIDS -----
    bid = stock.add_order({**cmn, "type": EnumOrderType.BID, "price": 650, "volume": 130})
    assert ask.volume == 0
    assert ask.status == EnumOrderStatus.CLOSED
    assert bid.volume == 0
    assert bid.status == EnumOrderStatus.CLOSED
    assert stock.order_book.asks == []
    assert stock.order_book.bids == []
    assert stock.price == 500
    assert stock.volume == 130


def test_execute_matching_orders__last_bid_gt__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, "cls": EnumOrderClass.LIMIT}
    # ----- ASKS -----
    ask = stock.add_order({**cmn, "type": EnumOrderType.ASK, "price": 500, "volume": 130})
    # ----- BIDS -----
    bid = stock.add_order({**cmn, "type": EnumOrderType.BID, "price": 650, "volume": 140})
    assert ask.volume == 0
    assert ask.status == EnumOrderStatus.CLOSED
    assert bid.volume == 10
    assert bid.status == EnumOrderStatus.ACTIVE
    assert stock.order_book.asks == []
    assert stock.order_book.bids == [bid]
    assert stock.price == 500
    assert stock.volume == 130


def test_execute_matching_orders__last_ask_gt__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, "cls": EnumOrderClass.LIMIT}
    # ----- BIDS -----
    bid = stock.add_order({**cmn, "type": EnumOrderType.BID, "price": 650, "volume": 1})
    # ----- ASKS -----
    ask = stock.add_order({**cmn, "type": EnumOrderType.ASK, "price": 500, "volume": 130})
    assert ask.volume == 129
    assert ask.status == EnumOrderStatus.ACTIVE
    assert bid.volume == 0
    assert bid.status == EnumOrderStatus.CLOSED
    assert stock.order_book.asks == [ask]
    assert stock.order_book.bids == []
    assert stock.price == 500
    assert stock.volume == 1


def test_execute_matching_orders__last_ask_eq__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, "cls": EnumOrderClass.LIMIT}
    # ----- BIDS -----
    bid = stock.add_order({**cmn, "type": EnumOrderType.BID, "price": 650, "volume": 130})
    # ----- ASKS -----
    ask = stock.add_order({**cmn, "type": EnumOrderType.ASK, "price": 500, "volume": 130})
    assert ask.volume == 0
    assert ask.status == EnumOrderStatus.CLOSED
    assert bid.volume == 0
    assert bid.status == EnumOrderStatus.CLOSED
    assert stock.order_book.asks == []
    assert stock.order_book.bids == []
    assert stock.price == 500
    assert stock.volume == 130


def test_execute_matching_orders__last_ask_lt__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, "cls": EnumOrderClass.LIMIT}
    # ----- BIDS -----
    bid = stock.add_order({**cmn, "type": EnumOrderType.BID, "price": 650, "volume": 140})
    # ----- ASKS -----
    ask = stock.add_order({**cmn, "type": EnumOrderType.ASK, "price": 500, "volume": 130})
    assert ask.volume == 0
    assert ask.status == EnumOrderStatus.CLOSED
    assert bid.volume == 10
    assert bid.status == EnumOrderStatus.ACTIVE
    assert stock.order_book.asks == []
    assert stock.order_book.bids == [bid]
    assert stock.price == 500
    assert stock.volume == 130
