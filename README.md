# Path Finding Visualizer

GUI to visualize how path finding algorithms find the shortest path. Speed and explored nodes can be seen visually.

## Path Finding Algorithms
* A*
* Depth First Search
* Dijkstra's
* Greedy Breadth First Search

## How to use
### Mouse
* Left click and left click drag is used to build walls
* Right click is used to add a start and ending node
* Right click drag is used to revert nodes back to open tiles
### Buttons
* Algorithm Selection: Used to select the path finding algorithm
* Grid Height: The number of rows
* Grid Width: The number of columns
* Run Speed: How long to wait between steps of the algorithm in seconds
* Reset Grid: Clears the grid
* Run: Finds the path between start and ending nodes

## Colors
* Green: Starting node
* Red: Goal node
* Cyan: Explored nodes
* Purple: Frontier (to be explored) nodes
* Orange: Found path from start to goal

## TO-DOs
* When resizing or when changing the number of rows/columns, the grid resets
* Can't change run speed while finding the path
