import requests

def get_iframe_url(merchant_id, product_id, amount, currency, callback_url):
    """Gets the Pesapal iframe URL."""

    url = "https://api.pesapal.com/v3/iframe_url"

    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json",
    }

    body = {
        "merchant_id": merchant_id,
        "product_id": product_id,
        "amount": amount,
        "currency": currency,
        "callback_url": callback_url,
    }

    response = requests.post(url, headers=headers, data=body)

    if response.status_code == 200:
        return response.json()["iframe_url"]
    else:
        raise Exception("Error getting iframe URL: {}".format(response.status_code))

if __name__ == "__main__":
    merchant_id = "YOUR_MERCHANT_ID"
    product_id = "YOUR_PRODUCT_ID"
    amount = 1000
    currency = "KES"
    callback_url = "https://www.example.com/callback"

    iframe_url = get_iframe_url(merchant_id, product_id, amount, currency, callback_url)

    print(iframe_url)
