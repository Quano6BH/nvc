import datetime
from flaskr.data_layer.wallet import WalletDataLayer

from web3 import Web3


class WalletBusinessLayer:

    def __init__(self, db_config):
        self.data_layer = WalletDataLayer(db_config)

    def get_nft_history_of_wallet(self, wallet_address, collection_id, token_id, snapshot_date):

        wallet_address = Web3.toChecksumAddress(wallet_address)
        snapshot_date = snapshot_date or datetime.date.today()

        rows = self.data_layer.get_nft_history_of_wallet(wallet_address,
                                                         collection_id, token_id, snapshot_date)

        if not rows:
            return None

        history = []
        for row in rows:
            #hbd.Holder, hbd.CollectionId, hbd.TokenId, SnapshotDate, cu.Interest, cu.Principal,
            #    hbd.UpdateAppliedId, hbd.HoldDaysinMonth, hbd.InterestEarnedInMonth, hbm.Paid
            (
                holder,
                data_collection_id,
                data_token_id,
                data_snapshot_date,
                interest,
                principal,
                updateAppliedId,
                hold_days_in_month,
                interest_earned_in_month,
                paid
            ) = row

            history.append(
                {
                    "datetime": str(data_snapshot_date),
                    "paid": str(paid)[-2] == "1",
                    "interestRate": interest,
                    "principal": principal,
                    "updateAppliedId": updateAppliedId,
                    "holdDays": hold_days_in_month,
                    "interestEarned": interest_earned_in_month,
                }
            )

        return history

    def get_nft_detail_in_current_month_of_wallet(self, wallet_address, collection_id, token_id, snapshot_date):

        wallet_address = Web3.toChecksumAddress(wallet_address)
        snapshot_date = snapshot_date or datetime.date.today()

        result = self.data_layer.get_nft_detail_in_current_month_of_wallet(wallet_address,
                                                                           collection_id, token_id, snapshot_date)

        if not result:
            return None

        # hbd.Holder, hbd.CollectionId, hbd.TokenId, SnapshotDate, cu.Interest, cu.Principal,
        #             hbd.UpdateAppliedId, hbd.HoldDaysinMonth, hbd.InterestEarnedInMonth
        (
            holder,
            data_collection_id,
            data_token_id,
            data_snapshot_date,
            interest,
            principal,
            updateAppliedId,
            hold_days_in_month,
            interest_earned_in_month
        ) = result

        return {
            "datetime": str(data_snapshot_date),
            "interestRate": interest,
            "principal": principal,
            "updateAppliedId": updateAppliedId,
            "holdDays": hold_days_in_month,
            "interestEarned": interest_earned_in_month,
        }

    def get_wallet_collection_info(self, wallet_address, collection_id, date_time):
        wallet_address = Web3.toChecksumAddress(wallet_address)

        date_time = date_time or datetime.date.today()
        rows = self.data_layer.get_wallet_collection_info(
            wallet_address, collection_id, date_time)
        if not rows:
            return None

        address, kyc, _, _, _, snapshot_date, _ = rows[0]
        nfts_data = []
        total_earned_in_month = 0
        for row in rows:
            #Address, Kyc, InterestEarnedInMonth, HoldDaysInMonth,TokenId,SnapshotDate, Holding
            _, _, interest_earned_in_month, hold_days_in_month, token_id, _, holding = row
            nfts_data .append({
                "tokenId": token_id,
                "holdDaysInMonth": hold_days_in_month,
                "interestEarnedInMonth": interest_earned_in_month,
                "holding": str(holding)[-2] == "1",
            })
            total_earned_in_month += interest_earned_in_month

        return {
            "kyc": kyc == b'\x01',
            "walletAddress": address,
            "snapshot_date": snapshot_date,
            "totalEarnedInMonth": total_earned_in_month,
            "nfts": nfts_data
        }

    def get_wallet_info(self, wallet_address):
        wallet_address = Web3.toChecksumAddress(wallet_address)

        data = self.data_layer.get_wallet_info(
            wallet_address)

        if not data:
            return None

        return {
            "kyc": data["Kyc"] == b'\x01',
            "walletAddress": data["Address"],
        }
    def update_wallet_kyc(self, wallet_address, kyc=True):
        self.data_layer.update_wallet_kyc(wallet_address, kyc)

    def update_wallets_kyc(self, wallet_addresses, kyc=True):
        self.data_layer.update_wallets_kyc(wallet_addresses, kyc)
