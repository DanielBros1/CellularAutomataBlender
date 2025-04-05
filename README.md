# Cellular Automata in Blender

## Project Description

Project is a visual simulation of city growth based on simple, cellular automata-style rules. The project is built using **Blender's Python API**, featuring a dynamic 3D animation of houses, trees, and rivers evolving over time.

## Key Features

- Automatically generates grid-based city landscape:
  - random placement of initial houses in the center,
  - procedural generation of a river across the map,
- The simulation runs for `25` time steps (`STEPS`), updating the grid at each stage.
- Houses are created or destroyed based on the number of neighboring houses.
- Destroyed houses may occasionally be replaced by trees.
- Fully automated object duplication, animation, and transformation using Blender keyframes.


## Simulation Rules

- A house is **created** if a cell has **2 or 3 neighboring houses**.
- A house is **destroyed** if it has **1 or 4+ neighboring houses**.
- In 15% of destruction events, a **tree** is planted in the house’s place.
- Trees may also cause the destruction of up to 4 neighboring houses.
- A river is generated procedurally, flowing vertically from one side of the grid to the other.

## How to Run

1. Open your `cellular_automata.blend` file (included in the repository).
2. Paste the contents of `main.py` into Blender's **Scripting Editor**.
3. Press **Run Script**.
4. The animated simulation

## Images: 

<img src="https://github.com/user-attachments/assets/3abd01ab-59d3-49ce-ad6d-6bcb7fe54ec7" width="400">


https://github.com/user-attachments/assets/6f84e15a-3183-4377-a729-e3aa9b1ab300

https://github.com/user-attachments/assets/8c1d207a-0c93-4d6b-a816-6866f439e40b

##### Author:
## @Daniel Broś