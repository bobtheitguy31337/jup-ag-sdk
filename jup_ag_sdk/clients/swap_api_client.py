from typing import Any, Dict, Optional

from jup_ag_sdk.clients.jupiter_client import JupiterClient
from jup_ag_sdk.models.swap_api.swap_request_model import SwapRequest


class SwapApiClient(JupiterClient):

    def __init__(
        self,
        api_key: Optional[str] = None,
        private_key_env_var: str = "PRIVATE_KEY",
        timeout: int = 10,
    ):
        super().__init__(
            api_key=api_key,
            private_key_env_var=private_key_env_var,
            timeout=timeout,
        )

    def quote(self, request: SwapRequest) -> Dict[str, Any]:
        params = request.to_dict()

        url = f"{self.base_url}/v6/quote"
        response = self.client.get(
            url, params=params, headers=self._get_headers()
        )
        response.raise_for_status()

        return response.json()

    def swap(self, request: SwapRequest) -> Dict[str, Any]:
        quote_response = self.quote(request)
        swap_payload = {
            "quoteResponse": quote_response,
            "userPublicKey": self._get_public_key(),
            "wrapUnwrapSOL": True
        }

        url = f"{self.base_url}/v6/swap"
        response = self.client.post(
            url, json=swap_payload, headers=self._post_headers()
        )
        response.raise_for_status()

        swap_response = response.json()
        signed_transaction = self._sign_base64_transaction(
            swap_response["swapTransaction"]
        )

        url = f"{self.base_url}/v6/send"
        send_payload = {
            "transaction": self._serialize_versioned_transaction(signed_transaction)
        }
        
        response = self.client.post(
            url, json=send_payload, headers=self._post_headers()
        )
        response.raise_for_status()

        return response.json() 