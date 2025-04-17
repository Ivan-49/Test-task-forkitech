from tronpy import Tron
from tronpy.providers import HTTPProvider
from cachetools import TTLCache, cached
from loguru import logger
import os
from dotenv import load_dotenv
API_KEYS = os.getenv("TRON_API_KEYS").split(",")

provider = HTTPProvider(endpoint_uri="https://api.trongrid.io", api_key=API_KEYS)

client = Tron(provider=provider)

cache = TTLCache(maxsize=1000, ttl=300)


class ClientTron:
    def __init__(self):
        self.client = client

    @cached(cache)
    def get_account(self, address: str) -> dict:
        try:
            account = self.client.get_account(address)
            resource = self.client.get_account_resource(address)

            logger.info(f"Account: {account}")
            logger.info(f"Resource: {resource}")

            balance = account.get("balance", 0)
            bandwidth = resource.get("freeNetUsed", 0)
            energy = resource.get("energyUsed", 0)

            return {
                "balance": balance,
                "bandwidth": bandwidth,
                "energy": energy,
                "address": address,
            }
        except Exception as e:
            logger.error(f"Ошибка при получении аккаунта {address}: {e}")
            return None
