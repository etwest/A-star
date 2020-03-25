#A Star Algortihm
A little bit of code I wrote for fun. It works prehaps surprisingly well.

##Implementation
This code currently works on an assumption for the heuristic that the nodes on the graph are positions in 2D space. This informs our estimation of the cost from node `x` to the end `h(x)` using the straight line cost between the nodes.
###Using a different Heuristic
The parts of the code that would need to be changed are within the `node` class. Specifically the `calc_dist` function, the constructor, and the internals of the node.