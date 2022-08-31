from test_players import add_player, test_add_player__success
from app.models.consts import EnumOrderClass, EnumOrderType, EnumOrderStatus

def add_order(client, json):
    res = client.post(
        "/order",
        json=json
    )
    return res


# TODO: ордер может выполниться при публикации - тогда он изменится
def test_add_order__success(client):
    with client:
        # ------ Add Player First -------------
        test_add_player__success(client)
        player_id = str(1).zfill(4)
        # ------------- CREATE  BID -----------------
        original1 = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.BID, "price": 36.60, "volume": 10.20}
        res = add_order(client, original1)
        assert res.status_code == 201
        assert res.json() == {"order_id": str(1).zfill(12)}
        # ------------- CREATE  ASK -----------------
        original2 = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.ASK, "price": 36.60, "volume": 10.20}
        res = add_order(client, original2)
        assert res.status_code == 201
        assert res.json() == {"order_id": str(2).zfill(12)}



def test_add_order__order_book_matching__success(client):
    with client:
        # ------ Add Player First -------------
        test_add_player__success(client)
        player_id = str(1).zfill(4)
        # ------------- CREATE  BID -----------------
        original1 = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.BID, "price": 36.60, "volume": 10.20}
        res = add_order(client, original1)
        assert res.status_code == 201
        assert res.json() == {"order_id": str(1).zfill(12)}
        # ------------- CREATE  ASK -----------------
        original2 = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.ASK, "price": 36.60, "volume": 10.20}
        res = add_order(client, original2)
        assert res.status_code == 201
        assert res.json() == {"order_id": str(2).zfill(12)}
        # ------------- ORDER BOOK EMPTY -----------------
        res = client.get(f"/order_book")
        assert res.status_code == 200
        assert res.json() == {"ts": 0, "bids_cnt": 0, "asks_cnt": 0, "bids": [], "asks": []}

def test_add_order__404_player_not_found__error(client):
    with client:
        # ------------- CREATE  BID -----------------
        original1 = {"player_id": "0001", "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.BID, "price": 36.60, "volume": 10.20}
        res = add_order(client, original1)
        assert res.status_code == 404
        assert res.json() == {"message": "Can't place order. Unknown Player with player_id=`0001` not found"}


def test_add_order__negative_price_with_3_digits__error(client):
    with client:
        # ------ Add Player First -------------
        test_add_player__success(client)
        player_id = str(1).zfill(4)
        # ------ Add BID -------------
        original = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.BID, "price": -0.123, "volume": 10.20}
        res = add_order(client, original)
        assert res.status_code == 422
        assert res.json() == {'detail': [
            {'ctx': {'limit_value': 0}, 'loc': ['body', 'price'], 'msg': 'ensure this value is greater than 0',
             'type': 'value_error.number.not_gt'}]} != {'detail': [
            {'ctx': {'decimal_places': 2}, 'loc': ['body', 'price'],
             'msg': 'ensure that there are no more than 2 decimal places', 'type': 'value_error.decimal.max_places'}]}


def test_add_order__negative_volume_with_6_digits__error(client):
    with client:
        # ------ Add Player First -------------
        test_add_player__success(client)
        player_id = str(1).zfill(4)
        # ------ Add BID -------------
        original = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.BID, "price": 36.60, "volume": -10.123456789}
        res = add_order(client, original)
        assert res.status_code == 422
        assert res.json() == {'detail': [
            {'ctx': {'limit_value': 0}, 'loc': ['body', 'volume'], 'msg': 'ensure this value is greater than 0',
             'type': 'value_error.number.not_gt'}]} != {'detail': [
            {'ctx': {'decimal_places': 6}, 'loc': ['body', 'volume'],
             'msg': 'ensure that there are no more than 6 decimal places', 'type': 'value_error.decimal.max_places'}]}


def test_add_order__wrong_type__error(client):
    with client:
        # ------ Add Player First -------------
        test_add_player__success(client)
        player_id = str(1).zfill(4)
        # ------ Add Order -------------
        original = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": "ABC", "price": 36.60, "volume": 10}
        res = add_order(client, original)
        assert res.status_code == 422
        assert res.json() == {
            'detail': [{'ctx': {'enum_values': ['BID', 'ASK']},
                        'loc': ['body', 'type'],
                        'msg': 'value is not a valid enumeration member; permitted: '
                               "'BID', 'ASK'",
                        'type': 'type_error.enum'}]
        }


def test_get_order_by_id__success(client):
    with client:
        # ------ Add Player First -------------
        test_add_player__success(client)
        player_id = str(1).zfill(4)
        # ---------------- CREATE BID FIRST -----------------
        original1 = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.BID, "price": 36.60, "volume": 10.20}
        res = add_order(client, original1)
        json1_id = {"order_id": str(1).zfill(12)}
        order1_id = json1_id["order_id"]
        assert res.status_code == 201
        assert res.json() == json1_id
        # ---------------- CREATE ASK FIRST -----------------
        original2 = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.ASK, "price": 37.60, "volume": 10.20}
        res = add_order(client, original2)
        json2_id = {"order_id": str(2).zfill(12)}
        order2_id = json2_id["order_id"]
        assert res.status_code == 201
        assert res.json() == json2_id
        # ---------------- AND READ FIRST -----------------
        res = client.get(f"/order/{order1_id}")
        assert res.status_code == 200
        assert res.json() == {**json1_id, "ts": 0, **original1, "status": EnumOrderStatus.CREATED}
        # ---------------- AND READ SECOND -----------------
        res = client.get(f"/order/{order2_id}")
        assert res.status_code == 200
        assert res.json() == {**json2_id, "ts": 0, **original2, "status": EnumOrderStatus.CREATED}


def test_get_order_by_id__404_not_found__error(client):
    with client:
        order_id = str(42).zfill(12)
        res = client.get(f"/order/{order_id}")
        assert res.status_code == 404
        assert res.json() == {"message": "order_id=`000000000042` not found"}


def test_get_order_book__empty__success(client):
    with client:
        res = client.get(f"/order_book")
        assert res.status_code == 200
        assert res.json() == {"ts": 0, "bids_cnt": 0, "asks_cnt": 0, "bids": [], "asks": []}


def test_get_order_book__sort_bids_acs_asks_desc_success(client):
    with client:
        # ------ Add Player First -------------
        test_add_player__success(client)
        player_id = str(1).zfill(4)
        # ------------- CREATE  BID -----------------
        original1 = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.BID, "price": 11.60, "volume": 11.20}
        wanted_id1 = {"order_id": str(1).zfill(12)}
        res = add_order(client, original1)
        assert res.status_code == 201
        assert res.json() == wanted_id1
        # ------------- CREATE  BID -----------------
        original2 = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.BID, "price": 12.60, "volume": 12.20}
        wanted_id2 = {"order_id": str(2).zfill(12)}
        res = add_order(client, original2)
        assert res.status_code == 201
        assert res.json() == wanted_id2
        # ------------- CREATE  ASK -----------------
        original3 = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.ASK, "price": 33.60, "volume": 33.20}
        wanted_id3 = {"order_id": str(3).zfill(12)}
        res = add_order(client, original3)
        assert res.status_code == 201
        assert res.json() == wanted_id3
        # ------------- CREATE  ASK -----------------
        original4 = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.ASK, "price": 44.60, "volume": 44.20}
        wanted_id4 = {"order_id": str(4).zfill(12)}
        res = add_order(client, original4)
        assert res.status_code == 201
        assert res.json() == wanted_id4
        # ------------- READ ORDER BOOK -----------------
        res = client.get(f"/order_book")
        assert res.status_code == 200
        assert res.json() == {
            "ts": 0,
            "bids_cnt": 2,
            "asks_cnt": 2,
            "bids": [{**wanted_id2, "ts": 0, **original2, "status": EnumOrderStatus.CREATED}, {**wanted_id1, "ts": 0, **original1, "status": EnumOrderStatus.CREATED}],
            # special sort order!!!
            "asks": [{**wanted_id3, "ts": 0, **original3, "status": EnumOrderStatus.CREATED}, {**wanted_id4, "ts": 0, **original4, "status": EnumOrderStatus.CREATED}]
            # # special sort order!!!
        }


def test_delete_order_by_id__success(client):
    with client:
        # ------ Add Player First -------------
        test_add_player__success(client)
        player_id = str(1).zfill(4)
        # ------------- CREATE  BID -----------------
        original1 = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.BID, "price": 11.60, "volume": 11.20}
        wanted1_json = {"order_id": str(1).zfill(12)}
        order1_id = wanted1_json["order_id"]
        res = add_order(client, original1)
        assert res.status_code == 201
        assert res.json() == wanted1_json
        # ------------- CREATE  ASK -----------------
        original2 = {"player_id": player_id, "cls": EnumOrderClass.LIMIT, "type": EnumOrderType.ASK, "price": 12.60, "volume": 11.20}
        wanted2_json = {"order_id": str(2).zfill(12)}
        order2_id = wanted2_json["order_id"]
        res = add_order(client, original2)
        assert res.status_code == 201
        assert res.json() == wanted2_json
        # ------------- DELETE -----------------
        res = client.delete(f"/order/{order1_id}")
        assert res.status_code == 204
        # ------------- DELETE -----------------
        res = client.delete(f"/order/{order2_id}")
        assert res.status_code == 204
        # ------------- AND READ ORDER BOOK -----------------
        res = client.get(f"/order_book")
        assert res.status_code == 200
        assert res.json() == {
            "ts": 0,
            "bids_cnt": 0,
            "asks_cnt": 0,
            "bids": [],
            "asks": []
        }


def test_delete_order_by_id__404_not_found__error(client):
    with client:
        # ------------- DELETE -----------------
        res = client.delete(f"/order/001")
        assert res.status_code == 404
        assert res.json() == {"message": "order_id=`001` not found"}
        # ------------- AND READ ORDER BOOK -----------------
        res = client.get(f"/order_book")
        assert res.status_code == 200
        assert res.json() == {
            "ts": 0,
            "bids_cnt": 0,
            "asks_cnt": 0,
            "bids": [],
            "asks": []
        }
