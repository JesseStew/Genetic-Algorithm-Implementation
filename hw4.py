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
import random
#------------------------------------------------------------------------------

#---------------------------------Variables------------------------------------
inputFile = 'input1.txt'
crossoverRate = 0.75
mutationRate = 0.01
clear = 100*'\n'
#------------------------------------------------------------------------------

#---------------------------------Classes/Functions----------------------------
f = open(inputFile, "r")
totalInput = [] #input from one input file
for line in f:
    lyst = line.split() # tokenize input line, it also removes EOL marker
    lyst = list(map(int, lyst))
    totalInput.append(lyst)
    
'''
Step 0.  Algorithm Initialization.  Assume data are encoded in bit strings (1’s and 0’s).
Specify a crossover probability/rate pc and a mutation probability/rate pm.  
Usually pc is chosen to be fairly high and pm is chosen to be very low.

Need to create multiple chromosome variations for each population. Base this on
the length of the num of chromosomes.
'''
def initializePopulation(totalInput):
    #random.randint(0,1)
    totalEncodedBoardPaths = []
    for board in totalInput:
        encodedBoardPath = []
        for num in range(0, len(board)):
            if ((num > 0) and (encodedBoardPath[num-1] == 0)) or (num+1 == len(board)) or (num == 0):
                #print("num + 1 = ", num+1, "  len(board) = ", len(board))
                encodedBoardPath.append(1)
            else:
                encodedBoardPath.append(random.randint(0,1))
        totalEncodedBoardPaths.append(encodedBoardPath)
    return totalEncodedBoardPaths

'''
Returns: a list with the cost of the initialized populations game in the 
         game's associated index.
'''
def calcCost(totalInput):
    totalEncodedBoardPaths = initializePopulation(totalInput)
    totalCosts = []
    for itr in range(0, len(totalInput)):
        costs = []
        for num in range(0, len(totalInput[itr])):
            if totalEncodedBoardPaths[itr][num] == 1:
                costs.append(totalInput[itr][num])
        print(costs)
        totalCosts.append(sum(costs))
    #is not returning correct costs
    return totalCosts

'''
Step 2.  The fitness function f(x) for each chromosome in the population is calculated.
'''
#def fitnessFunction():

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
    encodedPop = initializePopulation(totalInput)
    costs = calcCost(totalInput)
    '''print(totalInput)
    print(encodedPop)
    print("costs: ", costs)'''
    for num in range(0, len(totalInput)):
        print("totalInput[", num, "] = ", totalInput[num])
        print("encodedPop[", num, "] = ", encodedPop[num])
        print("costs[", num, "] = ", costs[num])
    printDpSolution(dpSol[0])
    printDpSolution(dpSol[1])
main()		
#---------------------------------End of Program-------------------------------