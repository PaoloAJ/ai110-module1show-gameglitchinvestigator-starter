from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty, validate_in_range


# --- check_guess tests ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_hint_message_too_high():
    # When guess is too high, message should say "Go LOWER"
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message


def test_hint_message_too_low():
    # When guess is too low, message should say "Go HIGHER"
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message


# --- parse_guess tests ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None


def test_parse_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert "not a number" in err


def test_parse_decimal():
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3


def test_parse_negative_number():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5


# --- update_score tests ---

def test_score_on_win_first_attempt():
    score = update_score(0, "Win", 1)
    assert score == 90  # 100 - 10*1 = 90


def test_score_on_win_late_attempt():
    score = update_score(0, "Win", 10)
    assert score == 10  # minimum 10 points


def test_score_on_too_high():
    score = update_score(100, "Too High", 1)
    assert score == 95  # -5 penalty


def test_score_on_too_low():
    score = update_score(100, "Too Low", 1)
    assert score == 95  # -5 penalty


# --- get_range_for_difficulty tests ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_hard_range_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


# --- validate_in_range tests ---

def test_guess_in_range():
    ok, err = validate_in_range(10, 1, 20)
    assert ok is True
    assert err is None


def test_guess_out_of_range_high():
    ok, err = validate_in_range(500, 1, 100)
    assert ok is False
    assert "between" in err


def test_guess_out_of_range_low():
    ok, err = validate_in_range(-5, 1, 100)
    assert ok is False
    assert "between" in err


def test_guess_at_boundary():
    ok, _ = validate_in_range(1, 1, 100)
    assert ok is True
    ok, _ = validate_in_range(100, 1, 100)
    assert ok is True
