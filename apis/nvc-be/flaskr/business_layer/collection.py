import datetime
import math
from flaskr.data_layer.collection import CollectionDataLayer
import json
from web3 import Web3


class CollectionBusinessLayer:

    def __init__(self, db_config):
        self.data_layer = CollectionDataLayer(db_config)

    def get_collections_report(self, datetime):
        result = self.data_layer.get_collections_report(datetime)

        if not result:
            return None

        rows = []

        for row in result:
            rows.append(
                {
                    "id": row["Id"],
                    "name": row["Name"],
                    "description": row["Description"],
                    "ipfs": row["Ipfs"],
                    "price": row["Price"],
                    "address": row["Address"],
                    "totalSupply": row["TotalSupply"],
                    "networkId": row["NetworkId"],
                    "maturity": row["Maturity"],
                    "totalMinted": row["TotalMinted"],
                    "totalSentOut": row["TotalMinted"],
                    "interestRate": row["InterestRate"],
                    "nextPayDate": str(row["NextPayDate"]),
                    "transactions": json.loads(row["Transactions"]) if row["Transactions"] else [],
                    "interestRecorded": row["TotalInterestRecorded"],
                    "interestPaid": row["TotalInterestPaid"],
                }
            )

        return rows

    def get_collections(self):
        result = self.data_layer.get_collections()

        if not result:
            return None

        rows = []
        #MIN(hbm.CollectionId), MIN(hbd.TokenId), SnapshotDate, MIN(cu.Interest), MIN(cu.Principal),  MIN(hbm.UpdateAppliedId) , SUM(hbd.InterestEarnedInMonth), SUM(hbd.HoldDaysInMonth)
        for row in result:
            id, name, description, price, ipfs = row
            rows.append(
                {
                    "id": id,
                    "name": name,
                    "description": description,
                    "ipfs": ipfs,
                    "price": price
                }
            )

        return rows

    def get_nft_detail_current(
        self, collection_id, token_id, snapshot_date
    ):
        data = self.data_layer.get_nft_detail_current(
            collection_id, token_id, snapshot_date)
        print(data)
        if not data:
            return None

        return {
            "datetime": str(data["SnapshotDate"]),
            "interestRate": data["Interest"],
            "principal": data["Principal"],
            "interestEarned": data["InterestEarnedInMonth"],
            "holdDays": data["HoldDaysInMonth"],
            "updateAppliedId": data["UpdateAppliedId"],
        }

    def get_nft_detail_history(
        self, collection_id, token_id, snapshot_date
    ):
        rows = self.data_layer.get_nft_detail_history(
            collection_id, token_id, snapshot_date)

        if not rows:
            return None
        history = []

        for row in rows:
            history.append(
                {
                    "datetime": str(row["SnapshotDate"]),
                    "interestRate": row["Interest"],
                    "principal": row["Principal"],
                    "paid": row["Paid"] == b'\x01',
                    "interestEarned": row["InterestEarnedInMonth"],
                    "holdDays": row["HoldDaysInMonth"],
                    "updateAppliedId": row["UpdateAppliedId"],
                }
            )

        return history

    def get_collection_latest_holder_by_month(self, collection_id, snapshot_date):
        snapshot_date = snapshot_date or datetime.date.today()
        reset_date, = self.data_layer.get_collection_latest_holder_by_month(
            collection_id, snapshot_date)
        return reset_date

    def get_collection_with_updates_by_id(self, collection_id):
        data = self.data_layer.get_collection_with_updates_by_id(collection_id)
        if not data['collection_info']:
            return None
        (
            id,
            start_date,
            end_date,
            ipfs,
            total_supply,
            address,
            price,
            network_id,
            name,
            description,
            _,
            _,
            _,
            _,
            _,
            buy_back_o,
            _,
            master_wallet,
        ) = data['collection_info'][0]
        contracts = data['contracts']
        print(12, contracts)
        return {
            "id": id,
            "startDate": str(start_date),
            "endDate": str(end_date),
            "ipfs": ipfs,
            "totalSupply": total_supply,
            "address": address,
            "networkId": network_id,
            "price": price,
            "name": name,
            "description": description,
            "updates": [
                {
                    "principal": principal,
                    "interest": interest,
                    "from_date": str(from_date),
                    "type": type,
                    "message": message,
                    "buyBack": str(buy_back)[-2] == "1",
                    "id": cu_id,
                }
                for _, _, _, _, _, _, _, _, _, _, principal, interest, from_date, type, message, buy_back, cu_id, master_wallet in data["collection_info"]
            ],
            "master_wallet": master_wallet,
            "contracts": [{
                "id": contract_id,
                "date": str(date),
                "contract": contract,
                "profit": profit,
                "value": value,
                "period": period,
                "status": status,
                "tx_id": tx_id,
                "tx_link": tx_link,
            }
                for contract_id, date, contract, profit, value, period, status, tx_id, tx_link in contracts
            ]

        }

    def get_nft_current(
        self, collection_id, token_id, wallet_address, snapshot_date=None
    ):

        wallet_address = Web3.toChecksumAddress(wallet_address)
        snapshot_date = snapshot_date or datetime.date.today()
        result = self.data_layer.get_nft_current(
            collection_id, token_id, wallet_address, snapshot_date)

        if not result:
            return None
        (
            holder,
            data_collection_id,
            data_token_id,
            data_snapshot_date,
            interest,
            principal,
            updateAppliedId,
            hold_days,
        ) = result

        return {
            "datetime": str(data_snapshot_date),
            # "paid": False,
            "interestRate": interest,
            "principal": principal,
            "updateAppliedId": updateAppliedId,
            "holdDaysInCurrentMonth": hold_days,
        }

    def get_nfts_summary_by_wallet(
        self, collection_id, wallet_address, snapshot_date=None
    ):
        wallet_address = Web3.toChecksumAddress(wallet_address)
        snapshot_date = snapshot_date or datetime.date.today()
        result = self.data_layer.get_nfts_summary_by_wallet(
            collection_id, wallet_address, snapshot_date)

        if not result:
            return None

        holder, sum_InterestEarnedInMonth, count_TokenId = result
        return {
            "walletAddress": holder,
            "totalEarnInCurrentMonth": sum_InterestEarnedInMonth,
            "totalNftsInCurrentMonth": count_TokenId,
        }

    def get_unique_holder(self, collection_id, date_time=None):
        date_time = date_time or datetime.date.today()
        result = self.data_layer.get_unique_holder(
            collection_id, date_time)

        return result[0]

    def get_total_pay(self, collection_id, date_time=None):
        date_time = date_time or datetime.date.today()
        result = self.data_layer.get_total_pay(collection_id, date_time)
        return result[0]

    def get_reset_day(self, collection_id, date_time=None):
        date_time = date_time or datetime.date.today()
        result = self.data_layer.get_reset_day(collection_id, date_time)
        return result[0]

    def get_report_data(self, collection_id, date_time=None):
        date_time = date_time or datetime.date.today()
        result = self.data_layer.get_report_data(collection_id, date_time)
        return (result[0][0], result[0][1], result[0][2], result[0][3])

    def get_reset_day(self, collection_id, date_time=None):
        date_time = date_time or datetime.date.today()
        result = self.data_layer.get_reset_day(collection_id, date_time)
        return result[0]
