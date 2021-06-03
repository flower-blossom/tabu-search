class Solution():
    '''A class storage the solution list and the dataModel'''
    def __init__(self, solutionList, dataModel):
        self.solutionList = solutionList
        self.dataModel = dataModel
    
    def __repr__(self):
        return str(self.solutionList)
    def totalLength(self):
        '''Total distance of the current solution path.'''
        length = 0
        # add distances from the first node to the last node
        for i in range(len(self.solutionList)-1):
            currentCustomerIndex = int(self.solutionList[i] - 1)
            nextCustomerIndex = int(self.solutionList[i+1] - 1)
            length += self.dataModel.distancesMatrix[currentCustomerIndex][nextCustomerIndex]
        # add distance from the last node to the first node
        length += self.dataModel.distancesMatrix[self.solutionList[0] - 1][self.solutionList[-1] - 1]
        return length