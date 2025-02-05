# Project: A learning resource for Maximum flow minimum cut theorem within the further maths AQA curriculum



## Description 
The maximum flow and minimum cut theorem can be a challenging topic due to multi-path and multi-cuts to analyse and find. The project provided an interactive teaching tool that allows a more versatile approach to building and solving problems within the context of maximum flow minimum cut theorem, giving appropriate solutions, enabling benefits both from a teaching perspective and as a student resource.

#### The project creates an interactive GUI where the user can:  

- Build a directed graph with initial states (sources) and finishing states (sinks) using a custom GUI with Pygame.  
- Determine the maximum flow that could be sent through the graph at any one time, obeying the capacities of each edge.  
- Enable the user to draw their own cuts on the graph and display analysis depending on collisions between edges.  
- Handle edges with a minimum capacity that must be sent through the graph.  
- Add supersources and supersinks as a visual aid for multiple sources and sinks, dynamically positioning them without collision and allocating associated edges.  
- Include node capacities to show that a node can have a limiting capacity within itself, not just its edges.  
- Evaluate the maximum flow as the lower bound and compare this with the minimum cut as the upper bound to find the optimal flow.  

#### Other key features  
 
- Allows the user to hide and show supersources/supersinks/node capacities and cuts to enable a more specific focus on certain elements of the graph.  
- Creates a double outlined node to identify sources/sinks/supersources and supersinks.  
- Creates a custom GUI which included:
    - A scrollbar with ability to display results over a single row or multiple using dynamical underlining on each record independent of the number of rows it holds.
    - Textboxes with sanitisation to filter the inputs to allow strings, integers and floats.
    - Buttons which either have a single purpose or become multi-phase.  
- Collision detection algorithms to check for collisions between nodes and edges.  
- Built the algorithm for maximum flow and minimum cut aspects of the solution from scratch, in particular using the intersection between a cut and edge to determine invalid cuts and the side at which the node lies (either the source or sink side).  
 
**For a more detailed explanation of the project, see the write up folder.**

## How to use the project? 
This projects acts as a tool to create and validate your answers to each graph made. This can be run through the NetwrokFlows10.py file.


Why this project? What does it solve?

## Specific technologies

This uses pygame due to its i

Challenge and future features

What did you learn