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


