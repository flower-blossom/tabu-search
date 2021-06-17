class IsFeasible():
    '''A class check the solution '''
    def __init__(self, solution, dataModel):
        self.solution = solution.solution
        self.quantityCustomer = dataModel.dataDescription["DIMENSION"]

    def checkSolution(self):
        if self.quantityCustomer != len(self.solution):
            return False 
        checkCustomers = [False for i in range(self.quantityCustomer)]
        for customer in self.solution:
            if checkCustomers[customer - 1] == True:
                return False
            else:
                checkCustomers[customer - 1] = True
        if False in checkCustomers:
            return False 
        return True