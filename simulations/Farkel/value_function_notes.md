# Farkel: Turn EV via Value Function (Dominance-Preserving Pruning)

This note documents the value-function / EV approach used in `farkel_analysis.ipynb`.

## Core modeling choice

The move-pruning heuristic is assumed to be **dominance-preserving**: for any omitted scoring selection, there exists a retained selection that dominates it under the continuation value used by the dynamic program.

- For a roll `counts`, the selectable scoring actions are `scoring_moves(counts)`.
- Under the dominance-preserving assumption, maximizing over `scoring_moves(counts)` is equivalent to maximizing over the full set of legal scoring selections.

## State

A decision point in the turn is represented by:

- `d`: dice in hand (1..6)
- `s`: accumulated turn points (discretized on a `ScoreGrid`, default 50-point steps)

Interpretation: state `(d, s)` means `s` points are currently at risk within the turn and `d` dice would be rolled on continuation.

## Banking policy (threshold vector)

A `ThresholdPolicy` is a non-decreasing vector `T[1..6]` (multiples of `SCORE_STEP`).

At any decision point:

- If `s >= T[d]`, **bank immediately** and end the turn with score `s`.
- Otherwise, roll `d` dice.

This matches the real decision point after each scoring selection, once the number of dice remaining (including hot dice reset) is known.

## Transition dynamics

From state `(d, s)` where `s < T[d]`:

1. Roll `d` dice. The roll distribution is exact: `roll_distribution(d)` enumerates all `DiceCounts` outcomes with multinomial probabilities.
2. If `scoring_moves(counts)` is empty: **bust**, final score is `0`.
3. Otherwise choose `move` in `scoring_moves(counts)` to maximize continuation value:
   - `s' = clamp(s + move.points)` (grid-clamped)
   - `d' = next_dice_in_hand(d, move.used)` (hot dice handled)
   - continuation value is `W(d', s')` (which will bank immediately if `s' >= T[d']`).

## Why a single backward sweep works

Every scoring move has strictly positive points, so `s' > s` (in grid units). That means `W(d, s)` only depends on values at higher scores, enabling an exact DP computed by sweeping `s` from high to low (no value iteration needed).

## Notebook entry points

Implemented in the notebook:

- `compute_policy_value_table(policy)` → returns a table `W[d][idx]`.
- `expected_turn_score(policy)` → expected score from start-of-turn state `(d=6, s=0)`.
- `sample_random_policy(...)` and `random_search_policies(n, ...)` → simple search scaffolding over monotone threshold vectors.

A potential next step is a local refinement step (coordinate descent / neighbor exploration) around the best random sample.
