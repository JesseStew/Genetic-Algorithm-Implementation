""" 
Program:       hw4.py
Programmed By: Brett Spatz and Jesse Stewart
Description:   Solves various Jump-It game boards with a genetic algorithm
               and compares results to a DP approach.
Trace Folder:  stewart013
"""


import sys
import modified_DP_solution as dpFile
import random

global inputFile, pc, pm
inputFile = 'input1.txt' # Specify input file

#Used to clear console output
clear = 100*'\n'


"""
Description: Gather game boards from input file and convert to list of lists
Input:       inputFile, text document with gameboard data
Returns:     totalInput, list of lists containing gameboard data
"""
def getGameBoards(inputFile):
    f = open(inputFile, "r")
    gameBoards = [] #input from one input file
    for line in f:
        lyst = line.split() # tokenize input line, it also removes EOL marker
        lyst = list(map(int, lyst))
        gameBoards.append(lyst)
    f.close()
    return gameBoards


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

  
# Algorithm step 1 functions:
"""
Description: Initialize the population for the current gameboard. Encodes the
             boards with 1's and 0's with 1 representing visited nodes and 0's
             representing skipped nodes.
Input:       gameBoard, list holding values for each node of the gameboard.
Returns:     population, list containing sublists representing each chromosome.
"""
def initializePopulation(gameBoard):
    population = []
    for i in range(0, len(gameBoard)*2):
        chromosome = []
        for num in range(0, len(gameBoard)):
            if ((num > 0) and (chromosome[num-1] == 0)) or \
                (num + 1 == len(gameBoard)) or (num == 0):
                 chromosome.append(1)
            else:
                chromosome.append(random.randint(0,1))
        population.append(chromosome)
    return population

 
# Algorithm step 2 functions:
"""
Description: Evaluates the chromosomes of a population for their fitness using
             the inverse of their total cost.
Input:       population, contains list of chromosomes. gameBoard, contains list
             of the given gameboard values.
Returns:     populationFitness, List containing fitness values of each
             chromosome in the population.
"""
def fitness(population, gameBoard):
    populationFitness = []
    for chromosome in population:
        cost = 0
        for num in range(0, len(chromosome)):
            if chromosome[num] == 1:
                cost = cost + gameBoard[num]
        #populationFitness.append(cost)
        fitness = 1 / cost
        populationFitness.append(fitness)
    return populationFitness


# Algorithm step 3 functions:
    # Step 3a
"""
Description: Determines the probability of a chromosome being selected for
             reproduction.
Input:       populationFitness, list containing fitness of values of each
             chromosome in the population.
Returns:     selectionProb, list containing the probabilities of each
             chromosome being selected.
"""
def selectionProbability(populationFitness):
    selectionProb = []
    fitSum = 0
    for chromosomeFitness in populationFitness:
        fitSum = fitSum + chromosomeFitness
    for chromFit in populationFitness:
        chromSelProb = chromFit / fitSum
        selectionProb.append(chromSelProb)
    return selectionProb


"""
Description: Selects two parent chromosomes from the population utilizing
             selection probability as weights for selection.
Input:       population, list containing all chromosomes for the gameboard.
             selectionProb, list containing the probabilities of each
             chromosome being selected.
Returns:     parents, list containing the two selected chromosomes
"""
def selectParents(population, selectionProb):
    parents = random.choices(population, weights = selectionProb, k = 2)
    return parents

    
    # Step 3b
"""
Description: ...
Input:       ...
Returns:     ...
"""
'''@@@@@@@@@@@@@@@
Bool function to check if the selected locust will work or produce the bug
'''
def locustCheck(locustCandidateList, parents, locust):
    if (parents[0][locust - 1] == 0 and parents[1][locust + 1] == 0):
        return False
    else:
        return True
    
    
"""
Description: Utilizes pc to determine if crossover occurs. If it doesn't,
             children represent clones of parents.
Input:       locustCandidateList, default value is none. May need to call
             itself with updated list if selected locust produces bug.
             parents, list containing parent chromosomes
Returns:     list containing children chromosomes
"""
'''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
I tried to utilize another bool function for this to handle the bug with double
0's. I also literally just noticed the bug that it might not crossover when
looping back because it calculates the chance at the start of the function.
Could just put that line of code in main before crossover is called.
'''
def crossover(locustCandidateList = None, parents):
    pCross = pc*100
    crossVal = random.randint(0, 100)
    if crossVal <= pc:
        if locustCandidateList == None:
            locustCandidateList = [x for x in range(1, len(parents[0] - 1))]
            locust = random.choice(potentialLocusts)
            children = []
            if locustCheck == True:
                for i in range(0, locust):
                    leftSide = 
            else:
                crossover(locustCandidateList, parents)
    else:
        return parents
        
    
    
    # Step 3c
""" 
Description: Utilizes mc to determine if children will be mutated or not. If
             they will be, values at randomly selected index will be flipped.
Input:       children, list containing 2 child chromosomes
Returns:     children, updated list with new values mutation occurs.
"""
''' @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Needs some error handling for mutations causing two 0s in a row
'''
def mutate(children):
    mCross = mc*100
    mutVal = random.randint(0, 100)
    if mutVal == mCross:
        mutIndex = random.randint(1, len(children[0]) - 1)
        if children[mutIndex] == 0:
            children[mutIndex] = 1
        else if children[mutIndex] == 1:
            children[mutIndex] = 0
    return children
    else:
        return children

# Algorith step 4 functions:
"""
Description: ...
Input:       ...
Returns:     ...
"""
'''@@@@@@@@@@@@@@@@@@@@@@@@
I think this function will loop the functions in step 3 until its repopulated
with new children
'''
#def newPopulation():


# Algorithm step 5 functions:
"""
Description: ...
Input:       ...
Returns:     ...
"""
'''@@@@@@@@@@@@@@@@@@@@@@@@
Might not need a termination function. in Main we could add a generations
variable that stops when it hits 1. Also, can compare the fitness values after
step 2 in main to a variable thats made from dpSol minimum cost to see if any
of the fitness values match the minimum cost's fitness. 
'''
#def termination():
#------------------------------------------------------------------------------

#---------------------------------Program Main---------------------------------
def main():
    """
    Creates a new text document, passes input file to a slightly modified
    version of the provided DP solution file to get the DP results, and then 
    writes the results to a new text document.
    """
    writeFile = open(inputFile[:-4]+'dpSolution.txt', "w")
    origSysOut = sys.stdout
    sys.stdout = writeFile
    dpFile.runFile(inputFile)
    writeFile.close()
    sys.stdout = origSysOut
    
    gameBoards = getGameBoards(inputFile) # List of gameboards in input file
    dpSol = getDpSolutions(inputFile) # Gather DP solutions
    
    """
    Step 0: Specify a crossover probability/rate pc and a mutation 
    probability/rate pm.
    """
    pc = 0.75
    pm = 0.01
    
    for i in range(0, len(gameBoards)):
        """
        Step 1. Initialize population
        """
        population = initializePopulation(gameBoards[i])
        
        """
        Step 2. The fitness function f(x) for each chromosome in the 
        population is calculated.
        """
        popFitness = fitness(population, gameBoards[i])
        
        """
        Step 3a. Selection. Assign probability of selection to each chromosome.
        Select a pair of chromosomes to be parents
        """
        popSelectProb = selectionProbability(popFitness)
        parents = selectParents(population, popSelectProb)
        
        """
        Step 3b. Crossover. Select randomly chosen locust. With probability pc,
        perform crossover with the parents forming two new offspring or clone 
        two exact copies of the parents.
        """
        #crossover(parents)
        
        """
        Step 3c. Mutation.  With probability pm , perform mutation on each of 
        the two offspring. 
        """
        
        
        """
        Step 4. The new population of chromosomes replaces the current 
        population.
        """
        
        
        """
        Step 5.  Check termination criteria.  If convergence is achieved then 
        stop and report results, otherwise go back to Step 2.
        """
        
        
        '''
        print(testPop, '\n')
        print(testPopFitness, '\n')
        print(testPopSelectProb, '\n')
        print(parents)
        '''
main()		
