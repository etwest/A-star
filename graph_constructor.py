#! /usr/local/bin/python3.7

from random import random

nodes = 100000

with open("newGraph", "w") as file:
    file.write("""# each node contains an x,y coordinate point that defines its 
# location. 
# the weights of the edges are simply their length on the grid
# using a simple distance calculation sqrt((x1 - x2)^2 + (y1 - y2)^2)
""")
    for i in range(nodes):
        x = round(random() * 2500, 2)
        y = round(random() * 2500, 2)
        n_num     = int(random() * (float(nodes) * .005))
        neighbors = ""
        n_list    = []
        for _ in range(n_num):
            n = random() * nodes
            if n not in n_list:
                neighbors += "\t" + str(int(n))
                n_list.append(n)
        file.write(str(i) + "\t" + str(x) + "\t" +str(y) + neighbors + "\n")
