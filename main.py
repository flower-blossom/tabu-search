from algorithms import Greedy, Tabu
from utils import IO
from dataModels.IsFeasible import IsFeasible
import numpy as np
file = 'bays29'
# dataModel = IO.readTSPLib(f'{file}.tsp')
# optSolution = IO.readOPTLib(f'{file}.opt.tour', dataModel)
# print(f"optSolution: {optSolution.totalDistance}")
# print(IsFeasible(optSolution, dataModel).checkSolution())
# tabuSolution = Tabu.Tabu(dataModel, pwi=0.4, sizeNeighbor=4, sizeTabus=0.5)
# tabuSolution.solve()
# print(f"bestSolution: {tabuSolution.bestSolution.totalDistance}")
# print(f"initialSolution: {tabuSolution.firstSolution.totalDistance}")
# print(IsFeasible(tabuSolution.bestSolution, dataModel).checkSolution())

def writeStatistical(arr, file):
    for i in arr:
        for j in i:
            file.write(f"{j} ")
        file.write("\n")

files = ['berlin52', 'gr96', 'st70']
# for file in files:
#     dataModel = IO.readTSPLib(f'{file}.tsp')
#     optSolution = IO.readOPTLib(f'{file}.opt.tour', dataModel)
#     statisticalFile = open(f'statistical_{file}.txt','w')
#     statistical = []
#     for sizeTabus in np.arange(0.2, 1, 0.1):
#         for sizeNeighbor in range(2, 9, 1):
#             total = []
#             total.append(round(sizeTabus, 2))
#             total.append(sizeNeighbor)
#             compareToInitial = []
#             compareToOpt = []
#             for i in range(100):
#                 tabuSolution = Tabu.Tabu(dataModel, pwi=0.5, sizeNeighbor=sizeNeighbor, sizeTabus=sizeTabus)
#                 tabuSolution.solve()
#                 efficiency = tabuSolution.firstSolution.totalDistance/optSolution.totalDistance
#                 efficiency2 = tabuSolution.bestSolution.totalDistance/optSolution.totalDistance
#                 compareToInitial.append(efficiency)
#                 compareToOpt.append(efficiency2)
#             total.append(round(sum(compareToInitial)/len(compareToInitial)*100, 2))
#             total.append(round(sum(compareToOpt)/len(compareToOpt)*100, 2))
#             statistical.append(total)
#     writeStatistical(statistical, statisticalFile)

def readTxt(file):
    # matrix = np.loadtxt(file, delimiter = ' ', dtype = 'str')
    with open( file) as f_obj:
        dataTxt = f_obj.readlines()
    # print(dataTxt)
    data = []
    for line in dataTxt:
        matrix = line.strip("\n").split(" ")
        matrix = [float(i) for i in matrix if i != '']
        data.append(matrix)
    return data

a = readTxt('statistical_bays29.txt')
print(a)