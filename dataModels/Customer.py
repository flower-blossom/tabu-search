### Customers class

class Customer():
    '''A class representing a customer'''

    def __init__(self, id, coordinate):
        self.id = id
        self.coordinate = coordinate

    def __repr__(self):
        return f'Customer ID: {self.id}, Latitude: {self.coordinate["lat"]}, Longitude: {self.coordinate["lon"]}.'