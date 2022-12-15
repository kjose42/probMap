coordinates have the format (column, row).
column is represented by x.
row is represented by y.

To generate maps, we ran generateTestcases.py.

To generate the output files and visuals for the maps, we ran generateTruths.py. 
Purple represent "hard to traverse" blocks, yellow represent highway blocks, and gray represents blocked blocks. 
Truth files are called InfoFileXforMapY.txt
X is the truth file's identifying number and Y represents the corresponding map's number. For example, InfoFile5forMap6.txt is the fifth ground truth file for map 6 (and map 6's file is testcase6.txt)

For part B, we ran probMap to calculate the probabilities of the agent being in each cell. The user inputs a map file and a ground truth file. When the map is generated, the user will see the probabilities for the first step and the agent's true location (the agent is represented by a blue circle). The user can control the simulation. They can say how many steps they want the program to advance with by inputting a number in the command line.

To generate a graph of the average error (between the agent's actual location and the filtering's estimation) for each step, we ran errGraph. The user inputs a map file and a ground truth file.

To generate a graph of the average probability (of the cell that the agent is actually in) for each step, we ran probGraph. The user inputs a map file and a ground truth file.

(info and maps folders are for Question 5 part B)
