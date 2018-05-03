""" 
Program:       hw4.py
Programmed By: Brett Spatz and Jesse Stewart
Description:   Solves various Jump-It game boards with a genetic algorithm
               and compares results to a DP approach.
Trace Folder:  stewart013
"""

#---------------------------------Imports--------------------------------------
import sys
import modified_DP_solution as dpFile
#------------------------------------------------------------------------------

#---------------------------------Variables------------------------------------
global inputFile
inputFile = 'input1.txt'
#import modified_DP_solution as dpFile
#------------------------------------------------------------------------------

#---------------------------------Classes/Functions----------------------------
"""
Description: Gathers output from dynamic programming solution into a list, 
             formats the minimum cost line, and creates sublists representing
             each gameboard's output.
Input:       Text file containing output of dynamic programming solution's
             print statements.
Returns:     List containing sublists for each gameboard's dynamic programming
             solutions.
"""
def getDpSolutions(inputFile):
    #dpFile.runFile()
    solutionFile = inputFile[:-4]+'dpSolution.txt'
    with open(solutionFile, 'r') as f:
        lines = [i.strip() for i in f.readlines()]
        lines[1::5] = ['minimum ' + num for num in lines[1::5]]
    solutions = [lines[x*5:x*5+5:] for x in range(int(len(lines)/5))]
    return solutions


"""
Description: Takes a list containing the dynamic programming solution for a
             single game board and prints out the information needed in the
             format matching the assignment example.
Input:       List with dp solution.
Output:      Game board, min cost, path indices, and path content.
"""
def printDpSolution(dpSolution):
    print(dpSolution[0] + '\n' + dpSolution[4] + '\n' + "DP Solution")
    for i in range (1, 4):
        print(dpSolution[i])
    print(dpSolution[4])

    
#------------------------------------------------------------------------------

#---------------------------------Program Main---------------------------------
def main():
    writeFile = open(inputFile[:-4]+'dpSolution.txt', "w")
    origSysOut = sys.stdout
    sys.stdout = writeFile
    dpFile.runFile(inputFile)
    writeFile.close()
    sys.stdout = origSysOut
    dpSol = getDpSolutions(inputFile)
    #print(dpSol)
    printDpSolution(dpSol[0])
    printDpSolution(dpSol[1])

main()
#---------------------------------End of Program-------------------------------