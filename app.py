from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API endpoint and headers for cryptocurrency exchange rates
crypto_url = "https://alpha-vantage.p.rapidapi.com/query"
crypto_headers = {
    "X-RapidAPI-Key": "3c39793693mshe590cf6acdbfe36p161adbjsnbd45cb947e77",
    "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com",
}

# API endpoint and headers for regular currency exchange rates
currency_url = "https://currency-exchange.p.rapidapi.com/exchange"
currency_headers = {
    "X-RapidAPI-Key": "3c39793693mshe590cf6acdbfe36p161adbjsnbd45cb947e77",
    "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com",
}

# List of supported cryptocurrencies
supported_cryptos = [
    "BTC",
    "ETH",
    "XRP",
    "LTC",
    "ADA",
    "DOT",
    "LINK",
    "XLM",
    "BNB",
    "BCH",
]

# List of supported fiat currencies
supported_fiats = [
    "USD",
    "EUR",
    "JPY",
    "GBP",
    "AUD",
    "CAD",
    "CHF",
    "CNY",
    "HKD",
    "INR",
    "KRW",
    "NZD",
    "RUB",
    "SEK",
    "THB",
    "ZAR",
    "BRL",
    "DKK",
]

# List of supported currencies (expanded to include more currencies)
supported_currencies = [
    "SGD",
    "MYR",
    "EUR",
    "USD",
    "AUD",
    "JPY",
    "CNH",
    "HKD",
    "CAD",
    "INR",
    "DKK",
    "GBP",
    "RUB",
    "NZD",
    "MXN",
    "IDR",
    "TWD",
    "THB",
    "VND",
]


def get_crypto_exchange_rate(from_currency, to_currency):
    querystring = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": from_currency,
        "to_currency": to_currency,
    }
    response = requests.get(crypto_url, headers=crypto_headers, params=querystring)
    data = response.json()
    if "Realtime Currency Exchange Rate" in data:
        return data["Realtime Currency Exchange Rate"].get("5. Exchange Rate")
    return None


def get_regular_exchange_rate(from_currency, to_currency, amount):
    querystring = {"from": from_currency, "to": to_currency, "q": str(amount)}
    response = requests.get(currency_url, headers=currency_headers, params=querystring)
    data = response.json()
    if "rates" in data:
        return data["rates"].get(to_currency)
    return None


@app.route("/", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    navbar_choice = request.args.get("calculator", "crypto").lower()
    exchange_rate = None
    converted_amount = None

    if navbar_choice == "crypto":
        if request.method == "POST":
            from_currency = request.form.get("from_currency_crypto")
            to_currency = request.form.get("to_currency_crypto")
            amount_crypto = request.form.get("amount_crypto")

            if amount_crypto is not None and amount_crypto.strip():
                try:
                    amount = float(amount_crypto)
                    exchange_rate = get_crypto_exchange_rate(from_currency, to_currency)
                    if exchange_rate is not None:
                        converted_amount = amount * float(exchange_rate)
                except ValueError:
                    # Tangani ketika input tidak valid
                    error_message = "Invalid input. Please enter a valid numeric value for the amount."
                    return render_template(
                        "index.html",
                        navbar_choice=navbar_choice,
                        error_message=error_message,
                        supported_cryptos=supported_cryptos,
                        supported_fiats=supported_fiats,
                        supported_currencies=supported_currencies,
                    )

    elif navbar_choice == "regular":
        if request.method == "POST":
            from_currency = request.form.get("from_currency_regular")
            to_currency = request.form.get("to_currency_regular")
            amount_regular = request.form.get("amount_regular")

            if amount_regular is not None and amount_regular.strip():
                try:
                    amount = float(amount_regular)
                    exchange_rate = get_regular_exchange_rate(
                        from_currency, to_currency, amount
                    )
                    if exchange_rate is not None:
                        converted_amount = amount * float(exchange_rate)
                except ValueError:
                    # Tangani ketika input tidak valid
                    error_message = "Invalid input. Please enter a valid numeric value for the amount."
                    return render_template(
                        "index.html",
                        navbar_choice=navbar_choice,
                        error_message=error_message,
                        supported_cryptos=supported_cryptos,
                        supported_fiats=supported_fiats,
                        supported_currencies=supported_currencies,
                    )

    return render_template(
        "index.html",
        navbar_choice=navbar_choice,
        exchange_rate=exchange_rate,
        converted_amount=converted_amount,
        supported_cryptos=supported_cryptos,
        supported_fiats=supported_fiats,
        supported_currencies=supported_currencies,
    )


if __name__ == "__main__":
    app.run(debug=True)
