### Calculating distances
import math

def getDistance(customer1, customer2, metric='EUC_2D'):
    '''Return distance between two customers'''
    if metric == 'ATT':
        pass
    else:
        squared_dx = (customer1.coordinate[0] - customer2.coordinate[0])**2
        squared_dy = (customer1.coordinate[1] - customer2.coordinate[1])**2
        d = math.sqrt(squared_dx + squared_dy)

    return d