import database_script as db

wallets_current = [
    token_holder["wallet"]
    for token_holder in db.extract_token_holders("1_2022-07-01.txt")
]
wallets_in = [
    token_holder["wallet"]
    for token_holder in db.extract_token_holders("1_2022-07-02.txt")
]

new_wallets = [
    wallet_in for wallet_in in wallets_in if (wallet_in not in wallets_current)
]
print(len(new_wallets))
