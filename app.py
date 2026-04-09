import os
import requests
from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Free API from exchangerate-api.com (no key needed for open endpoint)
# Uses the open.er-api.com free tier — no signup required
BASE_URL = "https://open.er-api.com/v6/latest"

CURRENCY_NAMES = {
    "USD": "US Dollar", "EUR": "Euro", "GBP": "British Pound",
    "JPY": "Japanese Yen", "CAD": "Canadian Dollar", "AUD": "Australian Dollar",
    "CHF": "Swiss Franc", "CNY": "Chinese Yuan", "INR": "Indian Rupee",
    "MXN": "Mexican Peso", "BRL": "Brazilian Real", "SGD": "Singapore Dollar",
    "HKD": "Hong Kong Dollar", "NOK": "Norwegian Krone", "SEK": "Swedish Krona",
    "DKK": "Danish Krone", "NZD": "New Zealand Dollar", "ZAR": "South African Rand",
    "RUB": "Russian Ruble", "TRY": "Turkish Lira", "AED": "UAE Dirham",
    "SAR": "Saudi Riyal", "KRW": "South Korean Won", "THB": "Thai Baht",
    "MYR": "Malaysian Ringgit", "IDR": "Indonesian Rupiah", "PHP": "Philippine Peso",
    "PLN": "Polish Zloty", "CZK": "Czech Koruna", "HUF": "Hungarian Forint",
    "ILS": "Israeli Shekel", "CLP": "Chilean Peso", "COP": "Colombian Peso",
    "PKR": "Pakistani Rupee", "BDT": "Bangladeshi Taka", "EGP": "Egyptian Pound",
    "VND": "Vietnamese Dong", "UAH": "Ukrainian Hryvnia", "NGN": "Nigerian Naira",
    "KWD": "Kuwaiti Dinar", "QAR": "Qatari Riyal", "OMR": "Omani Rial",
    "BHD": "Bahraini Dinar", "JOD": "Jordanian Dinar", "TWD": "Taiwan Dollar",
    "RON": "Romanian Leu", "HRK": "Croatian Kuna", "BGN": "Bulgarian Lev",
}

CURRENCY_FLAGS = {
    "USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "JPY": "🇯🇵", "CAD": "🇨🇦",
    "AUD": "🇦🇺", "CHF": "🇨🇭", "CNY": "🇨🇳", "INR": "🇮🇳", "MXN": "🇲🇽",
    "BRL": "🇧🇷", "SGD": "🇸🇬", "HKD": "🇭🇰", "NOK": "🇳🇴", "SEK": "🇸🇪",
    "DKK": "🇩🇰", "NZD": "🇳🇿", "ZAR": "🇿🇦", "RUB": "🇷🇺", "TRY": "🇹🇷",
    "AED": "🇦🇪", "SAR": "🇸🇦", "KRW": "🇰🇷", "THB": "🇹🇭", "MYR": "🇲🇾",
    "IDR": "🇮🇩", "PHP": "🇵🇭", "PLN": "🇵🇱", "CZK": "🇨🇿", "HUF": "🇭🇺",
    "ILS": "🇮🇱", "CLP": "🇨🇱", "COP": "🇨🇴", "PKR": "🇵🇰", "BDT": "🇧🇩",
    "EGP": "🇪🇬", "VND": "🇻🇳", "UAH": "🇺🇦", "NGN": "🇳🇬", "KWD": "🇰🇼",
    "QAR": "🇶🇦", "OMR": "🇴🇲", "BHD": "🇧🇭", "JOD": "🇯🇴", "TWD": "🇹🇼",
    "RON": "🇷🇴", "HRK": "🇭🇷", "BGN": "🇧🇬",
}


@app.route("/")
def index():
    return render_template("index.html",
                           currencies=sorted(CURRENCY_NAMES.keys()),
                           currency_names=CURRENCY_NAMES,
                           currency_flags=CURRENCY_FLAGS)


@app.route("/api/convert")
def convert():
    from_currency = request.args.get("from", "USD").upper()
    to_currency = request.args.get("to", "EUR").upper()
    amount = request.args.get("amount", "1")

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    try:
        response = requests.get(f"{BASE_URL}/{from_currency}", timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            return jsonify({"error": "API error: " + data.get("error-type", "unknown")}), 500

        rates = data["rates"]
        if to_currency not in rates:
            return jsonify({"error": f"Currency {to_currency} not supported"}), 400

        rate = rates[to_currency]
        converted = amount * rate
        last_updated = data.get("time_last_update_utc", "Unknown")

        return jsonify({
            "from": from_currency,
            "to": to_currency,
            "amount": amount,
            "converted": round(converted, 6),
            "rate": rate,
            "last_updated": last_updated,
            "from_name": CURRENCY_NAMES.get(from_currency, from_currency),
            "to_name": CURRENCY_NAMES.get(to_currency, to_currency),
            "from_flag": CURRENCY_FLAGS.get(from_currency, "💱"),
            "to_flag": CURRENCY_FLAGS.get(to_currency, "💱"),
        })

    except requests.Timeout:
        return jsonify({"error": "Request timed out. Please try again."}), 504
    except requests.RequestException as e:
        return jsonify({"error": f"Network error: {str(e)}"}), 503


@app.route("/api/rates")
def rates():
    """Get all rates for a base currency."""
    base = request.args.get("base", "USD").upper()
    try:
        response = requests.get(f"{BASE_URL}/{base}", timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            return jsonify({"error": "API error"}), 500

        filtered_rates = {
            k: v for k, v in data["rates"].items()
            if k in CURRENCY_NAMES
        }

        return jsonify({
            "base": base,
            "rates": filtered_rates,
            "last_updated": data.get("time_last_update_utc", "Unknown"),
        })
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 503


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "production") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug)
