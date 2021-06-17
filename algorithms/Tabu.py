from random import randrange, sample
from itertools import combinations
from dataModels import Solution
from algorithms import Greedy
class Tabu():
    def __init__(self, dataModel, pwi=0.1, lookSol=False, 
                inp=100, sizeNeighbor=3, sizeTabus=0.3):
        self.dataModel = dataModel
        self.distanceMatrix = dataModel.distancesMatrix
        self.lookSol = lookSol
        self.iteratorsNotImprove = inp
        self.sizeNeighbor = sizeNeighbor
        self.sizeTabus = sizeTabus
        self.bestSolution = None
        self.currentSolution = None
        self.percentWithInitial = pwi
        self.firstSolution = self.initialSolution()
        self.quantityCustomer = self.dataModel.dataDescription["DIMENSION"]

    def initialSolution(self):
        solution = Greedy.Greedy(self.dataModel).solve()
        return solution

    def chooseBestNeighbor(self, neighborsList):
        bestSolution = neighborsList[0]
        bestDistance = neighborsList[0].totalDistance
        for neighbor in neighborsList:
            if neighbor.totalDistance < bestDistance:
                bestSolution = neighbor
                bestDistance = neighbor.totalDistance
        return bestSolution

    def createNeighbor(self, bestNeighborChange):
        neighborSolution = self.currentSolution.solution.copy()
        indexChange1 = bestNeighborChange[0]
        indexChange2 = bestNeighborChange[1]
        neighborSolution[indexChange1], neighborSolution[indexChange2] = neighborSolution[indexChange2], neighborSolution[indexChange1]                                                                       
        return Solution.Solution(neighborSolution, self.dataModel)

    def checkTabus(self, bestNeighborSolution, tabus):
        for indexTabu in tabus:
            if bestNeighborSolution.solution[indexTabu] == self.currentSolution.solution[indexTabu]:
                return True
            else:
                return False
    
    def updateTabus(self, tabus, bestNeighborSolution):
        for index in range(self.quantityCustomer):
            if (bestNeighborSolution.solution[index] 
                    != self.currentSolution.solution[index] and index not in tabus):
                if len(tabus) == round(self.quantityCustomer * self.sizeTabus):
                    tabus.pop(0)
                    tabus.append(index)
                else:
                    tabus.append(index)
                break

    def compareToCurrentSol(self, solution):
        if solution.totalDistance < self.currentSolution.totalDistance:
            return True
        else: 
            return False
    
    def compareToBestSol(self, solution):
        if solution.totalDistance < self.bestSolution.totalDistance:
            return True
        else: 
            return False

    def mainTabu(self, neighborsList, tabus, terminationCriteriaStatus):
        while neighborsList:
            bestNeighborSolution = self.chooseBestNeighbor(neighborsList)
            neighborsList.pop(neighborsList.index(bestNeighborSolution))

            if self.checkTabus(bestNeighborSolution, tabus) == False:
                if self.compareToBestSol(bestNeighborSolution):
                    self.bestSolution = bestNeighborSolution
                    self.updateTabus(tabus, bestNeighborSolution)
                    self.currentSolution = bestNeighborSolution
                    terminationCriteriaStatus == True
                    break
                else:
                    self.updateTabus(tabus, bestNeighborSolution)
                    self.currentSolution = bestNeighborSolution
                    terminationCriteriaStatus == False
                    break

            else:
                if self.compareToCurrentSol(bestNeighborSolution):
                    if self.compareToBestSol(bestNeighborSolution):
                        self.bestSolution = bestNeighborSolution
                        self.updateTabus(tabus, bestNeighborSolution)
                        self.currentSolution = bestNeighborSolution
                        terminationCriteriaStatus == True
                        break
                    else:
                        self.updateTabus(tabus, bestNeighborSolution)
                        self.currentSolution = bestNeighborSolution
                        terminationCriteriaStatus == False
                        break

                else:
                    self.currentSolution = bestNeighborSolution
                    self.updateTabus(tabus, bestNeighborSolution)
                    terminationCriteriaStatus == False      
        return terminationCriteriaStatus

    def solve(self):
        tabus = []
        self.bestSolution = self.currentSolution = self.firstSolution
        stopValue = self.currentSolution.totalDistance * (1 - self.percentWithInitial)
        stopCondition = self.iteratorsNotImprove
        count = 0
        while self.bestSolution.totalDistance > stopValue  and count < stopCondition:
            terminationCriteriaStatus = False
            neighborsList = [self.createNeighbor(sample(range(self.quantityCustomer), k=2)) 
                                for i in range(self.quantityCustomer * self.sizeNeighbor)]
            terminationCriteriaStatus = self.mainTabu(neighborsList, tabus, terminationCriteriaStatus)                    
            if terminationCriteriaStatus == True:
                count = 0
            else:
                count += 1
            if self.lookSol:
                print(f"Current solution: {self.currentSolution}")
        if self.lookSol:
            print(f"Best solution: {self.bestSolution}")  


            























     