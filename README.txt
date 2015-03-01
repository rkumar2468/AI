#######################################################################################################################
##  Name:   Rajendra Kumar Raghupatruni                                                                              ##
##  ID:     109785402                                                                                                ##
##  Net-ID: rraghupatrun                                                                                             ##
#######################################################################################################################

Project 1: Peg Solitaire
---------------------------
Description:
***************
    This is a program to find a solution to the game of Peg Solitaire.
    The board consists of peg holders, which can be either empty or hold exactly one peg.
    More information about the game is available at: http://en.wikipedia.org/wiki/Peg_solitaire

Objective: To remove all the pegs except one from the board. This peg should be placed in the center peg holder.

Additional Constraints:
*************************
    - In IDFS - if the levels reached the number of pegs on the board and still the goal is not found the program exits
    - If the 'configuration.txt' file not found in the current directory, the program exits
    - If valid input/choice for the Algorithm to run is not given, the program exits
    - Already visited nodes are not revisited in all the three algorithms

Files:
*********
    - PegSolitaire.py
        * This is the main program file which plays the game.
    - classes.py
        * This file contains the FringeList datastructure definitions and its funtions
    - PrioQueue.py
        * This file contains the Priority Queue data structure implementation using python heap data structure
    - Heuristics.py
        * This file contains the Heuristic definitions and their computations for A* algorithm
    - ReadInput.py
        * This file is responsible to read the 'configuration.txt' file and generate the initial/start state of the
          game.
    - configuration.txt
        * This is the initial configuration of the game.

Testing:
***********
    - Unzip the file, AI-Project01-rraghupatrun.zip
    - Open PyCharm
    - Open the file "PegSolitaire.py" from the un-zipped directory.
    - Update "configuration.txt" file for any specific initial configuration
    - Run the program using "Shift + F10" or "ALT + u" - Click on "Run 'PegSolitaire'"
    - Select the algorithm to run for the given configuration
    - Hit Enter

Results:
-------------

1. Statistics:
----------------
- Time taken:

    S.No    Algorithm       Time Taken(ms)
   ****************************************
    1.      IDFS            13.1
    2.      A* Heuristic 1   2.2
    3.      A* Heuristic 2   4.1

- Memory used for the nodes:

    S.No    Algorithm       Nodes       Memory (Nodes * 50 Bytes)
   ***************************************************************
    1.      IDFS            77          3.8 KB
    2.      A* Heuristic 1   6          300 Bytes
    3.      A* Heuristic 2  12          600 Bytes


2. Outputs
--------------
Input Configuration:
************************

!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 X X X 0 0
  0 0 0 X 0 0 0
  0 0 0 X 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!

ExpandedList:
************************

a) A* Heuristic 1:
-------------------
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 X X X 0 0
  0 0 0 X 0 0 0
  0 0 0 X 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 X X X 0 0
  0 0 0 0 0 0 0
  0 0 0 0 0 0 0
  - - 0 X 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 X 0 0 X 0
  0 0 0 X 0 0 0
  0 0 0 X 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 X X 0 X 0
  0 0 0 0 0 0 0
  0 0 0 0 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 0 0 X X 0
  0 0 0 0 0 0 0
  0 0 0 0 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 0 X 0 0 0
  0 0 0 0 0 0 0
  0 0 0 0 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 0 0 - -
  0 0 0 0 0 0 0
  0 0 0 X 0 0 0
  0 0 0 0 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!

----------------------------------------------------------------------------------------------------------------------

b) A* Heuristic 2:
-------------------
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 X X X 0 0
  0 0 0 X 0 0 0
  0 0 0 X 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 X X X 0 0
  0 0 0 0 0 0 0
  0 0 0 0 0 0 0
  - - 0 X 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 X 0 0 X 0
  0 0 0 X 0 0 0
  0 0 0 X 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 X X 0 X 0
  0 0 0 0 0 0 0
  0 0 0 0 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 0 0 X X 0
  0 0 0 0 0 0 0
  0 0 0 0 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 0 X 0 0 0
  0 0 0 0 0 0 0
  0 0 0 0 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 X 0 0 X 0 0
  0 0 0 X 0 0 0
  0 0 0 X 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 X 0 X X 0 0
  0 0 0 0 0 0 0
  0 0 0 0 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 X X 0 0 0 0
  0 0 0 0 0 0 0
  0 0 0 0 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 X 0 - -
  0 0 0 X 0 0 0
  0 0 0 0 0 0 0
  0 0 0 0 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 X 0 - -
  - - 0 0 0 - -
  0 0 X 0 X 0 0
  0 0 0 X 0 0 0
  0 0 0 X 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 X 0 - -
  - - 0 0 0 - -
  0 0 X X X 0 0
  0 0 0 0 0 0 0
  0 0 0 0 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!
  - - 0 0 0 - -
  - - 0 0 0 - -
  0 0 0 0 0 0 0
  0 0 0 X 0 0 0
  0 0 0 0 0 0 0
  - - 0 0 0 - -
  - - 0 0 0 - -
!===============!

Note: Due to space constraints, the expanded list section has only the A* heuristic 1 and 2  algorithm outputs.

#####################################################-> END <-##########################################################