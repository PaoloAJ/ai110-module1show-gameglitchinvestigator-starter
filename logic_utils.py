def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Hard mode should have a wider range (1-200) to be harder than Normal (1-100)
    # Original bug: Hard was (1, 50) which is easier than Normal (1, 100)
    # FIX: Refactored from app.py using Claude Code agent mode
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: Refactored from app.py using Claude Code agent mode
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def validate_in_range(guess: int, low: int, high: int):
    """Check if guess is within the valid range. Returns (ok, error_message)."""
    if guess < low or guess > high:
        return False, f"Please guess a number between {low} and {high}."
    return True, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: Reversed hints — original said "Go HIGHER" when guess was too high
    # FIX: Removed TypeError fallback that compared int to string
    # FIX: Refactored from app.py using Claude Code agent mode
    if guess == secret:
        return "Win", "Correct!"

    if guess > secret:
        return "Too High", "Go LOWER!"
    else:
        return "Too Low", "Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: Removed off-by-one error (was attempt_number + 1)
    # FIX: Removed inconsistent scoring for "Too High" that alternated +5/-5
    # FIX: Refactored from app.py using Claude Code agent mode
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
