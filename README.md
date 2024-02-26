# CS143B Project 2 Virtual Memory README
The Virtual Memory Project cs143b

- In this project I have implemented the extended version of VM manager which supports demnd paging

## Setup
Note: This project is written entirely in python on OpenLab machines. It is recommended to run this project on the UCI Openlab machines.

### Steps to Setup/Run
1. Extract the zip file that was submitted to canvas by huangjk2@uci.edu (ID: 67387111) inside there should be the source code for Project 2

Note: No compilation is necessary for python, this assumes that main.py is in your current working directory
as well as the required initialization files such as init-dp.txt
- Must use redirection operators ("<",">") to redirect in an input file and to write to an output file
- When calling the main.py you must specify the initialization files with the "-i" argument
2. main.py is the shell. To run you must use the redirection operator < to redirect in an input file to stdin and > to redirect stdout to an output file and the "-i" to specify an initialization file to initialize the STs and PTs

An example of running the program:
```
python3 main.py -i init-dp.txt  <inpt.txt >out.txt
```

Assuming init.txt contains valid commands according to specifications on initializing the STs and PTs it will write the output to out.txt given an input files with a list of VAs to translate to
Also the input file (inpt.txt) and the initialization file (init-dp.txt) must be in the same directory as main.py

## Structure of Program

- main.py

The shell of the program takes in commands from stdin and outputs the output to stdout

- VMManager

The core of the program that initializes the PM with STs and PTs and does the VA to PA translation. This
is called by the main.py program for each VA it gets from inpt.txt
