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

#Specify a crossover probability/rate pc and a mutation probability/rate pm.
crossoverRate = 0.75
mutationRate = 0.01

#Used to clear console output
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

Description: The population size for each board is based on the number of
             chromosomes present in the board, len(totalInput[popIndex])*5.

Input:       totalInput (list of lists): 
                 the input text file as a list of lists.
                 
Returns:     totalEncodedBoardPaths (dictionary of lists of lists): 
                 A dictionary with keys corresponding to the index
                 of the board associated with the population. Dictionary contains a list of
                 individuls that make up the population, whose chromosomes are stored
                 in another list as 1's and 0's, corresponding to chromosomes where
                 1 represents a visited tuple and zero represents a skipped tuple.
'''
def initializePopulation(totalInput):
    #random.randint(0,1)
    totalEncodedBoardPaths = {}
    for popIndex in range(0, len(totalInput)):
        encodedBoardPathsOfPop = []
        for nu in range(0, len(totalInput[popIndex])*5): #create population size of number of chromosomes*5
            encodedBoardPath = []
            for num in range(0, len(totalInput[popIndex])):
                if ((num > 0) and (encodedBoardPath[num-1] == 0)) or (num+1 == len(totalInput[popIndex])) or (num == 0):
                    #print("num + 1 = ", num+1, "  len(board) = ", len(board))
                    encodedBoardPath.append(1)
                else:
                    encodedBoardPath.append(random.randint(0,1))
            encodedBoardPathsOfPop.append(encodedBoardPath)
        totalEncodedBoardPaths[popIndex] = encodedBoardPathsOfPop
    return totalEncodedBoardPaths

'''
Description: Appends the calculated cost of the traversed path (individual)
             to the end of the game path (individual).

Input:       totalInput (list of lists): 
                 the input text file as a list of lists.
                 
Returns:     totalEncodedBoardPaths (dictionary of lists of lists):
                 Same as initializePopulation function with the difference of 
                 the calculated cost of the traversed path (individual) 
                 appended to the end of the game path (individual).
'''
def calcCost(totalInput):
    totalEncodedBoardPaths = initializePopulation(totalInput)
    totalInputIndex = 0
    
    for populationKey in totalEncodedBoardPaths:
        for individual in totalEncodedBoardPaths[populationKey]:
            costsOfGame = []
            for chromosomeIndex in range(0, len(individual)):
                if individual[chromosomeIndex] == 1:
                    costsOfGame.append(totalInput[totalInputIndex][chromosomeIndex])
            # maybe change storage method?
            individual.append(sum(costsOfGame)) #append individual to be popped off for use later
        totalInputIndex = totalInputIndex + 1
    return totalEncodedBoardPaths

'''
Step 2.  The fitness function f(x) for each chromosome in the population is calculated.

Description: ...
Input:       initialPopWithCosts (dictionary of lists of lists):
                The returned function from calcCost.

Returns:     totalEncodedBoardPaths (dictionary of lists):
                A dictionary with the population index as the key, the 
                scores (inverse of cost) of the indexed game paths (individual)
                stored in a list.

'''
def fitnessFunction(initialPopWithCosts):
    fitnessScoresOfPopulation = {}
    for populationKey in initialPopWithCosts:
        fitnessScore = []
        for individual in initialPopWithCosts[populationKey]:
            fitnessScore.append(1/individual[len(individual)-1]) #use the inverse of 
        fitnessScoresOfPopulation[populationKey] = (fitnessScore)
    return fitnessScoresOfPopulation

"""
Description: Divide each f(x) by sum(scores)

Input:       fitnessScores (dictionary of lists):
                The returned function from fitnessFunction.
                
Returns:     selectionProbabilitiesOfPopulations (dictionary of lists):
                A dictionary with the population index as the key, the 
                selection probability (fitness score/sum of fitness scores) of 
                the indexed game paths (individual) stored in a list.
"""
def selectionProbability(fitnessScores):
    selectionProbabilitiesOfPopulations = {}
    for populationKey in fitnessScores:
        selectionProbabilities = []
        for individual in fitnessScores[populationKey]:
            selectionProbabilities.append(individual/sum(fitnessScores[populationKey]))
        selectionProbabilitiesOfPopulations[populationKey] = selectionProbabilities
    return selectionProbabilitiesOfPopulations

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
    #dpSol = getDpSolutions(inputFile)
    initialPopWithCosts = calcCost(totalInput)
    fitnessScores = fitnessFunction(initialPopWithCosts)
    selectionProbabilities = selectionProbability(fitnessScores)
    #costs = calcCost(totalInput)
    '''
    print(totalInput)
    print(encodedPop)
    print("costs: ", costs)
    '''
    for num in range(0, len(totalInput)):
        print("totalInput[", num, "]              = ", totalInput[num])
        for itr in range(0, 5):
            print("initialPopWithCosts[", num, "][", itr,"] = ", initialPopWithCosts[num][itr])
            print("fitnessScores[", num, "][", itr,"] = ", fitnessScores[num][itr])
            print("selectionProbabilities[", num, "][", itr,"] = ", selectionProbabilities[num][itr], "\n")
        print("initialPopWithCosts[", num, "][", len(initialPopWithCosts[num])-1,"]= ", 
              initialPopWithCosts[num][len(initialPopWithCosts[num])-1])
        print("len(initialPop[num]) = ", len(initialPopWithCosts[num]), "\n\n")
        #print("initialPopWithCosts[", num, "] = ", initialPopWithCosts[num])
        #print("costs[", num, "] = ", costs[num])
    
    '''
    printDpSolution(dpSol[0])
    printDpSolution(dpSol[1])
    '''
main()		
#---------------------------------End of Program-------------------------------