# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

   1. Find the labels of sudoko box which has two digits values
    2. Group the labels which have same value
    3. Group out the peers of two same value label
    4. Delete the same value from the grouped out peers

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In the naked twins func, we first set the constraint as the sudoko box has two digit values, this will filter out the sudoku
box labels which have only two digits values out. Then we group the labels out which have same box values. Then for the same value's labels
we add constraint that they must have a number of common peers, after we find out the common peers, we can narrow down the digit values of
those common peers. This help us further reduce the number of possibilities of some boxes.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We add diagonal constraint which is among the two main diagonals, the numbers 1 to 9 should all appear exactly once, we do so by adding
the two main diagnals boxs into our peers, this help enhance the constraints to meet the requirements of diagmonal soduku.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.