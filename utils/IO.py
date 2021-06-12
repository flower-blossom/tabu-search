import numpy as np
import itertools, os

from dataModels.Solution import Solution
from utils import distances


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

def readOPTLib(filename,  **params):
    node_data_filename = "/../data/" + filename

    with open(os.path.dirname(__file__) + node_data_filename) as f_obj:
        nodeData = f_obj.readlines()

    indexFirstCustomer = 0
    indexLastCustomer = 0
    optSolution = []
    
    for line in nodeData:
        if 'TOUR_SECTION' in line:
            indexFirstCustomer = nodeData.index(line) + 1
            break
    
    for index in range(len(nodeData) - 1, 0, -1):
        if '-1' in nodeData[index]:
            indexLastCustomer = index - 1
            break

    # Find optSolution
    if nodeData[indexFirstCustomer] == nodeData[indexLastCustomer]:
        optSolution = nodeData[indexFirstCustomer].strip("\n").split(" ")
    else:
        if len(nodeData[indexFirstCustomer]) == 2:
            for line in nodeData[indexFirstCustomer : indexLastCustomer + 1]:
                optSolution.append(line.strip("\n"))
        elif len(nodeData[indexFirstCustomer]) > 2:
            for line in nodeData[indexFirstCustomer : indexLastCustomer + 1]:
                customerInLine = line.strip("\n").split(" ")
                customerInLine = [i for i in customerInLine if i != '']
                optSolution.extend(customerInLine) 

    optSolution = [int(i) for i in optSolution]
    print(optSolution)
    return Solution(optSolution)
