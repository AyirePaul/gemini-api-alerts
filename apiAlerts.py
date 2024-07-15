import argparse
import json
import logging
import math
import sys

import requests

base_url = "https://api.gemini.com"

parser = argparse.ArgumentParser(description='AlertingTool - INFO - Parsing args')
parser.add_argument('-c', '--currency', default="All", type=str,
                    help='The currency trading pair, or All. Defaults to All')
parser.add_argument('-d', '--deviation', default=1, type=float,
                    help='Standard deviation threshold. e.g. 1. Defaults to 1.')
args = parser.parse_args()

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "trading_pair": "%(trading_pair)s", '
           '"deviation": %(deviation)s, "data": %(message)s}',
    datefmt='%Y-%m-%dT%H:%M:%S%z')


def alert(message, trading_pair, level=logging.INFO, deviation=None):
    logging.log(level, json.dumps(message), extra={"trading_pair": trading_pair,
                                                   "deviation": deviation if deviation else "null"})


def calculate_changes(data):
    # Convert the string prices to float
    open_price = float(data["open"])
    prices = [float(price) for price in data["changes"]]

    # last price is same as close price (most recent trade)
    last_price = float(data["close"])

    # Calculate the average price
    average = sum(prices) / len(prices)

    # price change
    change = last_price - open_price

    # Calculate the standard deviation
    squared_diffs = [(price - average) ** 2 for price in prices]
    sdev = math.sqrt(sum(squared_diffs) / (len(prices) - 1))

    return {
        "last_price": f"{last_price:.2f}",
        "average": f"{average:.2f}",
        "change": f"{change:.2f}",
        "sdev": f"{sdev:.1f}"
    }


def process_trading_pair(trading_pair):
    try:
        # Make the request
        response = requests.get(base_url + "/v2/ticker/" + trading_pair)

        # Check the status code
        if response.status_code == 200:
            # process the changes
            changes = calculate_changes(response.json())

            alert(message=changes, trading_pair=trading_pair,
                  deviation=str(float(changes["sdev"]) > args.deviation).lower())
        else:
            alert(message=f"Error retrieving data from ticker endpoint. Status code: {response.status_code}",
                  level=logging.ERROR, trading_pair=trading_pair)

    except requests.exceptions.RequestException as e:
        alert(message=f"Error making the request: {e}", level=logging.ERROR, trading_pair=trading_pair)


if args.currency == "All":
    try:
        # Make the request for symbols
        _response = requests.get(base_url + "/v1/symbols")

        symbols = _response.json()

        # process the changes
        for _trading_pair in symbols:
            process_trading_pair(_trading_pair)

    except requests.exceptions.RequestException as e:
        # Log the error
        alert(message=f"Error making the request: {e}", level=logging.ERROR, trading_pair="")
else:
    process_trading_pair(args.currency)
