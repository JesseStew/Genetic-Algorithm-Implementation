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


global inputFile, pc, pm, fitCriteriaMet
inputFile = 'input2.txt' # Specify input file

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

def printGaSolution(chromosome, gameBoard):
    print("GA Solution")
    pathIndices = []
    pathValues = []
    cost = 0
    for num in range(0, len(chromosome)):
        if chromosome[num] == 1:
            cost = cost + gameBoard[num]
            if num == len(chromosome) - 1:
                indVal = str(num)
                pathIndices.append(indVal)
                pathVal = str(gameBoard[num])
                pathValues.append(pathVal)
            else:
                indVal = str(num) + ' -> '
                pathIndices.append(indVal)
                pathVal = str(gameBoard[num]) + ' -> '
                pathValues.append(pathVal)
    print("minimum cost: ", cost)
    print("path showing indices of visited cells: ", end = "")
    for i in range(0, len(pathIndices)):
        print(pathIndices[i], end = "")
    print("\n" + "path showing contents of visited cells: ", end = "")
    for i in range(0, len(pathValues)):
        print(pathValues[i], end = "")
    print("\n" + "=========================")
    return cost


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
    for i in range(0, len(gameBoard)*250):
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
Description: Utilizes pc to determine if crossover occurs. If it doesn't,
             children represent clones of parents.
Input:       locustCandidateList, default value is none. May need to call
             itself with updated list if selected locust produces bug.
             parents, list containing parent chromosomes
Returns:     list containing children chromosomes
"""
def crossover(locustCandidateList, parents, pc):
    pCross = pc*100
    crossVal = random.randint(0, 100)
    if locustCandidateList == [None]:
        locustCandidateList = [x for x in range(1, len(parents[0]))]
    if crossVal <= pCross and locustCandidateList != []:
        locust = random.choice(locustCandidateList)
        if locustCheck(locustCandidateList, parents, locust) == True:
            children = []
            leftChild = parents[0][:locust] + parents[1][locust:]
            children.append(leftChild)
            rightChild = parents[1][:locust] + parents[0][locust:]
            children.append(rightChild)
            return children
        else:
            #del locustCandidateList[locust - 1]
            locustCandidateList.remove(locust)
            #crossover(locustCandidateList, parents, pc)
            children = crossover(locustCandidateList, parents, pc)
            return children
    else:
        return parents


"""
Description: Checks to make ensure crossover at locust point will produce
             a valid output
Input:       locustCandidateList, parents, locust
Returns:     Bool, true if locust is valid, false if not
"""
def locustCheck(locustCandidateList, parents, locust):
    if (parents[0][locust - 1] == 0 and parents[1][locust] == 0):
        return False
    else:
        return True


    # Step 3c
"""
Description: Utilizes mc to determine if children will be mutated or not. If
             they will be, values at randomly selected index will be flipped.
Input:       children, list containing 2 child chromosomes
Returns:     children, updated list with new values mutation occurs.
"""
def mutate(children, mc):
    mCross = int(mc*1000)
    mutVal = random.randint(0, 1000)
    if mutVal == mCross:
        mutIndex = random.randint(1, len(children[0]) - 1)
        for i in range(0, 2):
            if children[i][mutIndex] == 0:
                children[i][mutIndex] = 1
            else:
                children[i][mutIndex] = 0
            return children
    else:
        return children

# Algorith step 4 functions:
"""
Description: Creates a new population to replace the old population after step
             3 operations are applied.
Input:       oldPop, original population list. popFitness, original population
             list of fitness values. pc, probability of crossover. mc,
             probability of mutation.
Returns:     newPop, list containing new population consisting of children.
"""
def newPopulation(oldPop, popFitness, pc, mc):
    newPop = []
    while len(newPop) != len(oldPop):
        popSelectProb = selectionProbability(popFitness)
        parents = selectParents(oldPop, popSelectProb)
        candList = [None]
        children = crossover(candList, parents, pc)
        children = mutate(children, mc)
        for item in children:
            newPop.append(item)
    return newPop


# Algorithm step 5 functions:
def getBestFitVal(dpGameboardSol):
    minCost = int(dpGameboardSol[1].strip().split(':')[1])
    bestFit = 1 / minCost
    return bestFit






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

    total = len(gameBoards) # Holds total number of boards for accuracy rate
    incorrect = 0 # Holds total number of incorrect solutions for accuracy rate

    """
    Step 0: Specify a crossover probability/rate pc and a mutation
    probability/rate pm.
    """
    pc = 0.75
    pm = 0.001

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
        bestFitVal = getBestFitVal(dpSol[i])


		"""
		Step 5. Determines if any population matches fitness criteria for
		stopping point.
		"""
        fitCriteriaMet = False
        for index in range(0, len(popFitness)):
            if popFitness[index] == bestFitVal:
                fitCriteriaMet = True
                printDpSolution(dpSol[i])
                printGaSolution(population[index], gameBoards[i])
                break

        """
        Step 3 and 4. Select parents, crossover and mutate, generate new
        population.
        """
        if fitCriteriaMet == False:
            newPop = newPopulation(population, popFitness, pc, pm)
            newPopFitness = fitness(newPop, gameBoards[i])
            for index in range(0, len(newPopFitness)):
                if newPopFitness[index] == bestFitVal:
                    fitCriteriaMet = True
                    printDpSolution(dpSol[i])
                    printGaSolution(newPop[index], gameBoards[i])
                    break

			"""
			Step 5. Stops after one generation is created (specified in
			homework instructions).
			"""
            bestCandidateFitness = max(newPopFitness)
            bestCandidate = newPop[newPopFitness.index(bestCandidateFitness)]

            dpCost = printDpSolution(dpSol[i])
            gaCost = printGaSolution(bestCandidate, gameBoards[i])

			# Find number of incorrect answers
            if (dpCost != gaCost):
                incorrect += 1

    # Evaluate and print accuracy rate
    accuracyRate = ((total - incorrect) / total)
    print("GA overall Accuracy: " + "{:.2%}".format(accuracyRate))


main()
