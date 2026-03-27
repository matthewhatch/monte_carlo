# API Reference — `monte_carlo.events`

Module: `src/monte_carlo/events.py`

All baseball event functions. Each function takes the current game state and returns a `(new_state, runs_scored)` tuple.

**Game state format:** `[outs, runner_1st, runner_2nd, runner_3rd]`
- Each runner position is `0` (empty) or `1` (occupied)
- `outs` ranges from 0 to 3 (inning ends at 3)

---

## Hit Events

### `single(current_state)`

Randomly selects a single sub-type and dispatches to the appropriate handler.

| Sub-type | Probability |
|----------|------------|
| `SHORT_SINGLE` | 20% |
| `MEDIUM_SINGLE` | 50% |
| `LONG_SINGLE` | 30% |

**Returns:** `(new_state, runs_scored)`

---

### `short_single(current_state)`

Runner on 3rd scores. Runners on 1st and 2nd each advance one base.

**Returns:** `(new_state, runs_scored)`

---

### `medium_single(current_state)`

Runners on 2nd and 3rd score. Runner on 1st advances to 2nd. Batter on 1st.

**Returns:** `(new_state, runs_scored)`

---

### `long_single(current_state)`

Runners on 2nd and 3rd score. Runner on 1st advances to 3rd. Batter on 1st.

**Returns:** `(new_state, runs_scored)`

---

### `double(current_state)`

Randomly selects a double sub-type and dispatches to the appropriate handler.

| Sub-type | Probability |
|----------|------------|
| `SHORT_DOUBLE` | 80% |
| `LONG_DOUBLE` | 20% |

**Returns:** `(new_state, runs_scored)`

---

### `short_double(current_state)`

Batter on 2nd. Runner on 1st advances to 3rd. Runners on 2nd and 3rd score.

**Returns:** `(new_state, runs_scored)`

---

### `long_double(current_state)`

Batter on 2nd. All baserunners score.

**Returns:** `(new_state, runs_scored)`

---

### `triple(current_state)`

Batter on 3rd. All baserunners score.

**Returns:** `(new_state, runs_scored)`

---

### `home_run(current_state)`

Batter and all baserunners score. Bases cleared.

**Returns:** `(new_state, runs_scored)`

---

## Non-Hit Events

### `free_pass(current_state)`

Handles walks (`BB`) and hit-by-pitch (`HBP`). Batter takes 1st base. Force-advances runners only when forced.

**Force advance logic:**
- Runner on 1st only → advances to 2nd
- Runners on 1st and 2nd → runner on 2nd advances to 3rd
- Bases loaded → runner on 3rd scores (1 run)

**Returns:** `(new_state, runs_scored)`

---

### `error(current_state)`

Batter reaches 1st. All current runners advance one base. Runner on 3rd scores.

**Returns:** `(new_state, runs_scored)`

---

### `strike_out(current_state)`

Adds one out. No runner movement.

**Returns:** `([outs+1, ...], 0)`

---

## Out Events

### `out_in_play(current_state)`

Dispatches to ground ball or fly ball based on real MLB rates.

| Sub-type | Probability |
|----------|------------|
| `GROUND_OUT` | 53.8% |
| `LINE_OUT` | 15.3% |
| `FLY_OUT` | 30.9% |

Line outs add one out with no runner movement.

**Returns:** `(new_state, runs_scored)`

---

### `ground_ball(current_state)`

Dispatches to single ground out or double play (50/50).

**Returns:** `(new_state, runs_scored)`

---

### `ground_out(current_state)`

Adds one out. Runner advancement depends on base configuration:

| Runners | Result |
|---------|--------|
| Bases empty | Out only |
| Runner on 1st | Runner out at 2nd; batter safe at 1st |
| Runners on 1st & 2nd | Lead runner out at 3rd; batter and trail runner safe |
| Bases loaded | Runner out at home; batter and others safe |
| Runner on 3rd only | Runner scores; bases cleared |
| Runner on 2nd only | Runner advances to 3rd |

**Returns:** `(new_state, runs_scored)`

---

### `gidp(current_state)`

Ground-into-double-play. Two outs recorded. If no lead runner or 0 outs, falls back to `ground_out`.

**Returns:** `(new_state, runs_scored)`

---

### `fly_ball(current_state)`

Dispatches to short, medium, or long fly ball.

| Sub-type | Probability |
|----------|------------|
| `SHORT_FLY` | 30% |
| `MEDIUM_FLY` | 50% |
| `LONG_FLY` | 20% |

**Returns:** `(new_state, runs_scored)`

---

### `short_fly(current_state)`

Adds one out. No runner advancement.

**Returns:** `([outs+1, same runners], 0)`

---

### `medium_fly(current_state)`

Adds one out. Runner on 3rd scores if fewer than 2 outs (sacrifice fly).

**Returns:** `(new_state, runs_scored)`

---

### `long_fly(current_state)`

Adds one out. Runner on 3rd scores if fewer than 2 outs (sac fly). Remaining runners advance one base.

**Returns:** `(new_state, runs_scored)`
