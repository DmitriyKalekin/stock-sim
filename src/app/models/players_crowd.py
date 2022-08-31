from app.models.player import Player


class PlayersCrowd:
    def __init__(self, t):
        self.t = t
        self.last_id = 0
        self.players = []

    def get_new_id(self):
        self.last_id += 1
        return str(self.last_id).zfill(4)

    def add_player(self, player_dict: dict):
        player_id = self.get_new_id()
        p = Player(player_id=player_id, **player_dict)
        self.players.append(p)
        return player_id

    def get_player_by_id(self, player_id) -> Player | bool:
        for p in self.players:
            if p.player_id == player_id:
                return p
        return False

    def get_players(self):
        return {
            "ts": self.t,
            "count": len(self.players),
            "players": self.players,
        }

    def delete_player(self, player_id):
        player = self.get_player_by_id(player_id)
        if not bool(player):
            return False
        self.players = [p for p in self.players if p.player_id != player_id]
        return True




