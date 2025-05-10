from dotenv import load_dotenv
from jup_ag_sdk.clients.swap_api_client import SwapApiClient
from jup_ag_sdk.models.swap_api.swap_request_model import SwapRequest


def test_swap_quote() -> None:
    """
    Test the SwapApiClient quote method.
    """
    load_dotenv()
    client = SwapApiClient()

    # WSOL and USDC mints
    wsol_mint = "So11111111111111111111111111111111111111112"
    usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

    request = SwapRequest(
        input_mint=wsol_mint,
        output_mint=usdc_mint,
        amount=10000000,  # 0.01 WSOL
    )

    try:
        quote_response = client.quote(request)
        assert (
            "inputMint" in quote_response
        ), "Response does not contain 'inputMint' key."
        assert (
            "outputMint" in quote_response
        ), "Response does not contain 'outputMint' key."
        assert (
            "outAmount" in quote_response
        ), "Response does not contain 'outAmount' key."

        print()
        print("Quote API Response:")
        print(f"  - Input Amount: {quote_response['inAmount']}")
        print(f"  - Output Amount: {quote_response['outAmount']}")
        print(f"  - Price Impact: {quote_response.get('priceImpactPct', 'N/A')}%")

    except Exception as e:
        print("Error occurred while fetching quote:", str(e))
    finally:
        client.close()


def test_swap_execute() -> None:
    """
    Test the SwapApiClient swap method.
    """
    load_dotenv()
    client = SwapApiClient()

    # WSOL and USDC mints
    wsol_mint = "So11111111111111111111111111111111111111112"
    usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

    request = SwapRequest(
        input_mint=wsol_mint,
        output_mint=usdc_mint,
        amount=10000000,  # 0.01 WSOL
    )

    try:
        swap_response = client.swap(request)
        assert (
            "txid" in swap_response
        ), "Response does not contain 'txid' key."

        print()
        print("Swap API Response:")
        print(f"  - Transaction Signature: {swap_response['txid']}")
        print(f"  - View on Solscan: https://solscan.io/tx/{swap_response['txid']}")

    except Exception as e:
        print("Error occurred while executing swap:", str(e))
    finally:
        client.close() 