### Customers class

class Customer():
    '''A class representing a customer'''

    def __init__(self, id, coordinate):
        self.id = id
        self.coordinate = (float(coordinate[0]), float(coordinate[1]))
        # self.coordinate = coordinate

    def __repr__(self):
        return f'Customer ID: {self.id}, Address: {self.coordinate}.'