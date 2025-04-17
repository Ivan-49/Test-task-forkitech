from pydantic import BaseModel, Field


class AddressRequestCreateSchema(BaseModel):
    address: str


class AddressResponsePaginatedSchema(BaseModel):
    address: str
    created_at: str


class AddressResponseSchema(BaseModel):
    balance_trx: float
    address: str
    bandwidth: int
    energy: int
    created_at: str
