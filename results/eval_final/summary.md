# Held-out evaluation

Checkpoint: `models\ppo_main\checkpoint_0120.pt`

Values are mean ± standard deviation over seeds. Lower is better, except completed trips. Waiting and time loss cover completed trips; unfinished vehicles are counted separately.

| Scenario | Controller | Mean wait (s) | 95th pct wait (s) | Mean time loss (s) | Completed trips | Unfinished | Safety overrides | Illegal transitions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| test_balanced | fixed-time | 6.3 ± 0.5 | 18.0 ± 0.6 | 16.8 ± 1.3 | 623.3 ± 8.6 | 38.7 ± 3.8 | 0.0 ± 0.0 | 0.0 ± 0.0 |
| test_balanced | actuated | 4.8 ± 0.8 | 21.0 ± 4.6 | 13.0 ± 1.1 | 625.3 ± 11.5 | 36.7 ± 0.6 | 0.3 ± 0.6 | 0.0 ± 0.0 |
| test_balanced | ppo | 8.8 ± 0.8 | 32.8 ± 2.8 | 18.3 ± 1.6 | 621.7 ± 13.6 | 40.3 ± 3.5 | 84.7 ± 8.1 | 0.0 ± 0.0 |
| test_ew_heavy | fixed-time | 14.1 ± 3.6 | 40.9 ± 7.1 | 35.9 ± 7.9 | 501.7 ± 4.0 | 73.7 ± 20.4 | 0.0 ± 0.0 | 0.0 ± 0.0 |
| test_ew_heavy | actuated | 7.5 ± 0.2 | 27.8 ± 2.3 | 20.5 ± 0.5 | 529.0 ± 9.2 | 46.3 ± 9.5 | 2.0 ± 1.0 | 0.0 ± 0.0 |
| test_ew_heavy | ppo | 12.6 ± 0.5 | 32.6 ± 2.1 | 27.7 ± 1.3 | 526.7 ± 8.1 | 48.7 ± 9.0 | 60.3 ± 4.2 | 0.0 ± 0.0 |
| test_shift | fixed-time | 9.0 ± 1.7 | 30.3 ± 7.4 | 23.3 ± 3.5 | 599.3 ± 32.1 | 39.7 ± 5.8 | 0.0 ± 0.0 | 0.0 ± 0.0 |
| test_shift | actuated | 5.4 ± 1.1 | 22.0 ± 4.0 | 14.6 ± 1.5 | 600.0 ± 34.0 | 39.0 ± 4.6 | 1.0 ± 0.0 | 0.0 ± 0.0 |
| test_shift | ppo | 9.2 ± 0.7 | 34.3 ± 2.1 | 19.9 ± 1.2 | 595.7 ± 29.7 | 43.3 ± 8.1 | 62.0 ± 3.6 | 0.0 ± 0.0 |

## PPO compared with baselines

Percent change of the mean; positive means PPO is better, negative means worse.

| Scenario | vs fixed-time: mean wait | vs fixed-time: time loss | vs actuated: mean wait | vs actuated: time loss |
| --- | --- | --- | --- | --- |
| test_balanced | -40.2% | -8.9% | -84.1% | -41.4% |
| test_ew_heavy | +10.3% | +22.8% | -69.0% | -35.5% |
| test_shift | -2.6% | +14.7% | -72.3% | -35.7% |
