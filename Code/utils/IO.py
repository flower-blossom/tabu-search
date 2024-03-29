import numpy as np
import itertools, os, sys
from random import seed
path = os.getcwd()
parent = os.path.dirname(path)
sys.path.append(path)

from dataModels import Customer, DataModel, Cost, Solution
from utils import distances
from algorithms import Tabu, Greedy

def readTSPLib(filename,  **params):
    '''Return cost and dataModel in the specific filename'''
    node_data_filename = "/../data/" + filename

    with open(os.path.dirname(__file__) + node_data_filename) as f_obj:
        nodeData = f_obj.readlines()

    # Get keywords
    NAME = ''
    TYPE = ''
    COMMENT = ''
    DIMENSION = 0
    EdgeWeightType = ''
    EdgeWeightFormat = ''
    DisplayDataType = ''
    DisplayDataSectionIndex = 0
    EdgeWeightSectionIndex = 0
    NodeCoordSectionIndex = 0

    for i in range(len(nodeData)):
        node = nodeData[i].split()
        if ':' in node:
            node.remove(':')
        # print(node)
        if len(node) != 0:
            if 'NAME' in node[0]:
                NAME = node[1]
            if 'TYPE' in node[0]:
                TYPE = node[1]
            if 'COMMENT' in node[0]:
                for word in node[1:]:
                    COMMENT += word + ' '
                COMMENT = COMMENT[:-1]
            if 'DIMENSION' in node[0]:
                DIMENSION = int(node[1])
            if 'EDGE_WEIGHT_TYPE' in node[0]:
                EdgeWeightType = node[1]
            if 'EDGE_WEIGHT_FORMAT' in node[0]:
                EdgeWeightFormat = node[1]
            if 'DISPLAY_DATA_TYPE' in node[0]:
                DisplayDataType = node[1]
            if 'EDGE_WEIGHT_SECTION' in node[0]:
                EdgeWeightSectionIndex = i + 1
            if 'DISPLAY_DATA_SECTION' in node[0]:
                DisplayDataSectionIndex = i + 1
            if 'NODE_COORD_SECTION' in node[0]:
                NodeCoordSectionIndex = i + 1

    dataDescription = {'NAME': NAME, 'TYPE': TYPE, 'COMMENT': COMMENT, 'DIMENSION': DIMENSION}

    # Create a dict that contains data about the nodes (id, x, y)
    NodeCoordSection = {}

    nodeStartIndex = 0
    if EdgeWeightType in ['EUC_2D', 'EUC_3D', 'MAN_2D', 'MAN_3D', 'MAX_2D', 'MAX_3D', 'GEO', 'ATT', 'CEIL_2D']:
        nodeStartIndex = NodeCoordSectionIndex
    elif EdgeWeightType == 'EXPLICIT':
        nodeStartIndex = DisplayDataSectionIndex

    # Create a dict for customers
    customersDict = {}

    if nodeStartIndex:
        while 'EOF' not in nodeData[nodeStartIndex]:
            if ' ' in nodeData[nodeStartIndex]:
                customerData = nodeData[nodeStartIndex].split(' ')
            elif '\t' in nodeData[nodeStartIndex]:
                customerData = nodeData[nodeStartIndex].split('\t')
            customerData = [i for i in customerData if i != '' and i != '\n']
            customerData[-1] = customerData[-1][:-1]

            if EdgeWeightType == 'GEO':
                NodeCoordSection[customerData[0]] = {'lat': distances.getLatitude(float(customerData[1])), 
                                                    'lon': distances.getLatitude(float(customerData[2]))}
            else:
                NodeCoordSection[customerData[0]] = {'lat': float(customerData[1]), 'lon': float(customerData[2])}
            nodeStartIndex += 1

        for node in NodeCoordSection:
            customersDict[f'Customer {node}'] = Customer.Customer(node, NodeCoordSection[node])
    else:
        for i in range(1, 1 + DIMENSION):
            customersDict[f'Customer {i}'] = Customer.Customer(str(i), {'lat': 'na', 'lon': 'na'})


    # Create a numpy array for the distance matrix
    distancesMatrix = np.zeros((DIMENSION, DIMENSION))

    if EdgeWeightType == 'EXPLICIT':
        # a numpy array representing the distances matrix
        distancesMatrix = np.zeros((DIMENSION, DIMENSION))

        # List contains all distances data numbers in order
        distanceDataList = []

        # index of the first row of data
        distancesStartIndex = EdgeWeightSectionIndex
        
        # read the data into the distanceDataList
        while 'DISPLAY_DATA_SECTION' not in nodeData[distancesStartIndex] and 'EOF' not in nodeData[distancesStartIndex]:
            rowData = nodeData[distancesStartIndex].split(' ')
            rowData = [num for num in rowData if num != '' and num != '\n']
            distanceDataList += rowData
            distancesStartIndex += 1

        if EdgeWeightFormat == 'FULL_MATRIX':
            for i in range(DIMENSION):
                for j in range(i, DIMENSION):
                    distancesMatrix[i][j] = distanceDataList[i*DIMENSION + j]
                    distancesMatrix[j][i] = distancesMatrix[i][j]

        if EdgeWeightFormat == 'UPPER_ROW':
            dataCount = 0
            for i in range(DIMENSION):
                for j in range(DIMENSION - 1 - i):
                    distancesMatrix[i][j] = distanceDataList[dataCount]
                    dataCount += 1
            distancesMatrix = np.fliplr(distancesMatrix)
            for i, j in itertools.combinations_with_replacement(range(DIMENSION-1, -1, -1), 2):
                distancesMatrix[i][j] = distancesMatrix[j][i]

        if EdgeWeightFormat == 'LOWER_ROW':
            dataCount = 0
            for i in range(DIMENSION):
                for j in range(i):
                    distancesMatrix[i][j] = distanceDataList[dataCount]
                    dataCount += 1
            for i, j in itertools.combinations_with_replacement(range(DIMENSION), 2):
                distancesMatrix[i][j] = distancesMatrix[j][i]

        if EdgeWeightFormat == 'UPPER_DIAG_ROW':
            dataCount = 0
            for i in range(DIMENSION):
                for j in range(DIMENSION - 1 - i):
                    distancesMatrix[i][j] = distanceDataList[dataCount]
                    dataCount += 1
            distancesMatrix = np.fliplr(distancesMatrix)
            for i, j in itertools.combinations_with_replacement(range(DIMENSION-1, -1, -1), 2):
                distancesMatrix[i][j] = distancesMatrix[j][i]

        if EdgeWeightFormat == 'LOWER_DIAG_ROW':
            dataCount = 0
            for i in range(DIMENSION):
                for j in range(i+1):
                    distancesMatrix[i][j] = distanceDataList[dataCount]
                    dataCount += 1
            for i, j in itertools.combinations_with_replacement(range(DIMENSION), 2):
                distancesMatrix[i][j] = distancesMatrix[j][i]
    else:
        distancesMatrix = np.zeros((DIMENSION, DIMENSION))
        for i, j in itertools.product(range(DIMENSION), repeat = 2):
            distancesMatrix[i][j] = distances.getDistance(customersDict[f'Customer {i + 1}'], 
            customersDict[f'Customer {j + 1}'], EdgeWeightType)
    costs = Cost.Cost(distancesMatrix)
    dataModel = DataModel.DataModel(customersDict, dataDescription)
    return costs, dataModel
# test = [1, 14, 13 ,12 ,7, 6, 15, 5, 11, 9, 10, 16, 3, 2, 4, 8]
# a = readTSPLib("att48.tsp")[0]
a = readTSPLib("ulysses16.tsp")[0]
# test1 = Solution.Solution(test, a)
# seed(4)
b = Greedy.Greedy(a)
c = Tabu.Tabu_search(a)
c.solver()
# print(test1.totalLength)
print(c.best_solution.totalLength)
print(c.best_solution.solutionList)
print(b.totalLength)
print(b.solutionList)
