# Project Structure

This document defines file organization for the traffic signal AI project.

Architecture, algorithms, data contracts, and evaluation requirements are
defined in [TRAFFIC_AI_DESIGN.md](TRAFFIC_AI_DESIGN.md).

The development environment is native Windows with a project-local Python
virtual environment.

## Root Files

| Path | Purpose |
| --- | --- |
| README.md | Overview, installation, and verified execution commands |
| requirements.txt | Direct Python dependencies |
| requirements-lock.txt | Exact installed dependency versions |
| .gitignore | Exclude local environments, caches, and large artifacts |
| .venv/ | Local Windows Python environment; excluded from Git |

## Configuration

| Path | Purpose |
| --- | --- |
| configs/network.json | Network generation settings |
| configs/intersections.json | Lane, approach, movement, phase, and neighbor mappings |
| configs/scenarios.json | Demand schedules and scenario seeds |
| configs/controller.json | Signal safety timings and controller settings |
| configs/training.json | PPO settings, training seeds, and episode duration |

Use JSON initially. Keep adjustable settings outside algorithm code.

## Command-Line Scripts

| Path | Purpose |
| --- | --- |
| scripts/generate_network.py | Generate the SUMO network and verify signal IDs |
| scripts/generate_demand.py | Generate vehicle routes and traffic flows |
| scripts/run_simulation.py | Run a scenario using a selected controller and serve the live viewer |
| scripts/train.py | Train and save the shared PPO policy |
| scripts/evaluate.py | Compare the learned policy against baselines |
| scripts/run_perception.py | Run detection and tracking on real footage |

Scripts parse arguments, load settings, and invoke reusable implementation.
Configuration-driven scripts accept a `--config` argument with a documented
default.

## Reusable Implementation

| Path | Purpose |
| --- | --- |
| src/__init__.py | Package marker |
| src/simulation_adapter.py | SUMO lifecycle and traffic measurements |
| src/demand.py | Seeded vehicle demand, route files, and training scenario sampling |
| src/state.py | Raw traffic-state data structures |
| src/observations.py | Convert raw state into the 44-value observation |
| src/safety_controller.py | Validate requests and execute safe transitions |
| src/rl_environment.py | Synchronous stepping, trajectories, and rewards |
| src/policy.py | Shared actor/value networks and PPO integration |
| src/baselines.py | Fixed-time and actuated controller integration |
| src/metrics.py | Common evaluation metrics |
| src/runner.py | Common episode runner: one SUMO clock, controller requests, safety, metrics |
| src/congestion_detector.py | Persistent-congestion detection |
| src/telemetry.py | Monitoring snapshots, events, and the viewer's local HTTP endpoint |
| src/perception.py | Separate pretrained detection/tracking pipeline |

Keep simulator access, observation construction, signal execution, and learning
logic independently inspectable.

## Simulation Files

| Folder | Contents |
| --- | --- |
| simulation/networks/ | SUMO `.net.xml` road networks |
| simulation/routes/ | Vehicle routes and traffic flows |
| simulation/scenarios/ | `.sumocfg` files referencing networks and routes |

The initial network output is:
`simulation/networks/corridor.net.xml`.

## Data and Outputs

| Folder | Contents |
| --- | --- |
| data/ | Real traffic footage and its source information |
| models/ | Trained checkpoints and associated run metadata |
| results/ | Evaluation tables, logs, and recordings |
| tests/ | Focused checks for safety, observations, and environment stepping |

Exclude raw videos, large checkpoints, and transient recordings from ordinary
Git. Preserve small evaluation summaries and reproduction instructions.

## Documentation

| Path | Purpose |
| --- | --- |
| docs/TRAFFIC_AI_DESIGN.md | System design and implementation milestones |
| docs/PROJECT_STRUCTURE.md | File organization and development conventions |

Keep README.md aligned with working commands. Do not document planned features
as completed capabilities.

## Monitoring Interface

The interface is developed separately by the interface team. The AI side
delivers the live map visualization; the interface embeds it rather than
rendering traffic itself.

| Path | Purpose |
| --- | --- |
| viewer/index.html | Browser map viewer: network, vehicles, signals, and object details |

- `scripts/run_simulation.py` runs a scenario and serves the viewer through
  `src/telemetry.py`, by default at `http://127.0.0.1:8000/`.
- The interface embeds the viewer page in an `<iframe>`.
- `/api/network` and `/api/snapshot` expose the same data as JSON for any
  interface panels.

The viewer and interface display backend state only. Do not duplicate
traffic-control logic in either.

## Current Implementation Step

Create and verify:

- `configs/network.json`
- `scripts/generate_network.py`
- `simulation/networks/corridor.net.xml`

Other files are planned. Create them when their implementation begins.

## Path Conventions

Run documented commands from the project root.

A relative `--config` argument resolves from the terminal's working directory.
Paths inside project configurations resolve from the project root unless
explicitly documented otherwise.

Avoid hardcoded machine-specific absolute paths.

## Reproducibility

1. Commit generation scripts and configurations.
2. Capture exact package versions in requirements-lock.txt after verification.
3. Record Python and SUMO versions in README.md.
4. Commit the small generated network used for the demonstration.
5. Use explicit seeds for demand generation, training, and evaluation.
6. Keep training, validation, and held-out evaluation scenarios separate.
7. Save configuration and version information with model checkpoints.
8. Evaluate controllers using identical demand, seeds, and horizons.

Dependency versions and seeds improve reproducibility; they do not guarantee
bit-identical neural-network training across different hardware.

## Initial Commands

Generate the network:

```powershell
.\.venv\Scripts\python.exe scripts\generate_network.py --config configs\network.json