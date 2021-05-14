### Calculating distances
import math

def getDistance(customer1, customer2, edgeWeightType):
    '''Return distance between two customers'''
    d = 0
    if edgeWeightType == 'EUC_2D':
        squared_dx = (getDX(customer1, customer2))**2
        squared_dy = (getDY(customer1, customer2))**2
        d = math.sqrt(squared_dx + squared_dy)
    elif edgeWeightType == 'EUC_3D':
        squared_dx = (getDX(customer1, customer2)**2)
        squared_dy = (getDY(customer1, customer2)**2)
        squared_dz = (getDZ(customer1, customer2)**2)
        d = math.sqrt(squared_dx + squared_dy + squared_dz)
    elif edgeWeightType == 'MAN_2D':
        dx = abs(getDX(customer1, customer2))
        dy = abs(getDY(customer1, customer2))
        d = round(dx + dy)
    elif edgeWeightType == 'MAN_3D':
        dx = abs(getDX(customer1, customer2))
        dy = abs(getDY(customer1, customer2))
        dz = abs(getDZ(customer1, customer2))
        d = round(dx + dy + dz)
    elif edgeWeightType == 'MAX_2D':
        dx = abs(getDX(customer1, customer2))
        dy = abs(getDY(customer1, customer2))
        d = max(round(dx), round(dy))
    elif edgeWeightType == 'MAX_3D':
        dx = abs(getDX(customer1, customer2))
        dy = abs(getDY(customer1, customer2))
        dz = abs(getDZ(customer1, customer2))
        d = max(round(dx), round(dy) + round(dz))
    elif edgeWeightType == 'GEO':
        latitude1, longitude1 = getLatitude(customer1), getLongitude(customer1)
        latitude2, longitude2 = getLatitude(customer2), getLongitude(customer2)

        rrr = 6378.388
        q1 = math.cos(longitude1 - longitude2)
        q2 = math.cos(latitude1 - latitude2)
        q3 = math.cos(latitude1 + latitude2)
        d = int(rrr * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0 )
    elif edgeWeightType == 'ATT':
        dx = getDX(customer1, customer2)
        dy = getDY(customer1, customer2)
        r = math.sqrt((dx**2 + dy**2) / 10.0)
        t = round(r)
        if t < r:
            d = t + 1
        else:
            d = t
    elif edgeWeightType == 'CEIL_2D':
        d = math.ceil(getDistance(customer1, customer2, 'EUC_2D'))
    return d

def getDX(customer1, customer2):
    '''Return x-distance of two customers'''
    return customer1.coordinate[0] - customer2.coordinate[0]

def getDY(customer1, customer2):
    '''Return y-distance of two customers'''
    return customer1.coordinate[1] - customer2.coordinate[1]

def getDZ(customer1, customer2):
    '''Return z-distance of two customers'''
    return customer1.coordinate[2] - customer2.coordinate[2]

def getLatitude(customer):
    '''Return converted-latitude of the customer'''
    pi = 3.141592
    deg = round(customer.coordinate[0])
    min = customer.coordinate[0] - deg
    latitude = pi * (deg + 5.0 * min / 3.0) / 180.0
    return latitude

def getLongitude(customer):
    '''Return converted-longitude of the customer'''
    pi = 3.141592
    deg = round(customer.coordinate[0])
    min = customer.coordinate[1] - deg
    longitude = pi * (deg + 5.0 * min / 3.0) / 180.0
    return longitude