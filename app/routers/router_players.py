from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.routers.dto import res as response
from app.routers.dto.player import res_player, req_player
from fastapi import status
from app.models.stock import Stock

stock = Stock.get_singleton_instance()

router = APIRouter(
    tags=["player"],
    responses={404: {"model": response.MessageError}},
)


@router.post("/player", response_model=res_player.PlayerId, status_code=status.HTTP_201_CREATED)
async def add_player(player: req_player.PlayerBase):
    global stock
    player_id = stock.add_player(player.dict())
    return res_player.PlayerId(**{"player_id": player_id})


@router.get("/player/{player_id}", response_model=res_player.Player)
async def get_player_by_id(player_id: str):
    global stock
    player = stock.get_player_by_id(player_id)
    if not player:
        return JSONResponse(status_code=404, content={"message": f"player_id=`{player_id}` not found"})
    return res_player.Player.from_orm(player)


@router.get("/players", response_model=res_player.PlayersCollection)
async def get_players():
    global stock
    players = stock.get_players()
    return res_player.PlayersCollection(**players)


@router.delete("/player/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player_by_id(player_id: str):
    global stock
    exists = bool(stock.delete_player(player_id))
    if not exists:
        return JSONResponse(status_code=404, content={"message": f"player_id=`{player_id}` not found"})
    return
