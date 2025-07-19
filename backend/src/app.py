from http import HTTPStatus

from fastapi import FastAPI

from src.router import (
    addressRouter,
    authRouter,
    cartWantRouter,
    categoryRouter,
    checkoutRouter,
    colorRouter,
    productRouter,
    sellerRouter,
    userRouter,
)
from src.schema.messageSchema import Message

app = FastAPI(
    title='Brechó',
    description=(
        'Brechó is an online thrift store API with user authentication, store '
        'and product management, '
        'shopping cart, order tracking, and multiple payment options.'
    ),
    version='1.0.0',
)

app.include_router(userRouter.router)
app.include_router(authRouter.router)
app.include_router(addressRouter.router)
app.include_router(sellerRouter.router)
app.include_router(categoryRouter.router)
app.include_router(colorRouter.router)
app.include_router(productRouter.router)
app.include_router(cartWantRouter.router)
app.include_router(checkoutRouter.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Welcome to Brechó API!'}
