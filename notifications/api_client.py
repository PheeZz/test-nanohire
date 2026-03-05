from typing import Any
import aiohttp
from config import settings
from loguru import logger


class APIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.service_key = settings.API_SERVICE_KEY

    async def get_manager_notifications(self) -> list[dict[str, Any]]:
        url = f"{self.base_url}/api/v1/notification/responses/list"
        headers = {"X-Service-Key": self.service_key}

        try:
            async with (
                aiohttp.ClientSession() as session,
                session.get(url, headers=headers) as response,
            ):
                if response.status == 200:
                    data = await response.json()
                    return data.get("notifications", [])
                else:
                    error_text = await response.text()
                    logger.error(
                        f"❌ Error fetching notifications: {response.status} - {error_text}"
                    )
                    return []
        except Exception as e:
            logger.exception(f"❌ Exception while fetching notifications: {e}")
            return []


api_client = APIClient()
