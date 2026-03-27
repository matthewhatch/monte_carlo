# Architecture

## Overview

The simulator models a single player batting in every plate appearance across a full 9-inning game. There is no opposing pitcher — each outcome is drawn purely from the batter's historical statistical rates.

This approach, inspired by *Mathletics* by Wayne Winston, answers the question: *"If a lineup consisted entirely of clones of player X, how many runs would they score per game?"* This expected runs-per-game value is the **Runs Created** estimate.

---

## Simulation Pipeline

```
main()
  └─ simulate_game(player)          ← 9 iterations
       └─ simulate_inning(player)   ← until 3 outs
            └─ player.simulate_ab(state)  ← one plate appearance
                 └─ events.*()     ← update state + count runs
```

### 1. Player Probability Model (`Player.__init__`)

On construction, each raw count is divided by `plate_appearances` to produce a probability:

| Attribute | Probability |
|-----------|-------------|
| `errors` | `p_error` |
| `outs` | `p_out` |
| `strike_outs` | `p_strike_out` |
| `walks` | `p_walk` |
| `hbp` | `p_hbp` |
| `singles` | `p_single` |
| `doubles` | `p_double` |
| `triples` | `p_triple` |
| `home_runs` | `p_home_run` |

Probabilities are renormalized before each at-bat to sum to exactly 1.0 (guards against floating-point drift).

### 2. At-Bat Simulation (`Player.simulate_ab`)

Each call draws one outcome from `numpy.random.choice` using the 9 outcome probabilities. The outcome is then dispatched to the appropriate event function in `events.py`.

### 3. Game State

The game state is represented as a 4-element list:

```python
state = [outs, runner_on_1st, runner_on_2nd, runner_on_3rd]
# Each runner position is 0 (empty) or 1 (occupied)
# outs counts from 0 to 2; the inning ends when outs reaches 3
```

Every event function receives the current state and returns `(new_state, runs_scored)`.

---

## Event Hierarchy

### Primary outcomes

| Outcome constant | Event function | Notes |
|------------------|---------------|-------|
| `HOME_RUN` | `home_run()` | All runners score |
| `TRIPLE` | `triple()` | All runners score |
| `DOUBLE` | `double()` | Dispatches to `short_double` or `long_double` |
| `SINGLE` | `single()` | Dispatches to `short_single`, `medium_single`, or `long_single` |
| `BB` / `HBP` | `free_pass()` | Force-advances runners |
| `ERROR` | `error()` | Batter reaches; runner on 3rd scores |
| `K` | `strike_out()` | Adds one out; runners stay |
| `OUT` | `out_in_play()` | Dispatches to ground ball or fly ball |

### Secondary dispatch for singles

| Type | Probability | Runner advancement |
|------|-------------|-------------------|
| `SHORT_SINGLE` | 20% | Runners advance 1 base; runner on 3rd scores |
| `MEDIUM_SINGLE` | 50% | Runners on 2nd and 3rd score; runner on 1st goes to 2nd |
| `LONG_SINGLE` | 30% | Runners on 2nd and 3rd score; runner on 1st goes to 3rd |

### Secondary dispatch for doubles

| Type | Probability | Runner advancement |
|------|-------------|-------------------|
| `SHORT_DOUBLE` | 80% | Runners on 2nd and 3rd score; runner on 1st to 3rd |
| `LONG_DOUBLE` | 20% | All runners score |

### Secondary dispatch for outs in play

| Type | Probability | Notes |
|------|-------------|-------|
| `GROUND_OUT` | 53.8% | May become `GIDP` (double play); runner advances |
| `LINE_OUT` | 15.3% | Adds one out; all runners stay |
| `FLY_OUT` | 30.9% | May produce sacrifice fly (runner on 3rd scores with < 2 outs) |

### Fly ball sub-types

| Type | Probability | Notes |
|------|-------------|-------|
| `SHORT_FLY` | 30% | No runner advancement |
| `MEDIUM_FLY` | 50% | Runner on 3rd scores if < 2 outs (sac fly) |
| `LONG_FLY` | 20% | Runner on 3rd scores if < 2 outs; other runners advance |

---

## Data Flow

```
baseball-reference.com  ──scrape──▶  data/players_{year}.csv
constants/players.py    ──direct──▶  Player(**stats)
data/players_{year}.csv ──read──▶   Player(**stats)
                                          │
                                    simulate_game()
                                          │
                                    runs_created value
```

Player stats are looked up from a local CSV cache first. If not cached and not in a CI environment, the scraper fetches from baseball-reference.com and writes results back to the CSV for future use.
