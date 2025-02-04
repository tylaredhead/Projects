# Project: A learning resource for Maximum flow minimum cut theorem within the further maths AQA curriculam



## Description 
The project provided an interactive teaching tool that allowed a more versatile solution to building and solving the problems within the context of maximum flow minimum cut thereom, giving appropiate solutions, enabling benefits both from a teaching perspective and as a student resource.

### The project creates an interactive GUI where the user can:  

- Build a directed graph with initial states (sources) and finishing states (sinks) using a custom GUI with Pygame.  
- Determine the maximum flow that could be sent through the graph at any one time, obeying the capacities of each edge.  
- Enable the user to draw their own cuts on the graph and display analysis depending on collisions between edges.  
- Handle edges with a minimum capacity that must be sent through the graph.  
- Add supersources and supersinks as a visual aid for multiple sources and sinks, dynamically positioning them without collision and allocating associated edges.  
- Include node capacities to show that a node can have a limiting capacity within itself, not just its edges.  
- Evaluate the maximum flow as the lower bound and compare this with the minimum cut as the upper bound to find the optimal flow.  

### Other key features  

    -Allows the user to hide and show supersources/supersinks/node capacities and cuts to enable a more specifc focus on certain elements of the graph.  
    -Creates a double outlined node to identify sources/sinks/supersources and supersinks.  
    -Creates a custom GUI with a scrollbar, textboxes with sanitisation as well as buttons, coping for button with multiple phases and text going over multiple lines within the scrollbar.  
    -Collision detection algorithms to check for collisions between nodes and edges.  
    -Built the algorithm for maximum flow and minimum cut aspects of the solution from scratch, in particular using the intersection between a cut and edge to determine invalid cuts and the side at which the node lies (either the source or sink side).  
 
**For a more detailed explanation of the project, see the write up folder.**

## How to use the project?  

Why this project? What does it solve?

Specific technologies

Challenge and future features

What did you learn