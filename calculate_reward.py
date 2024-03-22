def calculate_reward(events: list[tuple[str, int, int]]) -> dict[str, float]:
    USDT_POOL = 10_000
    MAX_TIMESTAMP = 3_600
    TIMESTAMP = 0

    order_by_timestamp = lambda a: a[1]
    events.sort(key=order_by_timestamp)

    user_shares = dict()
    user_balances = dict()

    while TIMESTAMP < MAX_TIMESTAMP:
        for idx, event in enumerate(events):
            user, timestamp, share = event

            if timestamp == TIMESTAMP:
                if user_shares.get(user) != None:
                    user_shares[user] += share
                else:
                    user_shares.setdefault(user, share)
                    user_balances.setdefault(user, 0)
                events.pop(idx)

        for user in user_shares:
            distribution = USDT_POOL/MAX_TIMESTAMP
            sum_shares = sum(map(lambda v: user_shares[v], user_shares))
            user_share = user_shares[user]*distribution/sum_shares
            user_balances[user] += user_share
            # print(f'{TIMESTAMP:04} - {user}: share={user_shares[user]} {distribution=} add={user_share} sum={user_balances[user]}')

        TIMESTAMP += 1

    return dict(map(lambda balance: (balance[0], round(balance[1], 3)), user_balances.items()))

def test_calculate_reward():
    # Default case
    assert calculate_reward([('A', 0, 2), ('B', 1, 1), ('A', 10, -1)]) == {'A': 5005.556, 'B': 4994.444}
