order v 10 : vertex.
var a, b : vertex.

before (a, a.next).
before (a, b) -> before (a, b.next).

edge (a, b), before (b, a) -> False.

-- A graph is acyclic when it can be embedded in a linear order; 
-- that is, when there exists a labeling l : V → Z of the vertices
-- such that ij ∈ E implies l(i) < l(j) for all i, j ∈ V 

-- Janota, M.; Grigore, R.; and Manquinho, V. M. 2017. On the
-- quest for an acyclic graph. In Proceedings of the 24th RCRA
-- International Workshop on Experimental Evaluation of Al-
-- gorithms for Solving Problems with Combinatorial Explo-
-- sion 2017 co-located with the 16th International Conference
-- of the Italian Association for Artificial Intelligence (AI*IA
-- 2017), Bari, Italy, November 14-15, 2017, volume 2011 of
-- CEUR Workshop Proceedings, 33–44. CEUR-WS.org
