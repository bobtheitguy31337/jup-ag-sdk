from typing import Any, Dict
from pydantic import BaseModel
from pydantic.alias_generators import to_camel

class SwapRequest(BaseModel):
    """
    Model for swap requests to the Jupiter API.
    """
    input_mint: str
    output_mint: str
    amount: int
    slippage_bps: int = 50
    only_direct_routes: bool = False
    as_legacy_transaction: bool = False

    def to_dict(self) -> Dict[str, Any]:
        params = self.model_dump(exclude_none=True)

        camel_case_params = {
            to_camel(key): value for key, value in params.items()
        }

        return camel_case_params 