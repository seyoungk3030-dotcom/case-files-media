# 퇴근 후 사건파일: one scheduled run = one new room

Each run makes **one** new original puzzle and posts it to Instagram @case_files_after_work as a 7-card carousel plus a short narrated reel, both in the 3D style. The reel goes to the Reels tab only (`share_to_feed=false`). There are three runs a day, starting around 11:30, 17:30 and 20:30 KST, until 2026-12-31.

Everything lives in this repo (public). `kit/` holds the tools, `kit/ledger.json` is the source of truth, and `rooms/room-NNN/` is each episode. The repo is public so Instagram can fetch the media, so **never commit secrets**. The token is env `IG_ACCESS_TOKEN` and must never be printed or written anywhere.

Setup: `python3 -m pip install -q edge-tts numpy pillow bpy` (ffmpeg is preinstalled; `bpy` is Blender, used for the 3D renders). Run python with `-I`, from outside the episode folder.

**Format since ROOM 029 (user's choice, 2026-10-21): everything is in the 3D style.** 3D props are rendered with Blender (`kit/b3d.py`), cards use `kit/style3d.py`, and the reel is a ~30–40 s animated fast-hook reel made by `kit/short3d.py`. ROOM 029 is the reference episode for every file below; copy its structure. The old flat style (`kit/style.py` cards, `kit/reel.py` 90 s reel) is retired.

## 0. Guard
- If today (KST) is after 2026-12-31, do nothing and stop.
- Read `kit/ledger.json`. If a room has status READY or FAILED, finish it first: re-run publish, which skips anything already posted. Then stop.
- Run `python3 -I -c "import sys; sys.path.insert(0,'kit'); import publish; [print(m['timestamp'], (m.get('caption') or '')[:30]) for m in publish.recent(6)]"`. If a `[ROOM` post exists from the last 90 minutes, this slot is already covered, so stop. (Slots are 3+ hours apart; a manual post earlier in the day does not count as this slot.)
- The next room is the highest `room` in the ledger + 1, and the date is today in KST (`YYYY.MM.DD`).

## 1. Design the puzzle
- Use a mechanic that isn't among the last 10 ledger entries, and never repeat a puzzle.
- **Pick puzzles a viewer understands from one picture in 2 seconds**: physical, visual things that look good in 3D (cube stacks, scales and mobiles, dice, gears, matchsticks, coins, pipes, mirrors and light beams, folding boxes, block towers, sliding tiles, cups and balls). Avoid rule-heavy logic grids and long text deductions; they performed worst. Easy-to-medium beats hard: the reel gives 10 seconds.
- The answer is a 4-digit code. A tempting wrong answer (a trap) works well.
- Write `rooms/room-NNN/source/verify.py` that brute-forces every candidate and proves the answer is **unique**, and that every rule is needed. Save the result to `notes/proof.json`. If the answer isn't unique, redesign. Never post a puzzle that hasn't been proven. If the picture itself carries information (what is visible from the camera), model that view in code the way ROOM 029's `source/view.py` does.

## 2. 3D renders (`source/scene3d.py` → `.build-3d/*.png`)
- Build the scene with `kit/b3d.py` (`reset`, `mats`, `lights`, `camera`/`stack_camera`, `floor`, props such as `sphere`, `cube`, `pyramid`, `star`, `seesaw`, `cubestack`; write new props there when a puzzle needs them). Render each object group as its own transparent PNG so cards and the reel can lay them out. Also render the "answer" variant (x-ray, labels, highlighted parts) and any example used on the rules card. Cycles CPU takes about 5–20 s per sprite.
- Use the palette in `b3d.PAL`; keep the toy-like glossy look. Open the renders with Read and check that the puzzle reads correctly (nothing cut off, nothing ambiguous).

## 3. Cards (`source/render.py` → `cards/card-01..07.png`, 1080x1350)
Use `kit/style3d.py`: `card(room, date, n, 7, title, sub)`, `sprite`, `put`, `panel`, `text_lines`, `text_layer`, `pill`, `badge`, `cta`. Structure:
1. Hook: title (the question), mint subtitle (the twist), the full puzzle in 3D, `cta(fr, '도전 → 4장까지  ·  정답 → 6~7장')`
2. Rules in a glass panel, with a small 3D example, `cta(fr, '4장까지 풀고 댓글에 암호를 남겨주세요')`
3. How to read the code (A→B→C→D), same cta
4. Every rule and the whole puzzle on one card, same cta
5. Hint or trap (`subcol=CORAL`, `cta(..., CORAL)` with `다음 장부터 정답 · 먼저 멈춰서 풀어보세요`)
6. `정답 공개 · NNNN` with the answer renders and 1–2 reasoning lines
7. Answer renders, the big code (`text_layer(' '.join(code), 160, MINT, glow=MINT)`), `맞혔다면 좋아요 · 다음 방은 팔로우!`

Korean text, lines under about 900 px, nothing overlapping or clipped, no emoji in images. **Open every card PNG with Read and look at it**, then fix and re-render. Quality matters more than speed.

## 3b. Reel (`short3d.json` → `reel.mp4`)
- Write `rooms/room-NNN/short3d.json` (see the `kit/short3d.py` docstring and ROOM 029): room, two hook lines (the question on screen from frame one), two rule lines, the puzzle `layout` (or `stack`), legend, values, answer, `count` 10, cta, and four narrations (hook, rule, answer, cta) with numbers as Korean words. The answer narration names the legend items in order.
- Run `python3 -I kit/short3d.py /abs/path/rooms/room-NNN`, then Read `.build-short/qa-hook.png`, `qa-count.png`, `qa-answer.png`, `qa-cta.png`. Aim for 30–40 seconds.

## 4. Captions
`notes/caption-carousel.txt` and `notes/caption-reel.txt`. Copy the format of `rooms/room-011/notes/` exactly: the first line is `[ROOM NNN · 제목] YYYY.MM.DD <one emoji>`. The reel caption keeps the line about synthetic narration and the BGM we made, and says the answer is at the end of the video (10-second countdown). ROOM 029's captions show the current wording. Hashtags (since ROOM 029): `#퇴근후사건파일 #두뇌게임 #퍼즐 #퀴즈 #방탈출 #추리게임 #수수께끼 #IQ테스트` (niche puzzle tags reach people who look for puzzles; generic #팔로우 #좋아요 were dropped).

## 5. Host, publish, record
1. Add the room to `kit/ledger.json` (room, title, mechanic, answer, date) with status READY.
2. Delete `.build/`, `.build-3d/`, `.build-short/` and any `short.mp4` (git ignores them anyway), then `git add -A`, commit `ROOM NNN`, and `git push origin main`. Take `SHA=$(git rev-parse HEAD)`.
3. Set `BASE=https://raw.githubusercontent.com/seyoungk3030-dotcom/case-files-media/$SHA/rooms/room-NNN` and use it for both video and images. Instagram accepted the raw reel URL on ROOM 013 while jsDelivr's GitHub endpoint was returning 503. Only if raw fails, try `https://cdn.jsdelivr.net/gh/seyoungk3030-dotcom/case-files-media@$SHA/rooms/room-NNN` for the video.
4. Run `python3 -I kit/publish.py rooms/room-NNN $BASE $BASE`. It waits until the files are reachable, skips anything already posted, retries "not ready yet" on the same container, handles the false "action is blocked" error, and retries transient video-fetch failures.
5. If it fails, set the ledger status to FAILED with a short reason, commit and push, and stop. Never retry without checking the account first. **Never post the same room twice.**
6. On success the ledger shows PUBLISHED with URLs. Commit and push the ledger.

Finish with a one-line summary: room, title, answer, and both URLs.
