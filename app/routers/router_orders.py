from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.routers.dto import res as response
from app.routers.dto.order import res_order, req_order
from fastapi import status
from app.models.stock import Stock, PlayerNotExistException

stock = Stock.get_singleton_instance()

router = APIRouter(
    tags=["order"],
    responses={404: {"model": response.MessageError}},
)


@router.post("/order", response_model=res_order.OrderId, status_code=status.HTTP_201_CREATED)
async def add_order(order: req_order.OrderBase):
    global stock
    try:
        order = stock.add_order(order.dict())
    except PlayerNotExistException as e:
        return JSONResponse(status_code=404, content={"message": str(e)})
    return res_order.OrderId(**{"order_id": order.order_id})


@router.get("/order/{order_id}", response_model=res_order.Order)
async def get_order_by_id(order_id: str):
    global stock
    order = stock.get_order(order_id)
    if not order:
        return JSONResponse(status_code=404, content={"message": f"order_id=`{order_id}` not found"})
    return res_order.Order.from_orm(order)


@router.get("/order_book", response_model=res_order.OrderCollection)
async def get_order_book():
    global stock
    order_book = stock.get_order_book()
    return res_order.OrderCollection(**order_book)


@router.delete("/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_by_id(order_id: str):
    global stock
    exists = bool(stock.delete_order(order_id))
    if not exists:
        return JSONResponse(status_code=404, content={"message": f"order_id=`{order_id}` not found"})
    return
