from fastapi import FastAPI, Body, status, HTTPException
from app.routers import router_orders, router_players

import time
from app.models.stock import Stock
import asyncio
from app.config import get_config


app = FastAPI()
app.include_router(router_orders.router)
app.include_router(router_players.router)
cfg = get_config()


async def ticks_generator():
    # global players, stock, cfg
    # if cfg["testing"]: # pragma: no cover
    #     return
    # t = 0
    # while True: # pragma: no cover
    #     stock.on_tick(t)
    #     players.on_tick(t)
    #     print("t=", t)
    #     await asyncio.sleep(1)
    #     t += 1
    return


@app.on_event('startup')
async def app_startup():
    global cfg
    asyncio.create_task(ticks_generator())
    return

# ==================================== PLAYER =====================================
# @app.post("/player", tags=["player"])
# async def create_player():
#     return {"message": "Hello World"}
#
# @app.get("/player/{id}", tags=["player"])
# async def get_player_by_id(id: int):
#     return {"message": "Hello World"}
#
# @app.get("/players", tags=["player"])
# async def get_players():
#     return {"message": "Hello World"}
#
# @app.put("/player/{id}", tags=["player"])
# async def update_player_by_id(id: int):
#     return {"message": "Hello World"}
#
# @app.delete("/player/{id}", tags=["player"])
# async def delete_player_by_id(id: int):
#     return {"message": "Hello World"}
