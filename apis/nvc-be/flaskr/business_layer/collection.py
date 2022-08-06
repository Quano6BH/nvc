import datetime
import math
from flaskr.data_layer.collection import CollectionDataLayer

from web3 import Web3


class CollectionBusinessLayer:

    def __init__(self, db_config):
        self.data_layer = CollectionDataLayer(db_config)

    def get_nft_interest_history(
        self, collection_id, token_id, snapshot_date
    ):
        result = self.data_layer.get_nft_interest_history(
            collection_id, token_id, snapshot_date)

        if not result:
            return None

        history = []
        #MIN(hbm.CollectionId), MIN(hbd.TokenId), SnapshotDate, MIN(cu.Interest), MIN(cu.Principal),  MIN(hbm.UpdateAppliedId) , SUM(hbd.InterestEarnedInMonth), SUM(hbd.HoldDaysInMonth) 
        for row in result:
            _, _, row_snapshot_date, interest, principal, updateAppliedId, interest_earned_in_month, hold_days_in_month  = row
            history.append(
                {
                    "datetime": str(row_snapshot_date),
                    "interestRate": interest,
                    "principal": principal,
                    "interestEarned": interest_earned_in_month,
                    "holdDays": hold_days_in_month,
                    "updateAppliedId": updateAppliedId,
                }
            )

        return history

    def get_collection_latest_holder_by_month(self, collection_id, snapshot_date):
        snapshot_date = snapshot_date or datetime.date.today()
        reset_date, = self.data_layer.get_collection_latest_holder_by_month(
            collection_id, snapshot_date)
        return reset_date

    def get_collection_monthly_interest_snapshot(self, collection_id, datetime):
        # by_date_snapshot_Date = datetime.datetime.strptime(reset_date, "%Y-%m-%d")

        data = self.data_layer.get_collection_monthly_interest_snapshot(
            collection_id, datetime)

        result = {
            "data": {
                "interest": snapshot_date_interest_principal[1],
                "principal": snapshot_date_interest_principal[0],
                "monthly_snapshot": []
            },
            "parsed": ""
        }
        for wallet_data in data:
            # interest = "{:.2f}".format(wallet_data[1])
            result["data"]['monthly_snapshot'].append({
                "wallet": wallet_data[0],
                "interest": wallet_data[1],
                "holding_count": int(wallet_data[2])
            })
            result["parsed"] += f"{wallet_data[0]}={wallet_data[1]}\n"

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
