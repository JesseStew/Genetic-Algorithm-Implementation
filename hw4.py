""" 
Program:       hw4.py
Programmed By: Brett Spatz and Jesse Stewart
Description:   Solves various Jump-It game boards with a genetic algorithm
               and compares results to a DP approach.
Trace Folder:  stewart013
"""

"""
@Jesse: I took the print statements from the solutions and output them to a
text file. I figured it would get confusing if we added that code to this
program due to needing the same variable names and we really only needed the 
results. We will only need to call the getDPSolutions function once and it
returns a list of lists with the results. I was thinking our main function
would look something like this...

def main():
    dpSol = getDpSolutions(inputFile)
    gaSol = .... (might need multiple functions)
    for i in range(len(number of lines in inputFile):
        printDpSolution(dpSol[i])
        printGaSolution(gaSol[i])
    printAccuracy

"""
#---------------------------------Imports--------------------------------------

#------------------------------------------------------------------------------

#---------------------------------Variables------------------------------------
inputFile = 'input1.txt'
#------------------------------------------------------------------------------

#---------------------------------Classes/Functions----------------------------
"""
Description: ...
Input:       ...
Returns:     ...
"""
def getDpSolutions(inputFile):
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
    dpSol = getDpSolutions(inputFile)
    print(dpSol)
    printDpSolution(dpSol[0])
    printDpSolution(dpSol[1])
main()		
#---------------------------------End of Program-------------------------------