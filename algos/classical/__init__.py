"""Classical baseline algorithms for VRP benchmarking."""

from algos.classical.dijkstra import DijkstraSolver
from algos.classical.astar import AStarSolver
from algos.classical.genetic_algo import GeneticAlgorithmSolver
from algos.classical.ant_colony import AntColonySolver

__all__ = ["DijkstraSolver", "AStarSolver", "GeneticAlgorithmSolver", "AntColonySolver"]
