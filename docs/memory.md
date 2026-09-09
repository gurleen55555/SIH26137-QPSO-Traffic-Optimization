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

## 6. Known Risks Agents Should Watch For
- QPSO silently degrading into plain PSO during refactors (missing MBEST / β decay / quantum update term).
- Benchmark code comparing algorithms on different problem sizes/seeds (invalidates all comparison claims).
- Demo-breaking edge cases: empty graph, disconnected nodes, zero vehicles, zero destinations — must
  degrade gracefully, never throw an unhandled exception in front of evaluators.
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
