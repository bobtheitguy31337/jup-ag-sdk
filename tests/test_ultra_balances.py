from dotenv import load_dotenv

from jup_ag_sdk.clients.ultra_api_client import UltraApiClient


def test_ultra_get_balances() -> None:
    """
    Test the UltraApiClient balances method.
    """
    load_dotenv()
    client = UltraApiClient()

    address = client._get_public_key()

    try:
        balances_response = client.balances(str(address))
        assert (
            "SOL" in balances_response
        ), "Response does not contain 'SOL' key."

        print()
        print("Balances API Response:")
        for token, details in balances_response.items():
            print(f"Token: {token}")
            print(f"  - Amount: {details['amount']}")
            print(f"    UI Amount: {details['uiAmount']}")
            print(f"    Slot: {details['slot']}")
            print(f"    Is Frozen: {details['isFrozen']}")

    except Exception as e:
        print("Error occurred while fetching balances:", str(e))
    finally:
        client.close()
