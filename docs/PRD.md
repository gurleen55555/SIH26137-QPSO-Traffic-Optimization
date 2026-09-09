# Product Requirements Document
## SIH 2026 — Problem Statement SIH26137
### Quantum-Inspired Intelligent Traffic Route Optimization in Transportation Systems Using Metaheuristic Optimization

| Field | Details |
|---|---|
| Organization | Egreen Quanta |
| Domain | Software \| Fitness & Sports |
| Evaluator Verdict | GREEN — STRONG PICK |
| Submission Deadline | 20 September 2026 |
| Innovation Score | BREAKTHROUGH — Uses advanced/emerging quantum-inspired tech |
| Effort Score | MEDIUM — 7/10 — 7 distinct technical components |
| Technical Feasibility | WORKABLE — Achievable in 36 hrs with focused team priority |
| Competitive Crowding | VERY HIGH — 7 of 226 live SIH 2026 PS ask for similar build |
| Architecture Type | MULTI-LAYER — 3-layer stack: Data → Algorithm → Presentation |
| Team | 5 Members \| All Technical \| 15-Day Sprint |
| Document Version | v1.0 \| September 2026 |

> ⚠️ All 5 team members are expected to read and own every section of this document.

## Table of Contents
1. Pain Points & Core Understanding
2. Feasibility of Execution
3. Impact & Relevance
4. Scope of Innovation & Competitor Analysis
5. Clarity of Problem Statement
6. Evaluator's Perspective
7. Strategy for Team Fit & Execution
8. AI-Buildability Split — The 20/80 Rule
9. Data & Resource Availability
10. Advanced System Architecture
11. QPSO Algorithm Deep-Dive
12. Phase-wise Task Manager (15 Days | 5 Members)
13. Risk Register & Mitigation Plan

---

## 1. Pain Points & Core Understanding 🔎

### 1.1 What Exact Problem Is Being Addressed?
Urban transportation networks are plagued by a combinatorially explosive routing problem — the Vehicle Routing Problem (VRP). As city road graphs scale into thousands of nodes and edges, finding the globally optimal route becomes computationally intractable for classical exact algorithms. VRP is NP-hard: no known polynomial-time solution exists.

The problem is compounded by dynamic real-time changes in traffic load, accidents, and road closures. This PS asks teams to bridge the gap between theoretical quantum computing advantages and practical, deployable solutions using quantum-inspired metaheuristic algorithms — specifically Quantum Particle Swarm Optimization (QPSO) — to generate near-optimal vehicle routes dynamically.

> **KEY INSIGHT:** "Quantum-Inspired" ≠ "Quantum Computing". QPSO runs on classical CPUs — it simulates quantum behavior mathematically. No quantum hardware required. Teams that clarify this instantly gain credibility.

### 1.2 Root Causes of the Problem
- **NP-Hard Complexity**: VRP cannot be solved optimally at scale with classical exact methods (Branch & Bound, Dynamic Programming) within acceptable real-world time frames.
- **Static Routing Systems**: Existing GPS navigation (Google Maps, Waze) is mostly reactive — rerouting only after congestion occurs, not anticipating it proactively.
- **Siloed Data**: Traffic data, weather, events, and vehicle telemetry exist in isolated systems that are rarely integrated into a unified optimization engine.
- **Quantum Hardware Gap**: True quantum computers (IBM Quantum, Google Sycamore) cannot yet run full-scale urban VRP due to qubit noise and decoherence. Quantum-inspired classical algorithms fill this gap practically.
- **Lack of Multi-Vehicle Coordination**: Most routing tools optimize single-vehicle routes, not fleet-level coordinated routing with shared depot and capacity constraints.
- **Convergence Trap in Classical Metaheuristics**: GA and ACO get stuck in local optima for large-scale graphs. QPSO's quantum position update theoretically samples a wider solution space.

### 1.3 Primary Stakeholders & Users
| Stakeholder | Role | How They Benefit |
|---|---|---|
| City Traffic Authorities | System Operators | Real-time congestion reduction, signal optimization data |
| Logistics Companies (Zomato, Flipkart, Delhivery) | Fleet Managers | Reduced delivery time; 10–20% fuel cost savings at scale |
| Public Transport Agencies (BMTC, DTC, BEST) | Route Planners | Optimized bus routes, reduced empty miles, better headways |
| Emergency Services (Ambulance, Fire) | Emergency Responders | Fastest corridor identification in real time — saves lives |
| Individual Citizens / Commuters | End Users | Reduced commute time, lower vehicle emissions, reliable ETAs |
| Smart City Mission / Govt | Policy Makers | Infrastructure planning, congestion analytics, NQM alignment |
| Researchers / Academia | Knowledge Consumers | Validated benchmark data: quantum-inspired vs. classical algorithms |

### 1.4 Current Inefficiencies in Existing Solutions
- **Google Maps / Waze**: Dijkstra/A*-based — optimal for single-source single-destination but completely unequipped for multi-vehicle fleet VRP. No quantum speedup layer.
- **Google OR-Tools**: Heuristic VRP solver. CPU-bound, no real-time traffic integration in the core engine, no quantum-inspired component, complex to configure for new problem types.
- **Classical Metaheuristics (GA, ACO, SA)**: Slower convergence as problem size grows; susceptible to local optima; no live traffic integration in most implementations.
- **Academic QPSO Papers (IEEE/Springer)**: The math exists in literature since 2004 (Sun et al.) but no production-ready system with live traffic integration and UI has been demonstrated publicly.

---

## 2. Feasibility of Execution ⚙️

### 2.1 Can a Working Prototype Be Built in 15 Days?
**YES** — with disciplined scope control. The critical realization: QPSO does NOT need quantum hardware. It is a classical numerical algorithm with quantum-analogous mathematics. Standard Python + NumPy is sufficient.

### 2.2 Technical Requirements Stack
| Component | Tool / Technology | Purpose | Cost |
|---|---|---|---|
| Graph Engine | OSMnx + NetworkX | City road graph from OpenStreetMap — nodes = intersections, edges = roads, weights = time+congestion | Free |
| Traffic Simulation | SUMO (Eclipse) or synthetic generator | Simulate real-time traffic conditions with configurable scenarios | Free |
| Algorithm Core | Python 3.11, NumPy, SciPy | QPSO, PSO, GA, ACO implementations — all in pure Python + NumPy for speed | Free |
| Backend API | FastAPI + Uvicorn + WebSocket | Serve routes, stream real-time QPSO iterations to frontend | Free |
| Database | PostgreSQL + PostGIS | Spatial data storage, historical route logs, graph persistence | Free |
| Cache | Redis | In-memory graph state during real-time weight updates | Free |
| Frontend | React.js + Leaflet.js + D3.js | Interactive map, convergence animation, algorithm comparison panel | Free |
| Containerization | Docker + Docker Compose | One-command demo setup — eliminates "works on my machine" failures | Free |
| Cloud Hosting | AWS EC2 t3.medium / GCP e2-medium | Public URL for demo — evaluators can access from any device | ~$0.04/hr |
| Benchmarking | Custom Python harness + matplotlib | Compare QPSO vs Dijkstra vs GA vs ACO on identical problem instances | Free |

### 2.3 Potential Blockers & Mitigations
| Blocker | Risk Level | Mitigation |
|---|---|---|
| QPSO implementation is mathematically incorrect (effectively just renamed PSO) | CRITICAL | M1 reads Sun et al. 2004 on Day 1. Validates against published benchmark results by Day 2 EOD. M3 independently reviews math. |
| Real-time traffic APIs (TomTom, HERE) rate-limited or inaccessible | HIGH | Use SUMO simulator as primary plan. Real API is bonus only. Never make demo dependent on external API. |
| QPSO too slow on large city graphs (10,000+ nodes) | HIGH | Use zone partitioning — solve 500–800 node subgraphs per zone. Tune swarm to 20–30 particles. Set iteration cap. |
| VRP formulated incorrectly (single-vehicle instead of multi-vehicle) | MEDIUM | Confirm multi-vehicle setup (K≥3) in Day 3 integration checkpoint. Demo must show ≥5 vehicles from Day 8 onward. |
| Integration failures between algorithm core and frontend | HIGH | Reserve ALL of Day 8 for integration only. Add no features until end-to-end smoke test passes. |
| Cloud deployment failure during demo | MEDIUM | Always keep local Docker Compose as backup. Practice switching in Day 14 rehearsal. Cloud = bonus, local = primary. |

### 2.4 MVP Definition (Minimum to Impress Evaluators)
- Real city graph (Bengaluru inner city, ~600–800 nodes) loaded from OpenStreetMap via OSMnx.
- QPSO routing 5 vehicles simultaneously from a shared depot to 8–10 delivery destinations.
- 3 live traffic scenarios (normal, accident, rush hour) injected via UI button — QPSO re-routes in real time.
- Side-by-side benchmark: QPSO vs Dijkstra vs GA vs ACO — showing travel time, total distance, and convergence speed.
- D3.js convergence animation — showing particle swarm iterating toward optimal solution in real time.
- Quantified result: "QPSO achieves X% better solution quality in Y% fewer iterations than GA on this 600-node VRP instance."

---

## 3. Impact & Relevance 🌍

### 3.1 Who Benefits & How
| Beneficiary | Quantified Impact | Potential Scale |
|---|---|---|
| Citizens & Commuters | 15–25% estimated reduction in commute time in optimized corridors | City-level, daily |
| Logistics Sector (₹8.5 Lakh Cr market) | 10–20% fuel cost reduction from optimized fleet routing | Industry-wide |
| Government / Smart Cities | India loses ₹1.5 Lakh Cr/year to congestion (TERI). 10% fix = ₹15,000 Cr savings. | National |
| Emergency Services | WHO estimates 50,000+ preventable road deaths/yr in India. Faster corridors = lives saved. | National |
| Environment | Optimized routing cuts unnecessary fuel burn. Urban vehicles = 30% of city CO₂ emissions. | City-level |
| Research Community | Validated QPSO-vs-classical benchmark on Indian city graphs is novel — publishable contribution. | Global |
| Defence / Critical Infrastructure | Secure convoy routing, emergency evacuation planning — natural PS extension. | National |

### 3.2 Why Evaluators Find This Important
- Aligned with India's Smart City Mission (100 cities) and National Quantum Mission (NQM) — ₹6,000 Cr budget.
- Transportation is a Scope 1 emissions source — optimization is a cost-effective lever for climate goals.
- The "quantum-inspired" framing is intellectually credible, unlike generic "AI/blockchain for everything" submissions.
- Real problem with measurable outcomes — evaluators can ask: "How would you prove it works post-deployment?" and expect a concrete answer.

### 3.3 Scalability Roadmap
| Stage | Timeline | Scope | Stakeholder |
|---|---|---|---|
| Hackathon MVP | Day 0–15 | Single city, 5 vehicles, simulated traffic, benchmark dashboard | Hackathon jury |
| MVP+ | Month 1–3 | Real traffic API integration, 20+ vehicles, REST API for 3rd-party apps | Early adopters |
| Pilot Deployment | Month 4–12 | 1 city government pilot (e.g., BBMP Bengaluru traffic dept) | City authority |
| State Rollout | Year 1–2 | Multi-city, MoU with state transport dept, cloud SaaS pricing | State government |
| National Platform | Year 2–5 | NHAI integration, national ITS framework, white-label SaaS | Central govt + Enterprise |

---

## 4. Scope of Innovation & Competitor Analysis 💡

### 4.1 Existing Solutions — Competitor Matrix
| Solution | Type | Strength | Key Limitation for This PS |
|---|---|---|---|
| Google Maps / Waze | Commercial Navigation | Excellent UX, real-time traffic | Dijkstra/A* only. No fleet VRP. No quantum layer. Black box. |
| TomTom Traffic API | Commercial Traffic Data | Rich live traffic data | Data provider only — no optimization engine. Expensive at scale. |
| Google OR-Tools | Open Source VRP Solver | Production-grade VRP heuristics | CPU-bound. No quantum component. Complex API. No real-time. |
| IBM CPLEX / Gurobi | Enterprise Optimization | Exact solver for small instances | Fails at large-scale VRP (NP-hard time limits). Not real-time. Very expensive. |
| OpenTripPlanner | Open Source Transit | Multi-modal transit routing | Transit scheduling only. No VRP. No ML/quantum element. |
| Academic QPSO Papers (IEEE) | Research Literature | Mathematical foundation validated | No implementation. No UI. Not integrated with real traffic data. Lab only. |
| SUMO + TraCI | Traffic Simulator | Realistic vehicle simulation | Simulation ONLY. No optimization engine. No route recommendation output. |
| Ant Colony / GA Libraries | Research Tools | Established metaheuristics | Slower convergence at scale vs QPSO. No live integration. No UI. |

### 4.2 Innovative Differentiators to Build
- **QPSO Core (Quantum Layer)**: Implement genuine QPSO with quantum rotation gate and wave-function collapse analogy — not just renamed PSO. This is the core moat.
- **Benchmark UI (Live Benchmark Engine)**: Real-time comparison of QPSO vs 3 classical algorithms on the SAME city graph simultaneously. Unique demo power — no product does this visually.
- **Explainability (Convergence Transparency)**: D3.js animated particle swarm visualization showing each particle's journey toward optimal — "explainable quantum AI". Strong demo differentiator.
- **Interactive Demo (Congestion Injection)**: Evaluators inject traffic events (accident, road closure, rush hour) via UI buttons and watch QPSO re-route 5 vehicles simultaneously in <2 seconds.
- **Multi-Objective Fitness**: Optimize simultaneously for time + distance + emissions. Triple-objective QPSO. Most academic papers handle single-objective only.
- **Scalability (Zone-Partitioned Graph)**: Partition city into zones, solve local VRP per zone, stitch with global connector — novel hierarchical QPSO approach enabling city-scale deployment.

### 4.3 Key Research References to Study
- "Quantum-Behaved Particle Swarm Optimization" — Sun, Xu, Feng (2004). IEEE Congress on Evolutionary Computation. Foundation paper. All team members must read.
- "QPSO for Vehicle Routing Problem with Time Windows" — multiple IEEE papers 2018–2023. Direct application of QPSO to VRP.
- "Multi-Objective Metaheuristics for Urban Traffic" — Transport Research Part C (Elsevier). Validates multi-objective framing.
- India National Quantum Mission (NQM) official document — provides policy context for evaluator conversations.

---

## 5. Clarity of Problem Statement 🧩

### 5.1 Exact Deliverables (6 Required Outputs)
| # | Deliverable | Notes |
|---|---|---|
| D1 | Quantum-inspired metaheuristic optimization framework (core algorithm engine) | QPSO must be the primary algorithm — not just PSO or GA |
| D2 | Real-time or simulated traffic condition handling (dynamic graph weight updates) | Either SUMO simulation or live API — evaluators accept both |
| D3 | Transportation network modeled as weighted directed graph | Use OSMnx + NetworkX on real city OSM data |
| D4 | QPSO benchmarked against conventional metaheuristics and exact methods | Compare vs Dijkstra, A*, GA, and/or ACO — all on identical VRP instances |
| D5 | Objectives: minimize travel time, distance, AND traffic congestion simultaneously | Multi-objective fitness function — not single-metric routing |
| D6 | Scalability demonstration for smart-city logistics context | Show on 500+ node graph; argue scalability to full city scale theoretically |

### 5.2 Common Misinterpretations — Danger Zones
- **WRONG**: "We use actual quantum hardware (IBM Q)." — QPSO is quantum-INSPIRED: classical CPU simulation. State this clearly. Evaluators know the difference.
- **WRONG**: "We optimize one vehicle's route." — PS implies fleet routing (multi-vehicle VRP), not single-source shortest path. Show K≥3 vehicles from Day 1 of demo.
- **WRONG**: "Full city-scale production system." — Scope to 600–800 node subgraph for demo; argue scalability analytically. Evaluators understand hackathon limits.
- **WRONG**: "QPSO is enough, no benchmark needed." — PS explicitly states "benchmarked against conventional metaheuristics." Build all 4 algorithms.
- **WRONG**: "Build the UI first, add algorithm later." — Algorithm correctness is the primary evaluation criterion. UI is secondary. QPSO core must work by Day 3.

### 5.3 How to Frame the Solution for Evaluators
- "We didn't just solve routing — we proved that quantum-inspired computing achieves X% better solution quality in Y% fewer iterations than Genetic Algorithms on a 600-node Bengaluru VRP instance."
- "Our system doesn't just route — it adapts. Watch: I inject a traffic accident at MG Road. Our QPSO re-routes all 5 vehicles simultaneously in under 2 seconds."
- "Our benchmark engine is a research contribution in itself. Any team can plug in a new metaheuristic and instantly get a fair comparison against our QPSO baseline."

---

## 6. Evaluator's Perspective 🎯

### 6.1 Evaluation Criteria & Weights
| Criterion | Est. Weight | What Evaluators Look For | Your Target |
|---|---|---|---|
| Innovation & Novelty | 25% | Is QPSO genuine? Does the quantum analogy hold in code and explanation? | Show quantum position update formula in code + explain MBEST verbally |
| Technical Depth | 25% | Working algorithm, correct benchmarking, valid comparison, real numbers | Statistical comparison: 30 runs per algorithm, mean ± std convergence |
| Impact & Problem Fit | 20% | Does the solution address all 6 stated deliverables clearly? | Map each feature directly to D1–D6 in the demo walkthrough |
| Demo Quality & Feasibility | 20% | Live demo on real city data, interactive features, graceful failure handling | Scenario scripts ready; fallback to local if cloud fails |
| Scalability & Sustainability | 10% | Can this grow beyond a hackathon? Architecture decisions, modular code | Show zone-partitioning plan on slide; explain cloud deployment |

### 6.2 Red Flags Evaluators Will Notice
- 🚩 QPSO is just PSO with a name change — "What is the MBEST in your QPSO? Show me the quantum position update line in your code."
- 🚩 Only Dijkstra in the benchmark — "That's a shortest-path algorithm, not a VRP solver. Did you compare with ACO or GA on the same multi-vehicle problem?"
- 🚩 Demo only on toy 10-node graphs — "Can you show it on a real city graph with 500+ nodes? Indian roads?"
- 🚩 No convergence visualization — "How do you know QPSO found a near-optimal solution? Show me the convergence curve."
- 🚩 Single vehicle demo — "The PS says transportation SYSTEMS — plural. Show fleet routing."
- 🚩 Team member cannot explain their component — "Can you walk me through one iteration of QPSO mathematically?"

### 6.3 Likely Evaluator Questions (from PS Image Analysis)
- "Where is your input data coming from — real traffic data or synthetic? If synthetic, how valid is your model?"
- "Walk me through why QPSO is the right choice here and not overkill. Could ACO achieve the same results cheaper?"
- "What happens when connectivity drops, hardware fails, or traffic data is missing? Does the system degrade gracefully?"
- "How would this hold up with real production-scale data — full Bengaluru road graph, 50+ vehicles, actual live API?"
- "Who exactly measures this working after deployment? What KPI would a city authority track?"

---

## 7. Strategy for Team Fit & Execution 👥

### 7.1 Team Composition (5 Members, All Technical)
| Member | Role Tag | Core Skills Required | Primary Ownership |
|---|---|---|---|
| M1 | ALGO — Algorithm Engineer | Python, NumPy, optimization theory, metaheuristics, academic paper reading | QPSO core engine + PSO baseline + algorithm correctness |
| M2 | DATA — Data & Backend Engineer | Python, FastAPI, PostgreSQL, PostGIS, OSMnx, NetworkX, Docker, Redis | Graph pipeline + traffic simulation + database + API server |
| M3 | ML — Benchmarking Engineer | Python, GA/ACO implementation, statistics, matplotlib, pandas | GA + ACO implementations + benchmark harness + convergence analysis |
| M4 | STACK — Full-Stack Integration | FastAPI, WebSocket, REST design, React basics, Docker Compose, cloud CLI | System integration + WebSocket + deployment + API hardening |
| M5 | VIZ — Frontend & Visualization | React.js, Leaflet.js, D3.js, CSS, UX design thinking | Dashboard + interactive map + D3 convergence charts + demo UX |

### 7.2 Step-by-Step Research & Ideation Before Building
1. **Alignment (Day 1 AM)**: All 5 members read the abstract + algorithm section of Sun et al. 2004 QPSO paper. Then read the PS together. Align on what "quantum-inspired" means technically.
2. **Architecture (Day 1 PM)**: Whiteboard session (60 min). Agree on graph model structure, QPSO fitness function terms, API contract, frontend component list.
3. **Prototype (Day 2)**: M1+M3 implement toy QPSO on 10-node test graph, verify convergence vs. PSO baseline. M2 builds graph loader. M4+M5 set up project repo and frontend skeleton.
4. **Checkpoint (Day 3)**: Integration checkpoint. Does QPSO produce valid routes on a 10-node graph? Define MVP acceptance criteria in writing. Unblock blockers now, not Day 8.
5. **Sprint (Days 4–7)**: Parallel sprints. Daily 15-min stand-ups. Blockers surfaced immediately. No "I'll fix it later" culture.
6. **Integration (Day 8)**: Full integration day. Connect all layers. Budget the full day — expect and absorb integration bugs.
7. **Benchmarking (Days 9–11)**: Feature completion + actual benchmark runs. Generate real numbers: convergence speed, solution quality delta.
8. **Demo Prep (Days 12–14)**: Demo rehearsals. Each member must explain the ENTIRE system, not just their module. Simulate tough evaluator questions.
9. **Submission (Day 15)**: Final buffer. Video demo recording as submission backup. Documentation. Submission.

---

## 8. AI-Buildability Split — The 20/80 Rule 🤖

### 8.1 The 20% — What AI Can Build Fast (Scaffolding)
- Graph loading scaffold: OSMnx city graph loader in Python.
- Standard PSO implementation: base class.
- FastAPI boilerplate: REST endpoint structure, CORS setup, Pydantic models, health routes.
- React + Leaflet map scaffold: basic map with marker rendering and polyline drawing.
- Docker Compose file: multi-service container config (api, db, redis, frontend).
- Dijkstra + A* implementations: standard shortest path.

> ⏱ AI acceleration: ~2–3 days of scaffolding compressed to hours. BUT this is ONLY plumbing. The value — QPSO correctness, benchmark validity, system architecture — is NOT in the 20%.

### 8.2 The 80% — What Needs Real Understanding (The Value)
- **QPSO Quantum Extension**: Translating quantum superposition, rotation gates, and wave-function collapse into correct numerical position updates (MBEST formula, β decay). AI generates plausible-looking but often INCORRECT QPSO.
- **Multi-Vehicle VRP Formulation**: Defining the fitness function for fleet routing with depot constraints, capacity limits, optional time windows — requires domain reasoning.
- **Convergence Analysis**: Understanding WHY QPSO converges faster — statistical justification. Cannot be AI-generated on the spot.
- **Real-Time Graph Weight Updates**: Designing a traffic perturbation model that makes routing genuinely dynamic requires transportation domain understanding.
- **Benchmark Validity**: Ensuring all 4 algorithms solve the SAME problem instance with identical constraints and normalized metrics.
- **Architecture Decisions**: Zone partitioning strategy, WebSocket vs polling, PostGIS schema, Redis cache invalidation.

### 8.3 Risk of Over-Relying on AI Output
- **CRITICAL**: AI-generated QPSO frequently implements standard PSO with minor label changes (replacing "velocity" with "quantum_position"). Evaluators will identify this in code review or Q&A.
- **HIGH**: AI benchmark code often has subtle bugs — comparing different problem sizes, not normalizing convergence curves, using different random seeds.
- **MEDIUM**: AI integration code often misses edge cases — empty graph, disconnected nodes, zero traffic weight — causing demo failures.

### 8.4 Spot Question — Can Your Team Answer Live?
> Judge: "Change your fitness function on the spot — add a penalty term for routes crossing more than 3 signalized intersections. Show it affecting routes."

- If team built it and understands it: **YES** — 5-minute change in the fitness function module.
- If team used AI code they don't understand: **NO** — they won't know which file, function, or how the penalty integrates with the quantum position update step.
- **PREPARATION RULE**: Every team member must open every Python file and be able to explain what it does in 2 sentences before Day 12. No exceptions.

---

## 9. Data & Resource Availability 📊

### 9.1 Real, Accessible Datasets & APIs
| Data Source | Type | Access | How to Use |
|---|---|---|---|
| OpenStreetMap (via OSMnx) | Road Network Graph | Free, Open, No key | 3 lines of Python to pull any Indian city graph with nodes, edges, speed limits |
| SUMO (Eclipse Foundation) | Traffic Flow Simulator | Free, Open Source | Generate synthetic vehicle flows on OSM graph; export edge-level traffic density |
| HERE Maps Traffic API | Live Traffic Data | Free tier: 250K calls/mo | Real congestion data, incident reports, historical traffic speed per road segment |
| TomTom Traffic API | Live Traffic Data | Free tier available | Traffic flow, incidents, travel-time variance — sign up Day 1 for API key |
| OpenMobilityData (GTFS feeds) | Public Transit Data | Free, city-specific | Bus/metro route schedules for Indian cities — enriches multi-modal routing |
| data.gov.in (India Open Data) | Historical Transport Stats | Free, public | Traffic volume counts, accident data, road length by city — contextual evidence |
| Kaggle: Traffic/Route Datasets | Historical Traffic | Free, account required | Pre-labeled traffic datasets for training congestion prediction sub-model |

### 9.2 Data Access Strategy (Priority Order)
1. **PRIMARY (Day 1)**: OSMnx — pulls OpenStreetMap data for any Indian city in 3 lines. No signup, no cost, no API key. Use Bengaluru inner city graph (~600 nodes).
2. **SECONDARY (Day 1)**: SUMO — install and configure to generate traffic flows on the OSM graph. Offline — zero internet dependency during demo.
3. **OPTIONAL (Day 1 if pursuing)**: HERE or TomTom free tier. Sign up Day 1 to get API keys. Use only as enrichment layer, not core dependency.

### 9.3 Backup Plan — Synthetic Data (Bulletproof Demo)
- **Synthetic Graph**: Generate a custom weighted directed graph (600 nodes, 2000 edges) using NetworkX. Full control over topology. Guaranteed to work offline.
- **Synthetic Traffic**: Add Gaussian noise to edge weights every 30 seconds. Std dev parameterized per scenario (normal=0.1, rush=0.4, accident=0.8).
- **Pre-Built Scenarios**: 5 scripted scenarios: [1] Normal flow, [2] Morning rush, [3] Accident at key node, [4] Road closure, [5] Event (stadium, parade). Each triggered by a UI button. Deterministic. Impressive.

> **ADVANTAGE**: Synthetic data lets you craft scenarios that perfectly showcase QPSO's superior convergence. Evaluators see a crisp, repeatable, controlled demo — stronger than a flaky live API call.

---

## 10. Advanced System Architecture 🏗️
*(See `architecture.md` for the full standalone architecture spec.)*

### 10.1 Three-Layer Architecture Overview
| Layer | Components | Technology | Responsibility |
|---|---|---|---|
| Layer 1 — Data & Integration | OSMnx Loader, Traffic Feed Processor, Graph Preprocessor, Data Store | OSMnx, NetworkX, SUMO, PostGIS, Redis | Ingest city road graph, apply real-time traffic weights, persist spatial data, serve graph state |
| Layer 2 — Algorithm & AI Core | QPSO Engine, Classical Suite (GA/ACO/Dijkstra), VRP Formulator, Convergence Analyzer, Route Validator | Python, NumPy, SciPy, custom libs | Run optimization algorithms, generate route solutions, benchmark performance, validate output |
| Layer 3 — Presentation & API | FastAPI REST Server, WebSocket Server, React Dashboard, Leaflet Map, D3 Charts, Export Module | FastAPI, React, Leaflet.js, D3.js, Docker | Expose REST + WebSocket API, render interactive map with real-time routes, stream convergence data |

### 10.2 Layer 1 — Data & Integration Layer
- **OSMnx Road Network Loader**: Fetches Bengaluru inner city graph. Converts to NetworkX DiGraph. Nodes = intersections (lat/lon), edges = roads (length, speed_limit, lanes). Persists to PostGIS with spatial index.
- **Traffic Weight Updater**: Receives traffic events from UI or SUMO. Updates edge attribute `traffic_factor ∈ [0,1,…,3x]`. Effective weight = base_distance × speed_factor × traffic_factor × emission_factor. Pushes update to Redis pub/sub.
- **Graph Preprocessor**: Normalizes weights to [0,1]. Computes connected components (isolates disconnected subgraphs). Builds spatial R-Tree index for O(log n) proximity queries. Exports adjacency matrix for algorithm consumption.
- **Backup**: If OSM unavailable, loads precomputed Bengaluru graph from local pickle file. Zero network dependency.

### 10.3 Layer 2 — Algorithm & AI Core
- **QPSO Engine**: Swarm of M particles, each = complete K-vehicle route assignment encoded as permutation list. Quantum position update using MBEST + β-decay. Fitness: `f = α·time + β·distance + γ·congestion + δ·emissions`. Runs for `max_iter=200` or early stop on convergence. Streams best_fitness per iteration to Convergence Analyzer.
- **Classical Algorithm Suite**: Dijkstra (single-vehicle, exact baseline), A* with Euclidean heuristic, Genetic Algorithm (population=50, crossover=PMX, mutation=swap), ACO (pheromone update + evaporation). All accept identical VRP input and fitness function.
- **VRP Formulator**: Encodes multi-vehicle routing. Depot node, K vehicles, N delivery nodes. Capacity constraint per vehicle. Optional time windows. Output: K ordered node sequences.
- **Convergence Analyzer**: Logs (iteration, best_fitness, mean_fitness, diversity) per algorithm per run. Runs 30 repetitions for statistical significance. Computes mean ± std, convergence speed. Generates matplotlib + JSON output.

### 10.4 Layer 3 — Presentation & API Layer
- **FastAPI REST Server**: `POST /optimize`, `POST /scenario`, `GET /graph`, `GET /benchmark`, `GET /routes/history`. Async with Uvicorn. Rate limited.
- **WebSocket Server**: `/ws/routes` (route updates every 5 iterations), `/ws/convergence` (iteration, fitness tuples), `/ws/traffic` (edge weight changes for heatmap).
- **React Dashboard**: Left panel — control inputs; Center — Leaflet.js map with route polylines + animated vehicles + congestion heat overlay; Right — algorithm comparison panel; Bottom — D3.js real-time convergence animation.
- **Export Module**: `POST /export/report` (PDF benchmark report), `GET /export/routes` (GeoJSON).

### 10.5 Data Flow Sequence
1. User selects city + sets depot + destinations + vehicle count via React UI.
2. React sends `POST /optimize` with VRP parameters to FastAPI.
3. FastAPI loads graph from PostGIS + fetches current edge weights from Redis.
4. VRP Formulator encodes the problem instance.
5. QPSO Engine runs: for each iteration → quantum position update → fitness evaluation → best route update.
6. Every 5 iterations: QPSO streams best route set via WebSocket → Leaflet map updates polylines in real time.
7. Simultaneously: Convergence Analyzer streams (iter, fitness) → D3 chart animates particle swarm convergence.
8. QPSO finishes → final routes displayed → Benchmark Engine triggers GA + ACO + Dijkstra on same instance.
9. Benchmark results streamed to comparison panel → evaluator sees head-to-head metrics.
10. User injects traffic event → Traffic Updater reruns QPSO only (fastest) → new routes appear on map.

---

## 11. QPSO Algorithm Deep-Dive ⚛️

### 11.1 Why QPSO Over Classical PSO?
- **Classical PSO**: Position X and velocity V are deterministic real-valued vectors. Velocity update: `V(t+1) = ω·V(t) + c₁·r₁·(pbest-X) + c₂·r₂·(gbest-X)`. Converges but gets trapped in local optima.
- **QPSO Extension**: Removes the velocity concept. Particle exists in a quantum delta potential well centered at attractor p. Position is probabilistically updated using the MBEST (centroid of all personal bests). Theoretically explores a broader solution space.

### 11.2 QPSO Mathematical Core
- **Attractor Point**: `p(t) = φ·pbest + (1−φ)·gbest`, where `φ ~ Uniform(0,1)` drawn fresh each iteration.
- **Mean Best Position (MBEST)**: `C(t) = (1/M) × Σᵢ pbest_i(t)`. The centroid of all personal bests across M particles — the "quantum well center."
- **Quantum Position Update**: `X(t+1) = p(t) ± β(t) × |MBEST(t) − X(t)| × ln(1/u)`, where `u ~ Uniform(0,1)`. The ± is chosen randomly (50/50).
- **β Decay (Contraction-Expansion)**: `β(t) = β_max − (β_max − β_min) × t / T_max`. Typically β_max=1.0, β_min=0.5.
- **Fitness Function**: `f(routes) = α·Σtravel_time + β·Σdistance + γ·Σcongestion_penalty + δ·Σemission_proxy`. Normalize each term to [0,1] before weighting.

### 11.3 VRP Encoding in QPSO (Discrete Route Mapping)
- **Particle Representation**: Each particle `P = [r₁, r₂, …, r_K]` — a list of K route vectors.
- **Continuous-to-Discrete Mapping**: Use Smallest Position Value (SPV) rule: rank the real-valued particle dimensions; ranks map to node visit order.
- **Repair Operator**: After position update, validate routes. If any delivery node is unvisited or visited twice, apply repair operator (cheapest insertion or node swap).
- **Capacity Constraint**: Sum of delivery volumes on each route ≤ vehicle capacity. If violated: `f_penalized = f + λ·violation_amount`.

### 11.4 Hyperparameters & Recommended Settings
| Parameter | Recommended Value | Rationale |
|---|---|---|
| Swarm size M | 20–30 particles | Balances diversity vs computation time. 30 for 600-node graph, 20 for 100-node. |
| Max iterations T_max | 150–200 | Convergence typically observed by iteration 100. 200 as ceiling with early stop. |
| β_max | 1.0 | High initial exploration. |
| β_min | 0.5 | Sufficient exploitation in final iterations. |
| Fitness weights α,β,γ,δ | 0.4, 0.3, 0.2, 0.1 | Prioritize time, then distance, congestion, emissions. Tunable via UI. |
| Penalty λ | 10×avg_fitness | Large enough to make constraint violations non-competitive. |
| Early stop criterion | No improvement in 20 iterations | Trigger if Δbest_fitness < 0.001 for 20 consecutive iterations. |

---

## 12. Phase-wise Task Manager (15 Days | 5 Members) 📅

### Member Roles Quick Reference
| ID | Tag | Role | Primary Ownership |
|---|---|---|---|
| M1 | ALGO | Algorithm Engineer | QPSO implementation, algorithm correctness, quantum math |
| M2 | DATA | Data & Backend Engineer | Graph pipeline, database, traffic simulation, FastAPI server |
| M3 | ML | Benchmarking & ML Engineer | GA, ACO implementations, statistical benchmark harness, convergence analysis |
| M4 | STACK | Full-Stack Integration Engineer | WebSocket, REST design, Docker, cloud deployment, integration testing |
| M5 | VIZ | Frontend & Visualization Engineer | React dashboard, Leaflet.js map, D3.js convergence charts, demo UX |

### PHASE 1 (Days 1–3): Foundation, Research & Baselines
| Day | M1 — ALGO | M2 — DATA | M3 — ML | M4 — STACK | M5 — VIZ |
|---|---|---|---|---|---|
| Day 1 | Read Sun 2004 QPSO paper (all). Implement standard PSO on hand-built 10-node test graph. Verify particle convergence toward known optimum. | Install OSMnx + NetworkX. Pull Bengaluru inner city graph (~600 nodes). Export to JSON. Document node/edge schema. Set up PostgreSQL + PostGIS locally. | Implement Dijkstra + A* on test graph. Write benchmarking harness: runtime, path quality, iteration count. Verify vs known shortest paths. | Init GitHub monorepo (backend/, frontend/, algos/, infra/). Set up FastAPI skeleton with health endpoint. Define API contract with M1+M2+M3. | Create Figma wireframes: Map view, Algorithm panel, Convergence chart, Scenario controls. Set up React + Vite + Tailwind + Leaflet.js. Render static city graph nodes. |
| Day 2 | Extend PSO → QPSO: implement MBEST calculation + quantum position update (β=1.0). Verify on 10-node graph QPSO is competitive with PSO. | Build traffic weight updater: perturbs edge weights based on scenario type (normal/rush/accident). Test 5 scenario presets. Profile memory on 600-node graph. | Implement Genetic Algorithm for VRP: chromosome = route permutation, PMX crossover, swap mutation. Test on 10-node VRP. | Add Docker Compose with 4 services: algo-core (Python), api-server (FastAPI), db (PostgreSQL), frontend (React). Verify inter-service comms with curl. | Build interactive map: clickable node = depot selector, Shift+click = destination. Draw route polyline. Color-code K vehicle routes distinctly. |
| Day 3 | Validate QPSO vs PSO on 10-node graph. Scale to 600-node Bengaluru subgraph. Document findings. Prepare QPSO pseudo-code for team. | Implement Ant Colony Optimization (ACO): pheromone matrix, evaporation. Test weight updater at scale. Implement Redis pub/sub for edge weight change events (<100ms). | Test GA + ACO on identical 10-node VRP. Ensure fair comparison setup. | Connect ALGO module to FastAPI: `POST /optimize` endpoint → triggers QPSO → returns route JSON. Test round-trip latency. Fix serialization issues. | Connect React to API: send depot + destinations → receive K routes → render polylines. End-to-end smoke test. Verify CORS. Fix frontend error states. |

### PHASE 2 (Days 4–7): Core Algorithm Development & Data Pipeline
| Day | M1 — ALGO | M2 — DATA | M3 — ML | M4 — STACK | M5 — VIZ |
|---|---|---|---|---|---|
| Day 4 | Extend QPSO to multi-vehicle VRP: particle = K-route list. Implement SPV encoding. Test 5-vehicle routing on 50-node graph. | Build traffic event system: REST endpoint to trigger predefined scenarios. Store events in PostgreSQL with timestamps. Verify events update Redis edge weights correctly. | Run first benchmark: QPSO vs PSO vs Dijkstra vs GA on 50-node 5-vehicle VRP. Log to CSV. Generate first convergence plot. | Implement WebSocket server: `/ws/routes` pushes best route set every 5 QPSO iterations. Test with wscat. Ensure stable connection over 200 iterations. | Build algorithm comparison panel: 4-column table (QPSO, PSO, GA, ACO). Rows: travel time, distance, congestion score, runtime. Subscribe to benchmark WebSocket. |
| Day 5 | Implement multi-objective fitness: add emissions proxy term. Tune α,β,γ,δ weights. Verify all 4 terms contribute meaningfully. | Integrate SUMO simulation OR finalize synthetic traffic perturbation model. Document assumptions and parameter ranges. Generate 5 prebuilt scenario weight matrices. | Add ACO to benchmark suite. Tune hyperparameters for fair comparison (GA: pop=50, mut=0.1; ACO: ants=30, ρ=0.2; QPSO: M=25, β_max=1.0). | Build remaining REST endpoints: `POST /scenario`, `GET /benchmark`, `GET /graph`, `GET /routes/history`. | Build D3.js convergence chart: real-time animated line chart, X=iteration, Y=best fitness, 4 colored lines. Subscribe to `/ws/convergence`. |
| Day 6 | Implement zone-partitioned QPSO: split 600-node graph into 4 zones by lat/lon boundary. Solve local VRP per zone, stitch at boundary nodes. Test on full graph. | Build historical route analytics store: log every route set to PostGIS. Expose via `GET /routes/history` with filters. | Statistical significance setup: run each algorithm 30 times with different seeds. Compute mean ± std of final fitness and convergence speed. Save stats to JSON. | Implement scenario management: create/reset/trigger scenarios via API. Ensure updates propagate to all active algorithm runs. Test concurrent scenario switching. | Build congestion heatmap overlay: color-code edges by traffic_factor (green/yellow/red). Real-time update via `/ws/traffic`. Toggle button in UI. |
| Day 7 (BUFFER) | Debug QPSO convergence issues found during benchmark. Verify quantum position update formula against Sun 2004 published results. | Data pipeline robustness — handle missing edges, disconnected components, SUMO crashes, Redis drops. Graceful degradation. | Benchmark script robustness — parallel run management, result aggregation, chart generation. Fix GA/ACO correctness issues. | API stability — load test with 5 concurrent `POST /optimize` requests. Fix race conditions in WebSocket broadcast. Add timeout handling. | UI polish for all completed components. Fix map rendering artifacts, polyline z-order, D3 chart axis scaling. Ensure dark-mode consistency. |

### PHASE 3 (Days 8–11): Integration, Real-Time Features & Cloud
| Day | M1 — ALGO | M2 — DATA | M3 — ML | M4 — STACK | M5 — VIZ |
|---|---|---|---|---|---|
| Day 8 (INTEGRATION DAY) | Pair with M4 to trace full flow: UI click → API → QPSO → WebSocket → map update. Fix serialization/callback issues. | Validate data pipeline output matches algorithm input contract. Verify traffic updates reflect in QPSO edge weights during live runs. | Connect benchmark engine to `POST /benchmark`. Verify all 4 algorithms trigger sequentially and stream results correctly. | INTEGRATION LEAD: Orchestrate full end-to-end test. Fix WebSocket disconnects, API timeouts, CORS, Docker network issues. DO NOT ADD FEATURES. | Fix all frontend API connectivity issues. Ensure WebSocket reconnect on drop. Verify chart and map stay in sync during live QPSO run. |
| Day 9 | Implement adaptive β decay: `β(t) = 1.0 − 0.5×(t/T_max)`. Test improvement vs fixed β. Document optimal decay schedule. | Build route analytics dashboard backend: aggregate routes by zone to find congestion hotspots. Expose `GET /analytics/hotspots` (GeoJSON). | Generate final benchmark report data: 30-repetition stat analysis on 600-node 5-vehicle VRP. Tables + PNG charts + JSON. | Implement export API: `POST /export/report` (PDF via reportlab), `GET /export/routes` (GeoJSON). | Build analytics panel: total routes optimized (live counter), avg improvement vs Dijkstra (%), estimated fuel savings, estimated CO₂ reduction. Animated counters. |
| Day 10 | Stress test QPSO on 800-node graph. Profile with cProfile. Optimize: vectorize NumPy, reduce Python loops, early-stop at iteration 150. | Add PostGIS spatial query: routes within bounding box, top-5 most congested edges. Feed hotspots to heatmap overlay. | Add lightweight ML: linear regression on historical edge weights to predict congestion 15 min ahead. Inject predicted weights as QPSO input for one scenario. | Cloud deployment: AWS EC2 t3.medium (or GCP e2-medium). Deploy Docker Compose stack. Configure SSL via Certbot. Test public URL from mobile. | Vehicle animation: smooth animated icons moving along route polylines during QPSO solution playback. Speed proportional to edge travel time. |
| Day 11 | FINAL ALGO config: M=25, T_max=200, β=1.0→0.5, α=0.4,β=0.3,γ=0.2,δ=0.1. Document as `algorithm_config.yaml`. This is the demo config. | Preload 3 city graph backups: Bengaluru (primary), Delhi inner city, Mumbai CBD. Precomputed local pickles. Multi-city demo capability. | FINAL BENCHMARK: complete statistical comparison on Bengaluru 600-node graph. Publication-quality charts. 1-page benchmark summary PDF. | Full system test on cloud URL. Load test with 10 concurrent users. Fix bottlenecks. Write deployment README with one-command launch instructions. | Final UI: loading states, empty states, error components, tooltip explanations for metrics. Responsive for mobile. |

### PHASE 4 (Days 12–14): Testing, Benchmarking, Rehearsal & Demo Prep
| Day | M1 — ALGO | M2 — DATA | M3 — ML | M4 — STACK | M5 — VIZ |
|---|---|---|---|---|---|
| Day 12 | Write algorithm documentation: QPSO math formulation (PDF), parameter guide, code walkthrough. Prepare and practice 5-minute verbal explanation. | Write data pipeline documentation: OSMnx guide, graph schema, traffic model spec, backup data locations. Ensure M4 can run pipeline without M2 present. | Finalize benchmark report PDF: convergence charts, summary table, statistical significance (Wilcoxon test QPSO vs GA). Evaluator handout. | Hardening: graceful error handling throughout API. Validate edge cases (empty graph, no path, zero vehicles, timeout). No crashes. | Script 5 demo scenarios with exact UI steps, expected outcomes, talking points. Time each (target 3–5 min). Record screen for reference. |
| Day 13 | CROSS-TRAIN: explain QPSO to M5 and M2. Both must answer: "What is MBEST? Why does β decrease?" | CROSS-TRAIN: explain data pipeline to M1 and M3. All members can restart services and reload graph independently. | Write evaluator Q&A document (20 Qs + model answers). Distribute to all. Simulate tough evaluator grilling for 60 minutes (M3 plays evaluator). | Load test on cloud: 10 concurrent demo sessions. Verify 600-node QPSO completes in <15s on cloud VM. Verify local fallback works. | Full demo rehearsal #1: complete end-to-end walkthrough in front of full team. Record. Identify weak points, slow UI, unclear metric explanations. |
| Day 14 | REHEARSAL: each member presents their component (3 min). Simulate live fitness-function change with a signal-crossing penalty. Verify team can do it. | FINAL BUFFER: prepare local backup environment. Pre-download all graphs. Test full demo offline. Docker Compose up <60s on demo laptop. | FINAL BUFFER: print benchmark report. One-page technical summary handout. High-res convergence chart PNGs. | FINAL BUFFER: test on evaluator devices (different OS, mobile browsers). Verify cloud URL accessible on venue WiFi. Hotspot backup. | FINAL REHEARSAL #2: full demo run with all 5 members. Time all scenarios. Final UI fixes. Record 3–5 minute backup video demo. |

### DAY 15: Final Buffer, Documentation & Submission
| Time Block | Activity | Owner | Deliverable |
|---|---|---|---|
| 08:00–10:00 | Final cloud deployment check. Run all 5 demo scenarios. Fix overnight issues. | M4 + M2 | Stable cloud URL confirmed |
| 10:00–12:00 | Documentation review: README, API docs, algorithm docs. Must be accurate and readable. | M1 + M3 | GitHub README + `/docs/` folder |
| 12:00–14:00 | Final full-team demo walkthrough. Each member presents their segment. Time box strictly. | All 5 | Aligned demo script |
| 14:00–16:00 | Submission package assembly: code repo, live URL, benchmark PDF, algorithm docs, README. | M4 | Submission folder ready |
| 16:00–18:00 | Backup video demo recording (3–5 min). Upload to shared drive + include in submission. | M5 + M4 | MP4 video demo file |
| 18:00+ | Final submission. Team debrief. Document what to improve for next round. | All 5 | Submitted ✓ |

---

## 13. Risk Register & Mitigation Plan ⚠️

| Risk | Prob. | Impact | Mitigation Strategy | Owner |
|---|---|---|---|---|
| QPSO is mathematically incorrect (effectively PSO) | Med | Critical | M1 validates against Sun 2004 published results by Day 2 EOD. M3 independently reviews quantum position update code. | M1+M3 |
| Integration failure between algorithm core and frontend | High | High | Dedicate ALL of Day 8 to integration. Zero feature additions until end-to-end test passes. M4 leads, all support. | M4 |
| Cloud deployment fails during demo | Med | High | Always run local Docker Compose as primary. Cloud = bonus. Practice switching in Day 14 rehearsal. | M4+M2 |
| QPSO too slow for demo (>30s on 600-node graph) | Med | High | Zone partitioning reduces problem size. Swarm cap at 25 particles. Iteration limit 150 with early stop. Precompute warm-start. | M1 |
| Real traffic API unavailable/rate-limited | High | Low | SUMO + synthetic scenarios are the primary demo plan. External API never in the critical demo path. | M2 |
| Team member cannot explain their component to evaluator | Med | High | Cross-training sessions Days 13–14. Q&A document distributed to all. Every member presents on Day 14. | All |
| VRP formulated as single-vehicle (missing PS requirement) | Med | High | Day 3 checkpoint: demo must show ≥5 vehicles. If not, deprioritize all other features until multi-vehicle works. | M1+M4 |
| Benchmark comparison is invalid (different problem instances) | Med | Critical | Benchmark harness uses identical VRP instance, same graph, same constraints for ALL 4 algorithms. M3 validates. | M3 |
| Demo crashes on evaluator interaction (unexpected input) | High | Med | All input validated in API + frontend. Test boundary cases (0 destinations, full graph, max vehicles) on Day 12. | M4+M5 |
| Team burns out before Day 15 | Med | High | Enforce Day 7 as a buffer/rest day. No all-nighters after Day 12. Scope-cut features before scope-cutting sleep. | All |

---
*SIH26137 | Quantum-Inspired Traffic Optimization | PRD v1.0 | September 2026*
*All 5 members must read, understand, and own every section before the Day 3 checkpoint.*
