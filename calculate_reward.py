USDT_POOL = 10_000
MAX_TIMESTAMP = 3_600

DISTRIBUTION_EACH_TIMESTAMP = USDT_POOL / MAX_TIMESTAMP

# utils functions
is_type_equal = lambda a, t: type(a) == t
is_str = lambda a: is_type_equal(a, str)
is_int = lambda a: is_type_equal(a, int)
is_zero = lambda a: a == 0
is_greater_than_zero = lambda a: a > 0
is_below_max_timestamp = lambda a: a < MAX_TIMESTAMP
is_natural_number = lambda a: is_zero(a) or is_greater_than_zero(a)
is_between_zero_and_max_timestamp = lambda a: is_natural_number(a) and is_below_max_timestamp(a) 

# filter functions
invalid_user = lambda a: is_str(a[0])
invalid_timestamp = lambda a: is_int(a[1]) and is_between_zero_and_max_timestamp(a[1])
invalid_share = lambda a: is_int(a[2]) and not is_zero(a[2])
is_timestamp_greater = lambda b: lambda a: a[1] > b

# sort functions
order_by_timestamp = lambda a: a[1]

# map functions
format_to_three_decimal_points = lambda a: (a[0], round(a[1], 3))
apply_filter = lambda f: lambda a: list(filter(f, a))

def calculate_reward(events: list[tuple[str, int, int]]) -> dict[str, float]:
    # Initialize current timestamp
    CURRENT_TIMESTAMP = 0

    # Filter unwanted events
    events = apply_filter(invalid_user)(events)
    events = apply_filter(invalid_timestamp)(events)
    events = apply_filter(invalid_share)(events)

    # Sort events by timestamp
    events.sort(key=order_by_timestamp)
    
    # Initialize user shares and balances
    user_shares = dict()
    user_balances = dict()

    # Loop through each timestamp until timestamp is equal to max timestamp
    while CURRENT_TIMESTAMP < MAX_TIMESTAMP:
        # Update user shares
        for event in events:
            user, timestamp, share = event

            # Update user shares if timestamp is current timestamp
            if timestamp == CURRENT_TIMESTAMP:
                # Update user share if user exists
                if user_shares.get(user) is not None:
                    user_shares[user] = max(0, user_shares[user]+share)
                # Create new user share if user does not exist
                elif is_greater_than_zero(share):
                    user_shares.setdefault(user, share)
                    user_balances.setdefault(user, 0)

        # Calculate sum of user shares in current timestamp
        sum_shares = sum(user_shares.values())

        # Check if user shares is able to distribute
        if is_greater_than_zero(sum_shares):
            # Distribute USDT to users
            for user in user_shares:
                # Distribute USDT to user based on shares and distribution each timestamp
                user_balances[user] += user_shares[user] * DISTRIBUTION_EACH_TIMESTAMP / sum_shares

        # Remove events which is past current timestamp
        events = apply_filter(is_timestamp_greater(CURRENT_TIMESTAMP))(events)

        # Increment current timestamp
        CURRENT_TIMESTAMP += 1

    # Format user balances to three decimal points then return
    return dict(map(format_to_three_decimal_points, user_balances.items()))

if __name__ == '__main__':
    print(calculate_reward([('A', 0, 2), ('B', 1, 1), ('A', 10, -1)]))