import random
import graph_tool.topology as gt_topo
from MVE_solver import nx2gt
from parse import *
from utils import *

class MVNSolver:
    def __init__(self, target):
        self.target = target

    def solve(self, g, c):
        return self.solve_bf(g, c)

    def solve_bf(self, g, c):
        source = g.vertex(0)
        mask_v = g.new_vertex_property("bool")
        g.set_vertex_filter(mask_v, inverted=True)
        ret = []

        for _ in range(c):
            v_list, _ = gt_topo.shortest_path(g, source, self.target, weights=g.edge_properties['weight'])
            if len(v_list) == 2:
                break;
            elif not is_connected(g):
                return ret[:len(ret) - 1]
            min_dist = float("-inf")
            best_v = 0
            for v in v_list[1 : len(v_list) - 1]:
                mask_v[v] = 1
                dist = gt_topo.shortest_distance(g, source, self.target, weights=g.edge_properties["weight"])
                if dist > min_dist:
                    min_dist = dist
                    best_v = v
                mask_v[v] = 0
            mask_v[best_v] = 1
            ret.append(g.vertex_index[best_v])
        if not is_connected(g):
            return ret[:len(ret) - 1]
        return ret

if __name__ == "__main__":
    for i in range(1, 300):
        path = f"inputs/large/large-{i}.in"
        G = read_input_file(path)
        G = nx2gt(G)
        mnv_solver = MVNSolver(G.vertex(G.num_vertices() - 1))
        c = mnv_solver.solve(G, 5)
        k = []
        print(c)
        G.set_vertex_filter(None)
        assert is_valid_solution(G, c, k)
        print("Sample: " + str(i) + " Shortest Path Difference: {}".format(calculate_score(G, c, k)))
        write_output_file(G, c, k, 'test.out')
