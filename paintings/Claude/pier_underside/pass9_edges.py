P = piles()
# along a boundary, never across it -- and one pass, not three
q0 = P[0]                                   # near-left pile: lose its top into the gloom
s.smudge([(q0.bounds[0] + 0.004, 0.03), (q0.bounds[0] - 0.002, 0.16),
          (q0.bounds[0] + 0.005, 0.30)])
s.smudge([(q0.bounds[2] - 0.003, 0.04), (q0.bounds[2] + 0.004, 0.19),
          (q0.bounds[2] - 0.002, 0.33)])
# the deck's far-left underside edge, deep in shadow: let it go completely
s.smudge([(0.0, 0.712), (0.09, 0.694), (0.19, 0.672), (0.27, 0.654)])
# the mid pile's foot, where it meets its own reflection
q2 = P[2]
s.smudge([(q2.bounds[0] - 0.004, 0.722), (q2.bounds[2] + 0.004, 0.729)])
# the top of the joist stack, softened into the dark overhead
s.smudge([(0.06, 0.038), (0.42, 0.010), (0.78, -0.014)])
s.look(path="out/12_edges.png")
s.look(values=True, path="out/12_edges_values.png")
