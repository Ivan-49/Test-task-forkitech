from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.address import (
    AddressResponseSchema,
    AddressRequestCreateSchema,
    AddressResponsePaginatedSchema,
)
from database.main import get_session
from utils.addres_repo import AddressRepo
from utils.tron_client import ClientTron
from loguru import logger
from datetime import datetime

router = APIRouter(tags=["trx"])
client_tron = ClientTron()
address_repo = AddressRepo()


@router.post("/address", response_model=AddressResponseSchema)
async def create_address(
    address_data: AddressRequestCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    if not client_tron.client.is_address(address_data.address):
        raise HTTPException(status_code=400, detail="Неверный формат адреса TRON")

    account = client_tron.get_account(address_data.address)
    if account is None:
        raise HTTPException(
            status_code=404, detail="Адрес не найден или ошибка получения данных"
        )

    try:
        await address_repo.add_address(address_data.address, session)
    except Exception as e:
        logger.error(f"Ошибка при сохранении адреса в базу: {e}")
    logger.info(f"Адрес {account} сохранен в базе")

    return AddressResponseSchema(
        balance_trx=account["balance"] / 1_000_000,
        bandwidth=account["bandwidth"],
        energy=account["energy"],
        address=account["address"],
        created_at=str(datetime.now()),
    )


@router.get("/addresses-paginated", response_model=list[AddressResponsePaginatedSchema])
async def get_addresses_paginated(
    limit: int = 10, offset: int = 0, session: AsyncSession = Depends(get_session)
):
    
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit должен быть между 1 и 100")

    if offset < 0:
        raise HTTPException(
            status_code=400, detail="Offset не может быть отрицательным"
        )

    try:
        addresses = await address_repo.get_addresses_paginated(limit, offset, session)

        return [
            AddressResponsePaginatedSchema(
                address=address.address,
                created_at=str(address.timestamp),
            )
            for address in addresses
        ]
    except Exception as e:
        logger.error(f"Ошибка пагинации: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Внутренняя ошибка сервера при получении данных"
        )
