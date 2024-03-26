from calculate_reward import calculate_reward

def test_calculate_reward():
    default = calculate_reward([('A', 0, 2), ('B', 1, 1), ('A', 10, -1)])
    assert type(default) == dict
    assert len(default) == 2
    assert default == {'A': 5005.556, 'B': 4994.444}

def test_empty_calculate_reward():
    empty = calculate_reward([])
    assert type(empty) == dict
    assert len(empty) == 0
    assert empty == {}

def test_invalid_user_calculate_reward():
    invalid_user = calculate_reward([('A', 0, 2), ('B', 1, 1), ('A', 10, -1), (100, 10, 1)])
    assert type(invalid_user) == dict
    assert len(invalid_user) == 2
    assert invalid_user == {'A': 5005.556, 'B': 4994.444}

def test_invalid_timestamp_calculate_reward():
    invalid_timestamp = calculate_reward([('A', 0, 2), ('B', 1, 1), ('A', 10, -1), ('B', '1', 1)])
    assert type(invalid_timestamp) == dict
    assert len(invalid_timestamp) == 2
    assert invalid_timestamp == {'A': 5005.556, 'B': 4994.444}

def test_invalid_share_calculate_reward():
    invalid_share = calculate_reward([('A', 0, 2), ('B', 1, 1), ('A', 10, -1), ('B', 1, '1')])
    assert type(invalid_share) == dict
    assert len(invalid_share) == 2
    assert invalid_share == {'A': 5005.556, 'B': 4994.444}

def test_timestamp_exceed_calculate_reward():
    timestamp_exceed = calculate_reward([('A', 0, 2), ('B', 1, 1), ('A', 10, -1), ('B', 3_900, 1)])
    assert type(timestamp_exceed) == dict
    assert len(timestamp_exceed) == 2
    assert timestamp_exceed == {'A': 5005.556, 'B': 4994.444}

def test_timestamp_subceed_calculate_reward():
    timestamp_subceed = calculate_reward([('B', -1, 1), ('A', 0, 2), ('B', 1, 1), ('A', 10, -1)])
    assert type(timestamp_subceed) == dict
    assert len(timestamp_subceed) == 2
    assert timestamp_subceed == {'A': 5005.556, 'B': 4994.444}

def test_timestamp_invalid_calculate_reward():
    timestamp_invalid = calculate_reward([('B', -1, 1), ('A', 0, 2), ('B', 1, 1), ('A', 10, -1), ('B', 3_900, 1)])
    assert type(timestamp_invalid) == dict
    assert len(timestamp_invalid) == 2
    assert timestamp_invalid == {'A': 5005.556, 'B': 4994.444}

def test_zero_share_calculate_reward():
    zero_share = calculate_reward([('A', 0, 0), ('B', 1, 1)])
    assert type(zero_share) == dict
    assert len(zero_share) == 1
    assert zero_share == {'B': 9997.222}

def test_negative_share_calculate_reward():
    negative_share = calculate_reward([('A', 0, -1), ('B', 1, 1)])
    assert type(negative_share) == dict
    assert len(negative_share) == 1
    assert negative_share == {'B': 9997.222}

def test_ten_user_share_calculate_reward():
    ten_user_share = calculate_reward([('A', 0, 1), ('B', 0, 1), ('C', 0, 1), ('D', 0, 1), ('E', 0, 1), ('F', 0, 1), ('G', 0, 1), ('H', 0, 1), ('I', 0, 1), ('J', 0, 1)])
    assert type(ten_user_share) == dict
    assert len(ten_user_share) == 10
    assert ten_user_share == {'A': 1000.0, 'B': 1000.0, 'C': 1000.0, 'D': 1000.0, 'E': 1000.0, 'F': 1000.0, 'G': 1000.0, 'H': 1000.0, 'I': 1000.0, 'J': 1000.0}