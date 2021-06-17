class Solution():
    '''
    A class that contains the solution list 
    '''
    def __init__(self, solution, dataModel):
        self.solution = solution
        self.distancesMatrix = dataModel.distancesMatrix
        self.totalDistance = self.getTotalLength()

    def __repr__(self):
        return str(self.solution)

    def getTotalLength(self):
        '''
        Total distance of the current solution path.
        '''
        length = 0
        # add distances from the first node to the last node
        for i in range(len(self.solution)-1):
            currentCustomerIndex = int(self.solution[i] - 1)
            nextCustomerIndex = int(self.solution[i+1] - 1)
            length += self.distancesMatrix[currentCustomerIndex][nextCustomerIndex]

        # add distance from the last node to the first node
        length += self.distancesMatrix[self.solution[0] - 1][self.solution[-1] - 1]
        return length