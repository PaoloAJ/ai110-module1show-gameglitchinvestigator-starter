# Game Glitch Investigator: The Impossible Guesser

## The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`

## Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: _"How do I keep a variable from resetting in Streamlit when I click a button?"_
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## Document Your Experience

- [x] Describe the game's purpose: A number guessing game where players guess a secret number within a limited number of attempts, with hints indicating whether to guess higher or lower.
- [x] Detail which bugs you found:
  1. Hints were reversed ("Go HIGHER" when guess was too high)
  2. Secret converted to string on even attempts, breaking comparisons
  3. Hard difficulty range (1-50) was easier than Normal (1-100)
  4. Score had off-by-one error and inconsistent "Too High" penalty
  5. New Game didn't reset history or use correct difficulty range
  6. Info bar hardcoded "1 and 100" instead of using actual range
- [x] Explain what fixes you applied:
  1. Swapped hint messages in `check_guess` so "Too High" says "Go LOWER" and vice versa
  2. Removed string conversion of secret on even attempts in app.py
  3. Changed Hard range to (1, 200) to be genuinely harder
  4. Fixed score formula to use `attempt_number` (not `attempt_number + 1`) and made penalties consistent
  5. New Game now resets history, score, status, and uses difficulty-appropriate range
  6. Info bar now displays the actual range from `get_range_for_difficulty`

## Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
