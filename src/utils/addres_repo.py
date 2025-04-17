from models import AddressRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger


class AddressRepo:
    async def add_address(self, address: str, session: AsyncSession) -> AddressRequest:
        try:
            address_request = AddressRequest(address=address)
            session.add(address_request)
            await session.commit()
            return address_request
        except Exception as e:
            logger.error(f"database address add error: {e}")
            await session.rollback()
            raise e

    async def get_addresses_paginated(
        self, limit: int, offset: int, session: AsyncSession
    ):
        stmt = select(AddressRequest).limit(limit).offset(offset)
        result = await session.execute(stmt)
        return result.scalars().all()
