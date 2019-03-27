
# Five in a Row (Omok; Gomoku)

## Overview
This is a game of five in a row developed in Python 3.7. It supports CLI & GUI, and contains an artificial intelligence module. It was written in object-oriented structure in order to provide compatibility for future updates and implementation into other frameworks.

## Modules
###### main.py
Module that creates instances of classes necessary to run the application

###### omok_ai.py
Artificial intelligence module that, at construction of an instance, receives five in a row board instance and an index that indicates which side the AI will play on. Two instances of this module will be made to have the computer match itself. Once an instance is made, start() and stop() methods may be invoked in order to make and kill a thread that plays the game on the five in a row board instance that was given at construction. The module uses alpha beta pruning algorithm to calculate the next best move. Variables like area or depth may be edited to increase functionality while sacrificing speed, or vice versa. evaluateboard() method provides evaluation of predicted moves for the algorithm, and the evaluation criteria may be changed to improve the AI.

###### omok_board.py
The actual game engine which contains the five in a row board class. If only an instance of this class is made, the game may be played in CLI using play() and reset() methods. Every method and field that is necessary to realize the game is contained in this module; every other module is just an appendix to this module, which uses methods and fields in this module to run the game. duplicate() method is provided in order to simulate and predict game when GUI is loaded.

###### omok_checker.py
This module provides a class that contains static methods for checking various conditions in given board instance. Some of those conditions are defeat, draw, three to three, and much more which are to be implemented in future updates

###### omok_gui.py
Provides a class that creates GUI that is dependent on given five in a row board instance. Upon GUI user interaction, this module invokes an appropriate method in given board instance. When the board instance is modified in CLI manner, this module also updates the GUI. 

## Others
1. "res" folder contains images for GUI
1. "sample" folder contains screen captures that demonstrate appropriate run of the application
1. There are many improvements to be made, including GUI appearance, AI efficiency, full implementation of gomoku rules, online game support, and much more
