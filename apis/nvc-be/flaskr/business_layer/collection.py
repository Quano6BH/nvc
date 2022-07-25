import datetime
import math
from flaskr.data_layer.collection import CollectionDataLayer

from web3 import Web3


class CollectionBusinessLayer:

    def __init__(self, db_config):
        self.data_layer = CollectionDataLayer(db_config)
    def get_collection_interest_report(self, collection_id, snapshot_date):
        snapshot_date = snapshot_date or datetime.date.today()
        
        reset_date, = self.data_layer.get_collection_latest_holder_by_month(collection_id, snapshot_date)
        # by_date_snapshot_Date = datetime.datetime.strptime(reset_date, "%Y-%m-%d")
        data = self.data_layer.get_collection_interest_report(collection_id, reset_date- datetime.timedelta(days=1))
        
        result ={
            "data":[],
            "parsed":""
        }
        for wallet_data in data:
            interest = "{:.2f}".format(wallet_data[1])
            result["data"].append({
                "wallet":wallet_data[0],
                "interest":interest
            })
            result["parsed"]+=f"{wallet_data[0]}={interest}\n"
        
        return result

    def get_collection_with_updates_by_id(self, collection_id):
        data = self.data_layer.get_collection_with_updates_by_id(collection_id)
        if not data:
            return None
        (
            id,
            start_date,
            end_date,
            ipfs,
            total_supply,
            address,
            network_id,
            _,
            _,
            _,
            _,
            _,
            buy_back_o,
            _,
        ) = data[0]

        return {
            "id": id,
            "startDate": str(start_date),
            "endDate": str(end_date),
            "ipfs": ipfs,
            "totalSupply": total_supply,
            "address": address,
            "networkId": network_id,
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
                for _, _, _, _, _, _, _, principal, interest, from_date, type, message, buy_back, cu_id in data
            ],
        }

    def get_nft_history(
        self, collection_id, token_id, wallet_address
    ):
        wallet_address = Web3.toChecksumAddress(wallet_address)
        result = self.data_layer.get_nft_history(
            collection_id, token_id, wallet_address)
        if not result:
            return None
        earnings = []

        for row in result:
            _, _, _, row_snapshot_date, interest, principal, paid, updateAppliedId = row
            earnings.append(
                {
                    "datetime": str(row_snapshot_date),
                    "paid": paid == b"\x01",
                    "interestRate": interest,
                    "principal": principal,
                    "updateAppliedId": updateAppliedId,
                }
            )

        return earnings

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
            "paid": False,
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

    def get_wallet_nfts(self, collection_id, wallet_address, snapshot_date=None):
        wallet_address = Web3.toChecksumAddress(wallet_address)
        snapshot_date = snapshot_date or datetime.date.today()
        result = self.data_layer.get_wallet_nfts(
            collection_id, wallet_address, snapshot_date)
        if not result:
            return None

        totalEarnInCurrentMonth, kyc = result

        if not totalEarnInCurrentMonth:
            return None

        data = {
            "totalEarnInCurrentMonth": totalEarnInCurrentMonth,
            "kyc": kyc == b'\x01',
            "walletAddress": wallet_address
        }

        return data

    def get_unique_holder(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        result = self.data_layer.get_unique_holder(
            collection_id, snapshot_date)

        return result[0]

    def get_total_pay(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        result = self.data_layer.get_total_pay(collection_id, snapshot_date)
        return result[0]

    def get_reset_day(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        result = self.data_layer.get_reset_day(collection_id, snapshot_date)
        return result[0]

    def get_report_data(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        result = self.data_layer.get_report_data(collection_id, snapshot_date)
        return (result[0][0], result[0][1], result[0][2], result[0][3])

    def get_reset_day(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        result = self.data_layer.get_reset_day(collection_id, snapshot_date)
        return result[0]
