import math
import os
import random
import sys

# get current directory
path = os.getcwd()
parent = os.path.dirname(path)
sys.path.append(parent)

from algorithms import Greedy
from dataModels import Solution

class SimulatedAnneling():
    def __init__(self, dataModel, temperature=-1, alpha=-1, stoppingTemperature=-1, stoppingIter=-1):
        self.dataModel = dataModel
        self.size = len(dataModel.customerDict)
        self.temperature = math.sqrt(self.size) if temperature == -1 else temperature
        self.alpha = 0.995 if alpha == -1 else alpha
        self.stoppingTemperature = 1e-8 if stoppingTemperature == -1 else stoppingTemperature
        self.stoppingIter = 100 if stoppingIter == -1 else stoppingIter
        
        self.initalTemperature = self.temperature
        self.iteration = 1
        self.bestSolution = None
        self.bestFitness = float('Inf')
        self.fitnessList = []

    def initialSolution(self):
        '''
        Return an initial solution using Greedy algorithm
        '''
        solution =  Greedy.greedy(self.dataModel)
        currentFitness = solution.totalLength()
        if currentFitness < self.bestFitness:
            self.bestSolution, self.bestFitness = solution, currentFitness
        self.fitnessList.append(currentFitness)
        return solution, currentFitness

    def accept(self, candidate):
        """
        Accept with probability 1 if candidate is better than current.
        Accept with probabilty acceptP(..) if candidate is worse.
        """
        candidateFitness = candidate.totalLength()
        print(f'candidate fitness: {candidateFitness}')
        if candidateFitness < self.currentFitness:
            self.currentFitness, self.currentSolution = candidateFitness, candidate
            if candidateFitness < self.bestFitness:
                self.bestFitness, self.bestSolution = candidateFitness, candidate
        else:
            if random.random() < self.acceptP(candidateFitness):
                self.currentFitness, self.currentSolution = candidateFitness, candidate
        # print(self.currentSolution, self.currentFitness)

    def acceptP(self, candidateFitness):
        """
        Probability of accepting if the candidate is worse than current.
        Depends on the current temperature and difference between candidate and current.
        """
        return math.exp(-abs(candidateFitness - self.currentFitness) / self.temperature)

    def anneal(self):
        """
        Execute simulated annealing algorithm.
        """
        self.currentSolution, self.currentFitness = self.initialSolution()

        while self.temperature > self.stoppingTemperature and self.iteration < self.stoppingIter:
            candidateSolutionList = self.currentSolution.solutionList

            l = random.randint(2, self.size - 1)
            i = random.randint(0, self.size - l)

            # candidateSolutionList[i : (i + l)] = reversed(candidateSolutionList[i : (i + l)])

            subList = candidateSolutionList[i : (i + l)]
            random.shuffle(subList)
            candidateSolutionList[i : (i + l)] = subList
            
            candidate = Solution.Solution(candidateSolutionList, self.dataModel)
            self.accept(candidate)
            self.temperature *= self.alpha
            self.iteration += 1

            self.fitnessList.append(self.currentFitness)

            print("Best fitness obtained: ", self.bestFitness)
            improvement = 100 * (self.fitnessList[-1] - self.bestFitness) / (self.fitnessList[-1])
            print(f"Improvement over greedy heuristic: {improvement : .2f}%")
            # print(f"FitnessList: {self.fitnessList}")

    def batchAnneal(self, times=100):
        """
        Execute simulated annealing algorithm `times` times, with random initial solutions.
        """
        for i in range(1, times + 1):
            print(f"Iteration {i}/{times} -------------------------------")
            self.temperature = self.initalTemperature
            self.iteration = 1
            self.currentSolution, self.currentFitness = self.initialSolution()
            self.anneal()