# Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  When I first ran the game, it appeared to work on the surface but was full of subtle bugs. The guess input box showed up, but the hints were completely backwards, it told me to "Go HIGHER" when my guess was already too high, which made the game impossible to win by following the hints. The score would also behave erratically, sometimes going up on wrong guesses.

- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").
  - The hints were reversed: when I guessed too high, it said "Go HIGHER!" instead of "Go LOWER!", and vice versa.
  - On even-numbered attempts, the secret number was silently converted to a string, causing the integer comparison to fail and producing wrong hint directions.
  - The "New Game" button did not reset the guess history, so old guesses carried over into new rounds.
  - The info bar always said "Guess a number between 1 and 100" regardless of the selected difficulty.
  - The Hard difficulty range was (1, 50), which is actually easier than Normal (1, 100).
  - The score calculation had an off-by-one error, subtracting an extra 10 points on a win.
  - The "Too High" penalty alternated between +5 and -5 depending on whether the attempt number was even or odd.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  I used Claude Code (Claude Opus) as my primary AI assistant for this project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  Claude correctly identified that the check_guess function had its hint messages swapped, "Go HIGHER" was paired with the guess > secret branch when it should have been "Go LOWER." I verified this by running the game with the debug panel open: guessing 60 when the secret was 50 now correctly shows "Go LOWER!", and guessing 40 correctly shows "Go HIGHER!". The pytest test test_hint_message_too_high also confirms this fix.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  Claude initially kept the TypeError exception handler in check_guess that compared string versions of the guess and secret as a fallback. This was actually part of the bug, the original code intentionally converted the secret to a string on even attempts, so keeping the TypeError handler would have masked the real issue. I rejected this approach and removed both the string conversion in app.py and the TypeError fallback in check_guess, ensuring all comparisons are integer-to-integer. I verified by playing multiple rounds and confirming hints were correct on every attempt, not just odd ones.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I used a combination of automated testing with pytest and manual testing in the Streamlit app. For each bug, I wrote or updated a specific test case that would fail with the buggy code and pass with the fix. Then I ran the full game to confirm the fix worked in the actual UI.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  I ran pytest tests/test_game_logic.py -v which executed 16 test cases. The test_hint_message_too_high test verifies that when a guess of 60 is compared to a secret of 50, the message contains "LOWER", this directly validates the reversed-hints bug fix. The test_score_on_win_first_attempt test confirms the score is 90 (100 - 10\*1) on a first-attempt win, verifying the off-by-one fix. All 16 tests passed.

- Did AI help you design or understand any tests? How?
  Yes, Claude helped generate the full test suite covering check_guess, parse_guess, update_score, and get_range_for_difficulty. It suggested edge case tests like parsing negative numbers and decimals, and a test that Hard mode's range is wider than Normal's range. I reviewed each test to make sure it was testing the right behavior and not just passing trivially.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  In Streamlit, the entire script reruns from top to bottom every time the user interacts with a widget (like clicking a button or typing). Without st.session_state, any variable defined at the top of the script would be re-initialized on every rerun. The secret number was protected by if "secret" not in st.session_state, but the original code had a bug where on even attempts it converted the secret to a string (secret = str(st.session_state.secret)), which didn't change the stored value but broke the comparison logic, making it seem like the game was behaving inconsistently.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Imagine every time you click a button on a webpage, the entire page rebuilds itself from scratch, that's how Streamlit works. Without session state, it would be like having amnesia after every click: all your variables reset. st.session_state is like a notebook that survives between reruns, you write values into it and they persist, so the game can remember the secret number, your score, and your guess history across interactions.

- What change did you make that finally gave the game a stable secret number?
  The secret number was already stored in st.session_state so it persisted correctly. The real fix was removing the code that converted st.session_state.secret to a string on even-numbered attempts (secret = str(st.session_state.secret)). Now the game always compares the guess directly against the integer secret, so the hints are consistent every time.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

  - Writing targeted pytest cases for each bug before and after fixing it. Having automated tests gave me confidence that my fixes actually worked and didn't break anything else. I want to make test-driven debugging a regular habit.

- What is one thing you would do differently next time you work with AI on a coding task?
  I would be more careful about reviewing AI suggestions that involve exception handlers or fallback logic. The TypeError handler in the original code looked like defensive programming but was actually masking a deeper bug. Next time, I'll ask "why would this exception ever happen?" before accepting error-handling code.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  AI-generated code can look correct on the surface but hide subtle logic errors that only show up during gameplay or testing. This project taught me that AI code needs the same careful review and testing as any other code, you can't just trust it because it runs without syntax errors.
