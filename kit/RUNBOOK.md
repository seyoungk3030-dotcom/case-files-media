# 퇴근 후 사건파일: one scheduled run = one new room

Each run makes **one** new original puzzle and posts it to Instagram @case_files_after_work as a 7-card carousel plus a narrated reel. The reel goes to the Reels tab only (`share_to_feed=false`). There are three runs a day, starting around 11:30, 17:30 and 20:30 KST, until 2026-12-31.

Everything lives in this repo (public). `kit/` holds the tools, `kit/ledger.json` is the source of truth, and `rooms/room-NNN/` is each episode. The repo is public so Instagram can fetch the media, so **never commit secrets**. The token is env `IG_ACCESS_TOKEN` and must never be printed or written anywhere.

Setup: `python3 -m pip install -q edge-tts numpy pillow` (ffmpeg is preinstalled). Run python with `-I`, from outside the episode folder.

## 0. Guard
- If today (KST) is after 2026-12-31, do nothing and stop.
- Read `kit/ledger.json`. If a room has status READY or FAILED, finish it first: re-run publish, which skips anything already posted. Then stop.
- Run `python3 -I -c "import sys; sys.path.insert(0,'kit'); import publish; [print(m['timestamp'], (m.get('caption') or '')[:30]) for m in publish.recent(6)]"`. If a `[ROOM` post exists from the last 90 minutes, this slot is already covered, so stop. (Slots are 3+ hours apart; a manual post earlier in the day does not count as this slot.)
- The next room is the highest `room` in the ledger + 1, and the date is today in KST (`YYYY.MM.DD`).

## 1. Design the puzzle
- Use a mechanic that isn't among the last 10 ledger entries, and never repeat a puzzle. Rotate through logic grids (skyscraper, kakuro-lite, nonogram-lite, star battle), deductions with 민재/유나/도윤 (alibis, timestamps, liars), ciphers (shift, keypad, clock), spatial puzzles (folding, rotation, paths, mirrors), weighing, toggles, sequences and calendars.
- The answer is a 4-digit code the reader can solve from the cards alone in a few minutes. Medium difficulty is the target. A "trap" (a tempting wrong answer) works well.
- Write `rooms/room-NNN/source/verify.py` that brute-forces every candidate and proves the answer is **unique**. Save the result to `notes/proof.json`. If the answer isn't unique, redesign. Never post a puzzle that hasn't been proven.

## 2. Cards (`cards/card-01..07.png`, 1080x1350)
Write `source/render.py` using `kit/style.py` (`base(room, date, n, 7, title, sub)`, `lines`, `ctext`, `cell`, `big_answer`, colors). Card structure:
1. Hook: title, mint subtitle, the full puzzle visual, 2–3 story lines, `CTA_START.format(a='6~7')`
2. Rules, with a small worked example, `CTA_SOLVE`
3. How to read the code (★ marker or A→B→C→D), `CTA_SOLVE`
4. Every rule and every clue on one card, `CTA_SOLVE`
5. Hint or trap (coral accent), `CTA_HINT`
6. `정답 공개 · NNNN` with 3–4 short reasoning lines
7. Solved visual, `big_answer(d, y, code)`, `맞혔다면 좋아요 · 다음 방은 팔로우!`

Rules for the text: Korean, lines under about 900px wide, nothing overlapping or clipped, and no emoji in images. **Open every card PNG with the Read tool and look at it**, then fix problems and re-render. Quality matters more than speed: the user checks these.

## 3. Reel
- Write `episode.json` (see the `kit/reel.py` docstring). Use 7 scenes, `card` 1–7, `solve_after` 4 and `solve_seconds` 20. Narration should be about 1–2 sentences per scene, with numbers written as Korean words (일, 이, 삼, 사; 이십 초). Subtitles may use digits and must fit in 4 lines.
- Run `python3 -I kit/reel.py rooms/room-NNN`, then Read `.build/qa-*.png`. Aim for a reel of 70–100 seconds.

## 4. Captions
`notes/caption-carousel.txt` and `notes/caption-reel.txt`. Copy the format of `rooms/room-011/notes/` exactly: the first line is `[ROOM NNN · 제목] YYYY.MM.DD <one emoji>`. The reel caption keeps the line about synthetic narration and the BGM we made. Hashtags: `#퇴근후사건파일 #방탈출 #추리게임 #팔로우 #좋아요`.

## 5. Host, publish, record
1. Add the room to `kit/ledger.json` (room, title, mechanic, answer, date) with status READY.
2. Delete `.build/`, then `git add -A`, commit `ROOM NNN`, and `git push origin main`. Take `SHA=$(git rev-parse HEAD)`.
3. Set `BASE=https://cdn.jsdelivr.net/gh/seyoungk3030-dotcom/case-files-media@$SHA/rooms/room-NNN`. Confirm that `curl -sI $BASE/reel.mp4` returns 200 `video/mp4`.
4. Run `python3 -I kit/publish.py rooms/room-NNN $BASE`. It skips anything already posted, handles the false "action is blocked" error, and retries transient video-fetch failures.
5. If it fails, set the ledger status to FAILED with a short reason, commit and push, and stop. Never retry without checking the account first. **Never post the same room twice.**
6. On success the ledger shows PUBLISHED with URLs. Commit and push the ledger.

Finish with a one-line summary: room, title, answer, and both URLs.
