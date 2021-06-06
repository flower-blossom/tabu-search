from random import randrange, sample
from itertools import combinations
# from dataModels import Solution

import os, sys

# get current directory
path = os.getcwd()
parent = os.path.dirname(path)
sys.path.append(parent)

from dataModels import Solution
from algorithms import Greedy

class Tabu_search():
    def __init__(self, cost):
        self.distance_matrix = cost.distancesMatrix
        self.cost = cost
        self.best_solution = None
        self.current_solution = None


    def initial_solution(self):
        solution = Greedy.Greedy(self.cost)
        return solution

    # def distance_varies_by_neighbor(self, cus1, cus2):
    #     index_cus1 = self.best_solution.index(cus1)
    #     index_cus2 = self.best_solution.index(cus2)
    #     cus_before_cus1 = self.best_solution[index_cus1 - 1]
    #     cus_after_cus1 = self.best_solution[index_cus1 + 1]
    #     cus_before_cus2 = self.best_solution[index_cus2 - 1]
    #     cus_after_cus1 = self.best_solution[index_cus2 + 1]
    #     distance_before_change = (self.distance_matrix[cus1, cus_before_cus1] 
    #                            +  self.distance_matrix[cus1, cus_after_cus1]
    #                            +  self.distance_matrix[cus2, cus_before_cus2]
    #                            +  self.distance_matrix[cus2, cus_after_cus1])

    #     distance_after_change =  (self.distance_matrix[cus2, cus_before_cus1] 
    #                            +  self.distance_matrix[cus2, cus_after_cus1]
    #                            +  self.distance_matrix[cus1, cus_before_cus2]
    #                            +  self.distance_matrix[cus1, cus_after_cus1])
    #     total_change = distance_after_change - distance_before_change 
    #     return total_change

    # def choosing_best_neighbor_change(self, neighbors_list):
    #     min_total_change_distance = distance_varies_by_neighbor(neighbors_list[0][0], 
    #                                                             neighbors_list[0][1])
    #     current_neighbor = neighbors_list[0]
    #     for neighbor in neighbors_list:
    #         change_distance = distance_varies_by_neighbor(neighbor[0], neighbor[1])
    #         if change_distance < min_total_change_distance:
    #             min_total_change_distance = change_distance
    #             current_neighbor = neighbor
    #     return min_total_change_distance, current_neighbor      

    # def check_aspiration(self, distance_varies_neighbor_solution):
    #     if distance_varies_neighbor_solution + current_total_distance < best_total_distance:
    #         return True
    #     return False
    # def check_aspiration(self, best_neighbor_solution):
    #     if best_neighbor_solution.totalLength < self.best_total_distance:
    #         return True
    #     return False

    def choose_best_neighbor(self, neighbors_list):
        best_solution = neighbors_list[0]
        best_distance = neighbors_list[0].totalLength
        for neighbor in neighbors_list:
            if neighbor.totalLength < best_distance:
                best_solution = neighbor
                best_distance = neighbor.totalLength
        return best_solution

    def create_solution_neighbor(self, best_neighbor_change):
        neighbor_solution = self.current_solution.solutionList.copy()
        index_change_1 = best_neighbor_change[0]
        index_change_2 = best_neighbor_change[1]
        neighbor_solution[index_change_1], neighbor_solution[index_change_2] = neighbor_solution[index_change_2], neighbor_solution[index_change_1]                                                                       
        return Solution.Solution(neighbor_solution, self.cost)

    def check_tabus(self, best_neighbor_solution, tabus):
        for index_tabu in tabus:
            if best_neighbor_solution.solutionList[index_tabu] == self.current_solution.solutionList[index_tabu]:
                return True
            else:
                return False
    
    def compare_to_current_sol(self, solution):
        if solution.totalLength < self.current_solution.totalLength:
            return True
        else: 
            return False
    
    def compare_to_best_sol(self, solution):
        if solution.totalLength < self.best_solution.totalLength:
            return True
        else: 
            return False

    def main_tabu(self, neighbors_list, tabus, termination_criteria_status):
        best_neighbor_solution = self.choose_best_neighbor(neighbors_list)
        neighbors_list.pop(neighbors_list.index(best_neighbor_solution))
        if self.check_tabus(best_neighbor_solution, tabus) == False:
            if self.compare_to_best_sol(best_neighbor_solution):
                self.best_solution = best_neighbor_solution
                self.current_solution = best_neighbor_solution
                termination_criteria_status == True
                return best_neighbor_solution, termination_criteria_status
            else:
                self.current_solution = best_neighbor_solution
                termination_criteria_status == False
                return best_neighbor_solution, termination_criteria_status
        else:
            if self.compare_to_current_sol(best_neighbor_solution):
                if self.compare_to_best_sol(best_neighbor_solution):
                    self.best_solution = best_neighbor_solution
                    self.current_solution = best_neighbor_solution
                    termination_criteria_status == True
                    return best_neighbor_solution, termination_criteria_status
                else:
                    self.current_solution = best_neighbor_solution
                    termination_criteria_status == False
                    return best_neighbor_solution, termination_criteria_status
            else:
                if neighbors_list:
                    return self.main_tabu(neighbors_list, tabus, termination_criteria_status)
                else:
                    self.current_solution = best_neighbor_solution
                    termination_criteria_status == False
                    return best_neighbor_solution, termination_criteria_status
        # return best_neighbor_solution, termination_criteria_status

    def update_tabus(self, tabus, best_neighbor_solution):
        for index in range(len(self.distance_matrix)):
            if best_neighbor_solution.solutionList[index] != self.current_solution.solutionList[index]:
                if len(tabus) == 5:
                    tabus.pop(0)
                    tabus.append(index)
                else:
                    tabus.append(index)
                break

    def solver(self):
        tabus = []
        self.best_solution = self.initial_solution()
        self.current_solution = self.best_solution
        termination_criteria = 100
        count = 0
        # neighbors_list = [self.create_solution_neighbor(sample(range(0, len(self.distance_matrix)), k=2)) for i in range(1000)]
        # for i in neighbors_list:
        #     print(i.totalLength)
        # while count < termination_criteria:
        while self.best_solution.totalLength > 12000:
            termination_criteria_status = False
            neighbors_list = [self.create_solution_neighbor(sample(range(0, len(self.distance_matrix)), k=2)) for i in range(100)]
            best_neighbor_solution, termination_criteria_status = self.main_tabu(neighbors_list, tabus, termination_criteria_status)
            self.update_tabus(tabus, best_neighbor_solution)
            if termination_criteria_status == True:
                count = 0
            else:
                count += 1


            