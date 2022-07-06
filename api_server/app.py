import os
import json
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import datetime


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/collections/1")
@cross_origin()
def collection_id():
    with open("json/collectionId.json", "r") as file:
        data = json.loads(file.read())
    return jsonify(data)


@app.route("/collections/1/report")
@cross_origin()
def collection_report():
    try:
        with open("json/collection_report.json", "r") as file:
            data = json.loads(file.read())
        with open("json/03_07_2022.json", "r") as file:
            read_data = json.loads(file.read())
        data["uniqueHolders"] = len(read_data)
        return jsonify(data), 200
    except:
        return "statusCode 403", 403


@app.route("/wallets/<wallet_address>")
@cross_origin()
def get_wallets(wallet_address):
    try:
        with open("json/wallets.json", "r") as file:
            data = json.loads(file.read())
        with open("json/h22.json", "r") as file:
            wallets = json.loads(file.read())[wallet_address]
        count = 0.0
        for token_id in wallets["tokenIds"]:
            count += wallets["tokenIds"][token_id]["interest"]
        data["totalEarnInCurrentMonth"] = count
        return jsonify(data), 200
    except KeyError:
        return "statusCode 404", 404


@app.route("/wallets/<wallet_address>/nfts/<nft_id>")
@cross_origin()
def get_nft_info(wallet_address, nft_id):
    with open("json/03_07_2022.json", "r") as file:
        nft = json.loads(file.read())

    with open("json/collectionId.json", "r") as file:
        collection_id = json.loads(file.read())

    with open("json/nft_id.json", "r") as file:
        data = json.loads(file.read())
    try:
        interest_rate = collection_id["updates"][0]["interest"]
        principal = collection_id["updates"][0]["principal"]
        current_owner = wallet_address
        holding_day = nft[wallet_address]["tokenIds"][nft_id]["holding_day"]
        interest = nft[wallet_address]["tokenIds"][nft_id]["interest"]
        data["tokenId"] = nft_id
        data["currentOwner"] = current_owner
        data["holdDaysInCurrentMonth"] = int(holding_day)
        data["earnings"]["05/2022"]["interestEarned"] = interest
        data["earnings"]["05/2022"] = {
            "interestEarned": interest,
            "interestRate": interest_rate,
            "principalRate": principal,
            "principalEarned": principal * holding_day,
        }
        data["earnings"]["06/2022"]["interestEarned"] = interest
        data["earnings"]["06/2022"] = {
            "interestEarned": interest,
            "interestRate": interest_rate,
            # "principalRate": principal,
            # "principalEarned": principal * holding_day,
        }
        return jsonify(data), 200
    except KeyError:
        return "statusCode 404", 404


try:
    if sys.argv[1] == "-p":
        usr_port = sys.argv[2]
    app.run(host="0.0.0.0", port=usr_port, debug=True)
except:
    app.run(host="127.0.0.1", port=5555, debug=True)
