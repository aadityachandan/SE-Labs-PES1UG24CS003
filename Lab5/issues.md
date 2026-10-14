# Issues Found and Fixed

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| pickle.load on a file (B301, Medium) | Security | 49 | Loading pickle data can execute arbitrary code | Replaced pickle with json |
| import pickle (B403, Low) | Security | 2 | Pickle module has security implications | Removed the import |
| try/except/pass (B110, W0702, E722) | Bug | 24-25 | Bare except hides every error silently | Catch specific errors and raise a clear message |
| Mutable default argument (W0102) | Bug | 11 | order_history=[] is shared across calls | Made order_history an instance attribute |
| Global statements (W0603) | Quality | 12, 28, 48 | Global state makes the code hard to test | Moved the state into an OrderQueue class |
| Broad exception (W0718) | Quality | 32 | except Exception catches everything | Catch (OSError, json.JSONDecodeError) |
| open() without with or encoding (R1732, W1514) | Quality | 30, 43, 49 | File handles may not be closed, no encoding set | Use with open(..., encoding="utf-8") |
| Unknown dish costs 99 | Logic bug (no tool flagged it) | 15 | Missing menu items silently cost 99 | Raise ValueError for unknown dishes |
| Invalid status accepted | Logic bug (no tool flagged it) | 23 | "teleported" was accepted as a status | Validate against VALID_STATUSES |
| Empty order accepted | Logic bug (no tool flagged it) | 60 | Order with no customer or items was created and delivered | Raise ValueError when customer or items are missing |
| Missing docstrings, bad names (C0114, C0116, C0103) | Style | 1, 7, 11, 21, 51 | printQueue, next_id, no docstrings | Renamed to snake_case, added docstrings |
| Old-style string formatting (C0209) | Style | 52 | % formatting instead of an f-string | Use an f-string |
| Missing blank lines (E302, E305) | Style | 11, 21, 27, 35, 42, 47, 51, 56, 70 | PEP 8 needs two blank lines | Added the blank lines |
| Lines too long (E501) | Style | 16, 54 | Lines over 79 characters | Wrapped the lines |