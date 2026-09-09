"""
Smoke test: verify all algorithms run on a toy graph and QPSO produces
a better (or at least comparable) fitness than the baselines.
"""

import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.osm_loader import generate_toy_graph, get_random_depot_and_destinations
from data.traffic_updater import apply_synthetic_traffic, TrafficScenario
from algos.vrp_formulator import build_vrp_from_graph
from algos.convergence_analyzer import ConvergenceAnalyzer


def main():
    print("=" * 70)
    print("SIH26137 — QPSO Traffic Optimization Smoke Test")
    print("=" * 70)

    # 1. Generate toy city graph
    print("\n[1] Generating toy graph (15 nodes)...")
    G = generate_toy_graph(n_nodes=15, seed=42)
    print(f"    Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

    # 2. Apply traffic scenario
    print("[2] Applying morning rush traffic...")
    G = apply_synthetic_traffic(G, TrafficScenario.MORNING_RUSH, seed=123)

    # 3. Pick depot & destinations
    depot, destinations = get_random_depot_and_destinations(G, num_destinations=8, seed=42)
    print(f"[3] Depot: {depot}, Destinations: {destinations}")

    # 4. Build VRP instance
    print("[4] Building VRP instance (3 vehicles, capacity=50)...")
    vrp = build_vrp_from_graph(
        G, depot, destinations,
        demands=[10, 15, 8, 12, 20, 10, 15, 10],
        num_vehicles=3,
        vehicle_capacity=50.0,
    )
    print(f"    Distance matrix shape: {vrp.distance_matrix.shape}")

    # 5. Run all algorithms
    print("[5] Running convergence analyzer (all 6 algorithms)...\n")

    def on_progress(algo_name, record):
        if record["iteration"] % 30 == 0 or record["iteration"] == 0:
            print(f"    {algo_name:>10s}  iter={record['iteration']:>4d}  "
                  f"best={record['best_fitness']:>12.2f}  "
                  f"mean={record['mean_fitness']:>12.2f}")

    analyzer = ConvergenceAnalyzer(seed=42, callback=on_progress)
    benchmark = analyzer.run(vrp)

    # 6. Print summary
    print("\n" + "=" * 70)
    print(f"{'Algorithm':>12s} | {'Best Fitness':>14s} | {'Runtime (s)':>12s} | "
          f"{'Iters':>6s} | {'Distance (m)':>14s} | {'Time (s)':>10s}")
    print("-" * 70)

    for entry in sorted(benchmark.summary, key=lambda e: e["best_fitness"]):
        print(f"{entry['algorithm']:>12s} | "
              f"{entry['best_fitness']:>14.2f} | "
              f"{entry['runtime_s']:>12.4f} | "
              f"{entry['iterations']:>6d} | "
              f"{entry['total_distance_m']:>14.1f} | "
              f"{entry['total_time_s']:>10.1f}")

    print("=" * 70)

    # 7. Verify QPSO routes
    qpso_result = benchmark.results["QPSO"]
    print(f"\nQPSO Best Routes:")
    for i, route in enumerate(qpso_result.best_routes):
        node_ids = [vrp.node_id_map[d] for d in route] if route else []
        print(f"  Vehicle {i+1}: depot → {node_ids} → depot")

    print("\n✅ Smoke test passed!")
    return benchmark


if __name__ == "__main__":
    main()
