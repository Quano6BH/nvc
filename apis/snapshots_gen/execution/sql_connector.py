from execution.base_connector import BaseConnector


class CollectionDataLayer(BaseConnector):
    COLLECTION_TABLE_NAME = "Collection"
    COLLECTIONUPDATE_TABLE_NAME = "CollectionUpdate"
    HOLDERBYDATE_TABLE_NAME = "HolderByDate"
    HOLDERBYMONTH_TABLE_NAME = "HolderByMonth"
    NFT_TABLE_NAME = "Nft"
    NFTHOLDER_TABLE_NAME = "NftHolder"
    WALLET_TABLE_NAME = "Wallet"

    def __init__(self, db_config):
        BaseConnector.__init__(self, db_config)

    insert_nft_id_database_script = f"""
        INSERT IGNORE INTO {NFT_TABLE_NAME} (TokenId, CollectionId) VALUES 
        $value;
    """

    def insert_nft_id(self, collection_id, collection_total_supply):
        rows = []
        for token_id in range(0, collection_total_supply):
            rows.append(f"({token_id}, {collection_id})")
        value = (",").join(rows)
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:
                self._execute_query(
                    cursor=cursor,
                    query_template=self.insert_nft_id_database_script,
                    value=value,
                )
                db_connection.commit()

    insert_wallets_database_script = f"""
        INSERT IGNORE INTO {WALLET_TABLE_NAME} (Address) VALUES 
        $wallets;
    """

    def insert_wallets(self, wallets):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:
                self._execute_query(
                    cursor=cursor,
                    query_template=self.insert_wallets_database_script,
                    wallets=(",").join(
                        [f"('{wallet}')" for wallet in wallets]),
                )
                db_connection.commit()

    fetch_closest_update_query_template = f"""
        SELECT FromDate, Principal, Interest, Id FROM {COLLECTIONUPDATE_TABLE_NAME} 
        WHERE (TIMESTAMPDIFF(day, FromDate, '$date')) <= 0 
        AND CollectionId = $collection_id 
        AND Type = 'Update'
        ORDER BY FromDate ASC LIMIT 1;
    """

    def fetch_closest_update(self, date, collection_id):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:
                self._execute_query(
                    cursor=cursor,
                    query_template=self.fetch_closest_update_query_template,
                    date=date,
                    collection_id=collection_id,
                )
                return cursor.fetchall()

    insert_nft_holder_database_script = f"""
        INSERT INTO {NFTHOLDER_TABLE_NAME} (TokenId, CollectionId, Holder, Principal, Interest, SnapshotDate) VALUES 
        $value;
    """

    def insert_nft_holder(
        self, token_holders, collection_id, principal, interest, snapshot_date
    ):
        rows = []
        for row in token_holders:
            token_id = row["token_id"]
            wallet = row["wallet"]
            rows.append(
                f"({token_id},{collection_id},'{wallet}',{principal}, {interest}, '{snapshot_date}')"
            )
        value = (",").join(rows)
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:
                self._execute_query(
                    cursor=cursor,
                    query_template=self.insert_nft_holder_database_script,
                    value=value,
                )
                db_connection.commit()

    fetch_data_by_date_query_template = f"""
        SELECT Holder, TokenId, HoldDays, HoldDaysInMonth, InterestEarned, InterestEarnedInMonth, SnapshotDate 
        FROM {HOLDERBYDATE_TABLE_NAME} 
        WHERE SnapshotDate = '$snapshot_date' 
        AND CollectionId = $collection_id;
    """

    def fetch_data_by_date(self, snapshot_date, collection_id):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:
                self._execute_query(
                    cursor=cursor,
                    query_template=self.fetch_data_by_date_query_template,
                    snapshot_date=snapshot_date,
                    collection_id=collection_id,
                )
                return cursor.fetchall()

    insert_holder_by_date_database_script = f"""
        INSERT INTO {HOLDERBYDATE_TABLE_NAME} 
        (Holder, TokenId, CollectionId, HoldDays, HoldDaysInMonth, InterestEarned, InterestEarnedInMonth, SnapshotDate, UpdateAppliedId, Holding) 
        VALUES $value;
    """

    def insert_holder_by_date(
        self, new_report, collection_id, snapshot_date, update_applied_id
    ):
        rows = []
        for holder in new_report.keys():
            for token_id in new_report[holder]["token_ids"].keys():
                hold_days = new_report[holder]["token_ids"][token_id]["holding_day"]
                hold_days_in_month = new_report[holder]["token_ids"][token_id][
                    "holding_day_in_month"
                ]
                interest_earned = new_report[holder]["token_ids"][token_id]["interest"]
                interest_earned_in_month = new_report[holder]["token_ids"][token_id][
                    "interest_in_month"
                ]
                holding = (
                    1 if new_report[holder]["token_ids"][token_id]["holding"] else 0
                )
                rows.append(
                    f"('{holder}',{token_id}, {collection_id},{hold_days}, {hold_days_in_month},{interest_earned}, {interest_earned_in_month},'{snapshot_date}',{update_applied_id}, {holding})"
                )
        value = (",").join(rows)
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:
                self._execute_query(
                    cursor=cursor,
                    query_template=self.insert_holder_by_date_database_script,
                    value=value,
                )
                db_connection.commit()

    insert_holder_by_month_database_script = f"""
        INSERT INTO {HOLDERBYMONTH_TABLE_NAME} (Holder, CollectionId, ResetDate, TotalNFTs, InterestEarned, UpdateAppliedId) 
        VALUES $value
    """

    def insert_holder_by_month(
        self, last_day_report, collection_id, reset_date, update_applied_id
    ):
        rows = []
        for holder in last_day_report.keys():
            total_nfts = 0
            interest_earned = 0
            for token_id in last_day_report[holder]["token_ids"].keys():
                total_nfts += last_day_report[holder]["token_ids"][token_id][
                    "holding_day"
                ]
                interest_earned += last_day_report[holder]["token_ids"][token_id][
                    "interest"
                ]
            rows.append(
                f"('{holder}',{collection_id},'{reset_date}',{total_nfts},{interest_earned},{update_applied_id})"
            )
        value = (",").join(rows)
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:
                self._execute_query(
                    cursor=cursor,
                    query_template=self.insert_holder_by_date_database_script,
                    value=value,
                )
                db_connection.commit()
    fetch_collection_address_query_template = f"""
        SELECT Address FROM {COLLECTION_TABLE_NAME}
        WHERE Id = $collection_id
    """

    def fetch_collection_address(self, collection_id):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:
                self._execute_query(
                    cursor=cursor,
                    query_template=self.fetch_collection_address_query_template,
                    collection_id=collection_id
                )
                return cursor.fetchall()
