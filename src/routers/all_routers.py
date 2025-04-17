from fastapi import APIRouter

from routers.trx_router import router as trx_router

all_routers = [trx_router]
