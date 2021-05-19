import numpy as np
import itertools, os, sys

# get current directory
path = os.getcwd()
parent = os.path.dirname(path)

sys.path.append(path)
from dataModels import Customer, DataModel, Cost
from algorithms import Greedy
from utils import distances

def getDataModel(filename,  **params):
    '''Return a dataModel in the specific filename'''
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

    dataDescription = {'name': NAME, 'type': TYPE, 'comment': COMMENT, 'dimension': DIMENSION}

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
        while nodeData[nodeStartIndex] != 'EOF\n':
            if ' ' in nodeData[nodeStartIndex]:
                customerData = nodeData[nodeStartIndex].split(' ')
            elif '\t' in nodeData[nodeStartIndex]:
                customerData = nodeData[nodeStartIndex].split('\t')
            customerData = [i for i in customerData if i != '' and i != '\n']
            customerData[-1] = customerData[-1][:-1]

            # if EdgeWeightType in ['EUC_3D', 'MAN_3D', 'MAX_3D']:
            #     NodeCoordSection[customerData[0]] = (float(customerData[1]), float(customerData[2]), float(customerData[3]))
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
        # print('len distanceDataList: ', len(distanceDataList))

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
    dataModel = DataModel.DataModel(customersDict, distancesMatrix, dataDescription)
    return costs, dataModel


test = getDataModel('bayg29.tsp')
solver = Greedy.greedy(test[1])
print(solver)
























# Tests
# print(NAME)
# print(TYPE)
# print(COMMENT)
# print(DIMENSION)
# print(EdgeWeightType)
# print(NodeCoordSectionIndex)
# print(NodeCoordSection)
# print(customersDict)
# print(distancesMatrix)
# print(EdgeWeightFormat)
# print(DisplayDataSectionIndex)