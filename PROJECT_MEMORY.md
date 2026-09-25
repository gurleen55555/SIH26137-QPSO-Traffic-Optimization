# Project Memory — SIH26137 Quantum-Inspired Traffic Route Optimization

> Purpose: a persistent context file for AI coding agents (Antigravity, Claude Code, Cursor, etc.) and
> teammates jumping into this repo. Read this before touching code. Keep it updated as decisions change.
> Full detail lives in `PRD.md` (requirements) and `architecture.md` (system design) — this file is the
> condensed "load-bearing facts" version.

## 1. What This Project Is
- SIH 2026, Problem Statement **SIH26137**. Team: 5 members, 15-day sprint, deadline **20 Sept 2026**.
- Goal: a **quantum-inspired metaheuristic** (QPSO — Quantum Particle Swarm Optimization) that solves
  multi-vehicle VRP (Vehicle Routing Problem) on a real city road graph, with real-time traffic re-routing,
  benchmarked against Dijkstra/A*/GA/ACO.

## 2. Non-Negotiable Facts (do not re-derive, do not contradict)
- **"Quantum-inspired" ≠ quantum hardware.** QPSO is a classical NumPy algorithm. No qubits, no
  quantum SDKs, no IBM Q / D-Wave dependency anywhere in this codebase.
- **Multi-vehicle only.** Single-vehicle shortest path (plain Dijkstra) is a baseline, never the deliverable.
  Demo must show **K ≥ 3** vehicles (target 5) from a shared depot.
- **QPSO must be real QPSO**, not renamed PSO. It must implement: MBEST (mean best position),
  the quantum position update with `ln(1/u)`, and β contraction-expansion decay. See `architecture.md §5`
  for exact formulas. If asked to "optimize" or "simplify" the QPSO update, do not remove these terms.
- **Benchmark fairness is a hard requirement.** QPSO, PSO, GA, ACO, Dijkstra/A* must all run on the
  *identical* problem instance (same graph snapshot, same depot/destinations, same constraints, same
  fitness function). Never let a refactor cause them to diverge.
- **Local Docker Compose is the primary demo path.** Cloud (AWS/GCP) is a bonus layer, never a hard
  dependency for the demo to function.
- **Live external traffic APIs (HERE/TomTom) are optional enrichment only.** SUMO or the synthetic
  Gaussian-noise traffic generator is the primary/critical-path mechanism. Never make the demo depend
  on an external API being up.

## 3. Tech Stack (locked in, don't swap without team discussion)
| Concern | Choice |
|---|---|
| Graph | OSMnx + NetworkX (Bengaluru inner city, ~600–800 nodes primary) |
| Algorithms | Python 3.11 + NumPy + SciPy (QPSO, PSO, GA, ACO, Dijkstra, A*) |
| Traffic sim | SUMO (Eclipse) or synthetic Gaussian-noise generator |
| Backend | FastAPI + Uvicorn + WebSocket |
| DB | PostgreSQL + PostGIS |
| Cache | Redis (pub/sub for live edge-weight updates) |
| Frontend | React.js + Leaflet.js + D3.js |
| Containers | Docker + Docker Compose |
| Cloud (bonus) | AWS EC2 t3.medium / GCP e2-medium |

## 4. Team & Ownership (so agents know who to attribute/ask)
| Tag | Member | Owns |
|---|---|---|
| ALGO | M1 | QPSO core, PSO baseline, algorithm correctness |
| DATA | M2 | Graph pipeline, traffic simulation, DB, API server |
| ML | M3 | GA + ACO, benchmark harness, convergence stats |
| STACK | M4 | Integration, WebSocket, deployment, API hardening |
| VIZ | M5 | React dashboard, Leaflet map, D3 charts, demo UX |

## 5. Current Phase / Where We Are
- [ ] Phase 1 (Days 1–3): baselines — PSO/QPSO on toy 10-node graph, graph loader, FastAPI/React skeletons.
- [ ] Phase 2 (Days 4–7): multi-vehicle QPSO, GA/ACO, WebSocket streaming, D3 convergence chart, buffer day.
- [ ] Phase 3 (Days 8–11): **Day 8 = integration-only, no new features.** Cloud deploy, analytics, exports.
- [ ] Phase 4 (Days 12–14): docs, cross-training, evaluator Q&A rehearsal, load testing, demo rehearsals.
- [ ] Day 15: final buffer, submission package, backup video.

> Update the checkboxes above as phases complete — this is the fastest way for an agent to know current
> state without re-reading the full PRD.

## 5. Current Phase / Where We Are

### M1 Status

- [x] QPSO core implementation completed.
- [x] QPSO MBEST calculation implemented.
- [x] Quantum position update with `ln(1/u)` implemented.
- [x] β contraction-expansion decay implemented.
- [x] Multi-vehicle particle decoding implemented.
- [x] Five-vehicle routing validated.
- [x] Multi-objective fitness implemented using PRD weights.
- [x] Dynamic traffic-weight evaluation integrated into route evaluation.
- [x] Bengaluru 800-node graph tested.
- [x] 600-node scalability/performance test completed.
- [x] QPSO vs PSO matched-seed validation completed.
- [x] QPSO pseudocode prepared.
- [x] Reusable M1 algorithm modules added under `algorithm/`.

### Current M1 Results

- QPSO configuration: 25 particles, 200 iterations, β = 1.0 → 0.5.
- Particle dimension for the current 8-destination / 5-vehicle test setup: 12.
- Objective weights: travel time 0.40, distance 0.30, congestion 0.20,
  emissions 0.10.
- QPSO vs PSO validation used 10 matched seeds.
- Mean QPSO fitness: **0.14833190**.
- Mean PSO fitness: **0.15687216**.
- QPSO had lower final fitness for all 10 matched seeds in the tested setup.
- 600-node test: 25 particles, 150 iterations, **32.23 s**.
- 800-node test: 25 particles, 200 iterations, **46.19 s**.




## 6. Known Risks Agents Should Watch For

- QPSO silently degrading into plain PSO during refactors
  (missing MBEST / β decay / quantum update term).
- Benchmark code comparing algorithms on different problem sizes, seeds,
  graph snapshots, destinations, constraints, or fitness definitions
  (invalidates comparison claims).
- QPSO runtime becoming too high on larger graphs.
  PRD mitigation strategies include zone partitioning, swarm capping,
  iteration limits with early stopping, and warm starts.
- Single-vehicle routing being used in the demo instead of the required
  multi-vehicle demonstration. The PRD demo configuration uses **5 vehicles**.
- QPSO mathematical correctness must be validated against the intended
  QPSO formulation; M1 owns QPSO correctness work and M3 independently
  reviews the quantum update implementation.
- Full list with probability/impact/mitigation: see `PRD.md §13`.

## 7. File Map
- `PRD.md` — full requirements, evaluator expectations, deliverables (D1–D6), risk register, 15-day plan.
- `architecture.md` — system architecture, API contracts, WebSocket channels, QPSO math reference,
  repo layout, data flow, reliability/degradation rules.
- `memory.md` — this file. Quick-load context for agents/new contributors.

## 8. Compute Notes (see chat answer below for full explanation)
- No GPU is required anywhere in this project. All algorithms (QPSO/PSO/GA/ACO/Dijkstra/A*) are
  classical CPU-bound NumPy code — there is no neural network being trained. A laptop CPU is sufficient.
- Antigravity (or any agentic IDE) is a development environment, not a compute backend — it executes on
  whatever machine/terminal it's attached to. It doesn't provide free GPUs itself.

### M1 Algorithm Modules

- `algorithm/decoder.py` — particle decoding into destination ordering and vehicle routes.
- `algorithm/evaluator.py` — evaluates an individual route on the road graph.
- `algorithm/solution_evaluator.py` — evaluates all vehicle routes and aggregates solution metrics.
- `algorithm/fitness.py` — objective normalization and PRD-defined weighted fitness.
- `algorithm/qpso.py` — core QPSO update, MBEST calculation, and generic QPSO functionality.
- `algorithm/objective.py` — decodes and evaluates a particle against the routing problem.
- `algorithm/optimizer.py` — complete QPSO optimization loop for the multi-vehicle routing problem.
- `algorithm/__init__.py` — exports the reusable M1 algorithm components.
- `algorithm/M1_QPSO_Bengaluru_Data_Inspection.ipynb` — M1 Bengaluru dataset inspection and validation notebook.

## 8. M1 Implementation Notes

The following are current implementation choices used for the M1 validation setup.
They should not be treated as additional PRD requirements without team agreement.

- Current test instance: 1 depot + 8 destinations + 5 vehicles.
- Particle representation currently uses 12 continuous values:
  8 values determine destination ordering and 4 values determine route split positions.
- The current route decoder uses a sigmoid transformation before sorting the particle values.
- The current Bengaluru test graph is an undirected NetworkX MultiGraph with 800 nodes
  and 1056 edges.
- The current traffic test uses traffic factors applied to edge travel time.
- The current emissions calculation uses distance × `vehicle_weight_factor`.
  The current test implementation uses `vehicle_weight_factor = 1.0` because the
  provided dataset does not contain this field.
- Normalization bounds used for the current validation setup are fixed reference bounds.
- The current 600-node performance test was created as a connected subgraph while
  preserving the required depot and destination nodes.

> If the PRD does not explicitly specify one of these implementation details,
> agents must not treat it as a new project requirement.