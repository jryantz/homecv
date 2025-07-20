import requests
from homecv.config import Config


class HomeAssistantClient:
    def __init__(self, base_url=None, token=None):
        self.base_url = base_url or Config.HOMEASSISTANT_URL
        self.token = token or Config.HOMEASSISTANT_TOKEN

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def get_snapshot(self, entity):
        url = f"{self.base_url}/api/camera_proxy/{entity}"

        response = requests.get(
            url=url,
            headers=self.headers,
            timeout=5,
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to get snapshot: {response.status_code} {response.text}"
            )

        return response.content
