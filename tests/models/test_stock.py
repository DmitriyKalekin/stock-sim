from app.models.consts import OrderEClass, OrderEType, OrderEStatus
from app.models.stock import MarketOrderNotExecutableException
import pytest


def test_execute_matching_orders__market_order_closed__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, }
    # ----- ASKS -----
    ask = stock.create_order({**cmn, "type": OrderEType.ASK, "price": 700, "volume": 100})
    stock.create_order({**cmn, "type": OrderEType.ASK, "price": 600, "volume": 100})
    stock.create_order({**cmn, "type": OrderEType.ASK, "price": 500, "volume": 100})
    # ----- BIDS -----
    bid = stock.create_order(
        {"player_id": player_id, "type": OrderEType.BID, "price": OrderEClass.MARKET, "volume": 300})
    assert ask.volume == 0
    assert ask.status == OrderEStatus.CLOSED
    assert bid.volume == 0
    assert bid.status == OrderEStatus.CLOSED
    assert stock.order_book.asks == []
    assert stock.order_book.bids == []
    assert stock.price == 700
    assert stock.volume == 300


def test_execute_matching_orders__market_order__exception(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, }
    # ----- ASKS -----
    ask = stock.create_order({**cmn, "type": OrderEType.ASK, "price": 700, "volume": 100})
    stock.create_order({**cmn, "type": OrderEType.ASK, "price": 600, "volume": 100})
    stock.create_order({**cmn, "type": OrderEType.ASK, "price": 500, "volume": 100})
    # ----- BIDS -----
    with pytest.raises(MarketOrderNotExecutableException) as e:
        stock.create_order({**cmn, "type": OrderEType.BID, "price": OrderEClass.MARKET, "volume": 400})
    assert e.value.args[0] == 'Market volume `300` less than order.volume = `400`'
    assert ask.volume == 100
    assert ask.status == OrderEStatus.CREATED


def test_execute_matching_orders__market_order_closed_same_price__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, }
    # ----- ASKS -----
    ask = stock.create_order({**cmn, "type": OrderEType.ASK, "price": 700, "volume": 100})
    # ----- BIDS -----
    bid = stock.create_order({**cmn, "type": OrderEType.BID, "price": OrderEClass.MARKET, "volume": 100})
    assert ask.volume == 0
    assert ask.status == OrderEStatus.CLOSED
    assert bid.volume == 0
    assert bid.status == OrderEStatus.CLOSED
    assert stock.order_book.asks == []
    assert stock.order_book.bids == []
    assert stock.price == 700
    assert stock.volume == 100


def test_execute_matching_orders__last_bid_closes_2__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, }
    # ----- ASKS -----
    ask = stock.create_order({**cmn, "type": OrderEType.ASK, "price": 700, "volume": 100})
    stock.create_order({**cmn, "type": OrderEType.ASK, "price": 600, "volume": 100})
    stock.create_order({**cmn, "type": OrderEType.ASK, "price": 500, "volume": 100})
    # ----- BIDS -----
    bid = stock.create_order({**cmn, "type": OrderEType.BID, "price": 650, "volume": 250})
    assert ask.volume == 100
    assert ask.status == OrderEStatus.CREATED
    assert bid.volume == 50
    assert bid.status == OrderEStatus.EXECUTED
    assert stock.order_book.asks == [ask]
    assert stock.order_book.bids == [bid]
    assert stock.price == 600
    assert stock.volume == 200


def test_execute_matching_orders__last_bid_lt__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, }
    # ----- ASKS -----
    ask = stock.create_order({**cmn, "type": OrderEType.ASK, "price": 500, "volume": 130})
    # ----- BIDS -----
    bid = stock.create_order({**cmn, "type": OrderEType.BID, "price": 650, "volume": 1})
    assert ask.volume == 129
    assert ask.status == OrderEStatus.EXECUTED
    assert bid.volume == 0
    assert bid.status == OrderEStatus.CLOSED
    print("=======ASKS========")
    print(stock.order_book.asks)
    print("=======BIDS========")
    print(stock.order_book.bids)


    assert stock.order_book.asks == [ask]
    assert stock.order_book.bids == []
    assert stock.price == 500
    assert stock.volume == 1


def test_execute_matching_orders__last_bid_eq__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, }
    # ----- ASKS -----
    ask = stock.create_order({**cmn, "type": OrderEType.ASK, "price": 500, "volume": 130})
    # ----- BIDS -----
    bid = stock.create_order({**cmn, "type": OrderEType.BID, "price": 650, "volume": 130})
    assert ask.volume == 0
    assert ask.status == OrderEStatus.CLOSED
    assert bid.volume == 0
    assert bid.status == OrderEStatus.CLOSED
    assert stock.order_book.asks == []
    assert stock.order_book.bids == []
    assert stock.price == 500
    assert stock.volume == 130


def test_execute_matching_orders__last_bid_gt__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, }
    # ----- ASKS -----
    ask = stock.create_order({**cmn, "type": OrderEType.ASK, "price": 500, "volume": 130})
    # ----- BIDS -----
    bid = stock.create_order({**cmn, "type": OrderEType.BID, "price": 650, "volume": 140})
    assert ask.volume == 0
    assert ask.status == OrderEStatus.CLOSED
    assert bid.volume == 10
    assert bid.status == OrderEStatus.EXECUTED
    assert stock.order_book.asks == []
    assert stock.order_book.bids == [bid]
    assert stock.price == 500
    assert stock.volume == 130


def test_execute_matching_orders__last_ask_gt__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, }
    # ----- BIDS -----
    bid = stock.create_order({**cmn, "type": OrderEType.BID, "price": 650, "volume": 1})
    # ----- ASKS -----
    ask = stock.create_order({**cmn, "type": OrderEType.ASK, "price": 500, "volume": 130})
    assert ask.volume == 129
    assert ask.status == OrderEStatus.EXECUTED
    assert bid.volume == 0
    assert bid.status == OrderEStatus.CLOSED
    assert stock.order_book.asks == [ask]
    assert stock.order_book.bids == []
    assert stock.price == 500
    assert stock.volume == 1


def test_execute_matching_orders__last_ask_eq__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, }
    # ----- BIDS -----
    bid = stock.create_order({**cmn, "type": OrderEType.BID, "price": 650, "volume": 130})
    # ----- ASKS -----
    ask = stock.create_order({**cmn, "type": OrderEType.ASK, "price": 500, "volume": 130})
    assert ask.volume == 0
    assert ask.status == OrderEStatus.CLOSED
    assert bid.volume == 0
    assert bid.status == OrderEStatus.CLOSED
    assert stock.order_book.asks == []
    assert stock.order_book.bids == []
    assert stock.price == 500
    assert stock.volume == 130


def test_execute_matching_orders__last_ask_lt__success(stock):
    player_id = stock.add_player({"name": "Player0001"})
    cmn = {"player_id": player_id, }
    # ----- BIDS -----
    bid = stock.create_order({**cmn, "type": OrderEType.BID, "price": 650, "volume": 140})
    # ----- ASKS -----
    ask = stock.create_order({**cmn, "type": OrderEType.ASK, "price": 500, "volume": 130})
    assert ask.volume == 0
    assert ask.status == OrderEStatus.CLOSED
    assert bid.volume == 10
    assert bid.status == OrderEStatus.EXECUTED
    assert stock.order_book.asks == []
    assert stock.order_book.bids == [bid]
    assert stock.price == 500
    assert stock.volume == 130
