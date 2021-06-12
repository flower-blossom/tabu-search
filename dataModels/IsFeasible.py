class IsFeasible():
    '''A class check the solution '''
    def __init__(self, solution, dataModel):
        self.solution = solution.solutionList
        self.dataDescription = dataModel.dataDescription

    def checkSolution(self):
        quantityCustomer = self.dataDescription["DIMENSION"]
        checkCustomers = [False for i in range(quantityCustomer)]
        for customer in self.solution:
            if checkCustomers[customer - 1] == True:
                return False
            else:
                checkCustomers[customer - 1] = True
        if False in checkCustomers:
            return False 
        return True