def add_player(client, json):
    res = client.post(
        "/player",
        json=json
    )
    return res


def test_add_player__success(client):
    with client:
        original1 = {"name": "Player001"}
        res = add_player(client, original1)
        player_id = str(1).zfill(4)
        assert res.status_code == 201
        assert res.json() == {"player_id": player_id}


def test_get_player_by_id__success(client):
    with client:
        original1 = {"name": "Player001"}
        res = add_player(client, original1)
        player_id = str(1).zfill(4)
        assert res.status_code == 201
        assert res.json() == {"player_id": player_id}
        # ---------- read ------------
        res = client.get(f"/player/{player_id}")
        assert res.status_code == 200
        assert res.json() == {"player_id": player_id, **original1}


def test_get_player_by_id__404_not_found__error(client):
    with client:
        player_id = "Player001"
        res = client.get(f"/player/{player_id}")
        assert res.status_code == 404
        assert res.json() == {"message": "player_id=`Player001` not found"}

def test_get_players__empty__success(client):
    with client:
        res = client.get(f"/players")
        assert res.status_code == 200
        assert res.json() == {"ts": 0, "count": 0, "players": []}

def test_delete_player_by_id__success(client):
    with client:
        # ------------- CREATE  BID -----------------
        original1 = {"name": "Player001"}
        res = add_player(client, original1)
        player1_id = str(1).zfill(4)
        assert res.status_code == 201
        assert res.json() == {"player_id": player1_id}
        # ------------- CREATE  ASK -----------------
        original2 = {"name": "Player002"}
        res = add_player(client, original2)
        player2_id = str(2).zfill(4)
        assert res.status_code == 201
        assert res.json() == {"player_id": player2_id}
        # ------------- DELETE -----------------
        res = client.delete(f"/player/{player1_id}")
        assert res.status_code == 204
        # ------------- DELETE -----------------
        res = client.delete(f"/player/{player2_id}")
        assert res.status_code == 204
        # ------------- AND READ ORDER BOOK -----------------
        res = client.get(f"/players")
        assert res.status_code == 200
        assert res.json() == {
            "ts": 0,
            "count": 0,
            "players": []
        }


def test_delete_order_by_id__404_not_found__error(client):
    with client:
        # ------------- DELETE -----------------
        res = client.delete(f"/player/001")
        assert res.status_code == 404
        assert res.json() == {"message": "player_id=`001` not found"}
        # ------------- AND READ ORDER BOOK -----------------
        res = client.get(f"/players")
        assert res.status_code == 200
        assert res.json() == {
            "ts": 0,
            "count": 0,
            "players": []
        }
