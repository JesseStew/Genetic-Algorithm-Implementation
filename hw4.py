""" 
Program:       hw4.py
Programmed By: Brett Spatz and Jesse Stewart
Description:   Solves various Jump-It game boards with a genetic algorithm
               and compares results to a DP approach.
Trace Folder:  stewart013
"""

"""
def main():
-    dpSol = getDpSolutions(inputFile)
-    gaSol = .... (might need multiple functions)
-    for i in range(len(number of lines in inputFile):
-        printDpSolution(dpSol[i])
-        printGaSolution(gaSol[i])
-    printAccuracy
-
-"""
#---------------------------------Imports--------------------------------------
import sys
import modified_DP_solution as dpFile
import random
#------------------------------------------------------------------------------

#---------------------------------Variables------------------------------------
global inputFile
inputFile = 'input1.txt' # Specifiy input file

#Specify a crossover probability/rate pc and a mutation probability/rate pm.
crossoverRate = 0.75
mutationRate = 0.01

#Used to clear console output
clear = 100*'\n'
#------------------------------------------------------------------------------

#---------------------------------Classes/Functions----------------------------
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

'''
-------------------------------------------------------------------------------
------------------------Code-Inserted-from-hw4Remake.py------------------------
-------------------------------------------------------------------------------
'''
'''
Step 3a.  Selection.  Using the values from f(x), assign probability of 
          selection to each chromosome xi. 
'''
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

'''
Step 3a.  Selection (cont.). Select a pair of chromosomes to be a parent, 
          allowing chromosomes to potentially pair with itself
'''
"""
Description: Selects two parent chromosomes from the population utilizing
             selection probability as weights for selection.
             
Input:       population (dictionary of lists of lists):
                A dictionary with keys corresponding to the index
                of the board associated with the population.
                
             selectionProbabilities (dictionary of lists):
                 A dictionary with the population index as the key
    
Returns:     parents (dictionary of lists):
                 A dictionary of lists containing the two selected chromosomes
"""
def selectParents(population, selectionProbabilities):
    parents = {}
    for popKey in population:
        parents[popKey] = random.choices(population[popKey], weights = selectionProbabilities[popKey], k = 2)
    return parents
 
'''
Step 3b.  Crossover.  Select randomly chosen locust (crossover point).  With 
probability pc , perform crossover with the parents forming two new offspring 
or clone two exact copies of the parents.
'''
"""
Description: ...
Input:       ...
Returns:     ...
"""
'''@@@@@@@@@@@@@@@
Bool function to check if the selected locust will work or produce the bug
crossoverRate = 0.75
mutationRate = 0.01

Description: Utilizes pc to determine if crossover occurs. If it doesn't,
             children represent clones of parents.
             
Input:       parents (dictionary of lists):
                 A dictionary of lists containing the two selected chromosomes.

Returns:     children (dictionary of lists):
                 A dictionary of lists containing the product of the chromosome 
                 swap for each parent in parents.
                 Note:
                   # May need to change this so that there the crossoverRate is 
                   # factored in for each parent combination
'''
def crossover(parents):
    children = {}
    randomness = random.random()
    print("random = ", randomness)
    print("crossoverRate = ", crossoverRate)
    if crossoverRate >= randomness:
        for parentsKey in parents:
            #creates a random int corresponding to an index within the board game
            locus = random.randint(0, len(parents[parentsKey][0])-1)
            child = []
            #checks for two concurrent 0's with selected locus 
            #if true, loops until a good locus has been selected
            while parents[parentsKey][0][locus - 1] == 0 and parents[parentsKey][1][locus] == 0:
                locus = random.randint(0, len(parents[parentsKey][0])-1)
            print("locus = ", locus)
            for chromosomeIndex in range(0, len(parents[parentsKey][0])):
                #append beginning of first parent to child
                if chromosomeIndex < locus - 1:
                    child.append(parents[parentsKey][0][chromosomeIndex])
                else: #append end of second parent to child
                    child.append(parents[parentsKey][1][chromosomeIndex])
            children[parentsKey] = child
    return children
   
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
'''

#------------------------------------------------------------------------------
"""
Description: Gathers output from dynamic programming solution into a list, 
             formats the minimum cost line, and creates sublists representing
             each gameboard's output.
Input:       Text file containing output of dynamic programming solution's
             print statements.
Returns:     List containing sublists for each gameboard's dynamic programming
             solutions.
"""
#------------------------------------------------------------------------------

#---------------------------------Program Main---------------------------------
def main():
    """
    Creates a new text document, passes input file to a slightly modified
    version of the provided DP solution file to get the DP results, and then 
    writes the results to the new text document.
    """
    writeFile = open(inputFile[:-4]+'dpSolution.txt', "w")
    origSysOut = sys.stdout
    sys.stdout = writeFile
    dpFile.runFile(inputFile)
    writeFile.close()
    sys.stdout = origSysOut
    
    dpSol = getDpSolutions(inputFile)
    
    totalInput = getGameBoards(inputFile)
    
    '''
    Step 0.  Algorithm Initialization.  Assume data are encoded in bit strings 
    (1’s and 0’s). Specify a crossover probability/rate pc and a mutation 
    probability/rate pm.  Usually pc is chosen to be fairly high and pm is 
    chosen to be very low.
    '''
    #done in calcCost(totalInput) using initializePopulation(totalInput)
    population = initializePopulation(totalInput)
    
    '''
    Step 1.  The population is chosen consisting of n chromosomes each of length 𝑙.
    '''
    initialPopWithCosts = calcCost(totalInput)
    
    
    '''
    Step 2.  The fitness function f(x) for each chromosome in the population is calculated.
    '''
    fitnessScores = fitnessFunction(initialPopWithCosts)
    
    '''
    Step 3a.  Selection.  Using the values from f(x), assign probability of 
    selection to each chromosome xi. 
    '''
    selectionProbabilities = selectionProbability(fitnessScores)
    
    '''
    Step 3a.  Selection (cont.). Select a pair of chromosomes to be a parent, 
    allowing chromosomes to potentially pair with itself
    '''
    parents = selectParents(population, selectionProbabilities)
    
    '''
    Step 3b.  Crossover.  Select randomly chosen locust (crossover point).  With 
    probability pc , perform crossover with the parents forming two new offspring 
    or clone two exact copies of the parents.
    '''
    children = crossover(parents)
    
    '''
    print(totalInput)
    print(encodedPop)
    print("costs: ", costs)
    '''
    for num in range(0, len(totalInput)):
        '''
        for itr in range(0, 5):
            print("initialPopWithCosts[", num, "][", itr,"] = ", initialPopWithCosts[num][itr])
            print("fitnessScores[", num, "][", itr,"] = ", fitnessScores[num][itr])
            print("selectionProbabilities[", num, "][", itr,"] = ", selectionProbabilities[num][itr], 
                  "\n\n------------NEW-INDIVIDUAL------------\n")
        '''
        print("initialPopWithCosts[", num, "][", num,"] = ", initialPopWithCosts[num][num])
        print("fitnessScores[", num, "][", num,"] = ", fitnessScores[num][num])
        print("selectionProbabilities[", num, "][", num,"] = ", selectionProbabilities[num][num])
        print("\n------------STATS------------\n")
        print("parents[", num, "] = ", parents[num], "\n")
        print("totalInput[", num, "]              = ", totalInput[num])
        print("initialPopWithCosts[", num, "][", len(initialPopWithCosts[num])-1,"]= ", 
              initialPopWithCosts[num][len(initialPopWithCosts[num])-1], "\n")
        print("parents[", num, "] = ", parents[num], "\n")
        print("children[", num, "] = ", children[num], "\n")
        print("len(initialPop[num]) = ", len(initialPopWithCosts[num]), "\n",
              "\n------------NEW-BOARD------------\n")
        #print("initialPopWithCosts[", num, "] = ", initialPopWithCosts[num])
        #print("costs[", num, "] = ", costs[num])
    print(children)
    '''
    printDpSolution(dpSol[0])
    printDpSolution(dpSol[1])
    '''
main()		
#---------------------------------End of Program-------------------------------