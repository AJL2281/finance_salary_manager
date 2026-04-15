import requests

# Global var to fetch the dollar value once and reuse it
_cached_dollar_type_card = None

# Make the request to the API of DolarApi.com to get the sell value
def get_dollar_type_card():
    global _cached_dollar_type_card

    # If we already fetch the value just return it 
    if _cached_dollar_type_card is not None:
        return _cached_dollar_type_card

    try:
        r = requests.get("https://dolarapi.com/v1/dolares/tarjeta", timeout=5)
        r.raise_for_status()
        _cached_dollar_type_card = r.json()['venta']
        return _cached_dollar_type_card

    except requests.exceptions.RequestException as e:
            print(f"Error while connecting to DolarAPI: {e}")
            return None

    except ValueError:
        print("Error invalid JSON response from the API.")
        return None

# Test Block
# if __name__ == "__main__":
#     print("Testing API Connection")

#     sell_value = get_dolar_type_card()

#     if sell_value:
#         print(f"Success, current dollar value: {sell_value}")

#         print("Testing Cache")
#         cached_sell_value = get_dolar_type_card()
#         print(f"Cached value: {cached_sell_value}")

#     else:
#         print("Failed to retrieve the value")