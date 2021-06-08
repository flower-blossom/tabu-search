# addNode(), ...

a = 1

class Solution():
    '''
    A class that contains the solution list and the dataModel
    '''
    def __init__(self, solutionList, cost):
        self.solutionList = solutionList
        self.cost = cost
        self.totalLength = self.totalLength()

    def __repr__(self):
        return str(self.solutionList)
 
    def insertCustomer(self, customerIdx, cost, pos=-1):
        '''
        Insert a customer to the solutionList, default position is the end of the solutionList
        '''
        d = 0
        if pos != -1:
            self.solutionList.insert(pos, customerIdx)

            d += cost.distancesMatrix[self.solutionList[pos-1]][customerIdx]
            d += cost.distancesMatrix[customerIdx][self.solutionList[pos+1]]
            d -= cost.distancesMatrix[self.solutionList[pos-1]][self.solutionList[pos+1]]
        else:
            self.solutionList.append(customerIdx)

            d += cost.distancesMatrix[self.solutionList[-2]][customerIdx]
            d += cost.distancesMatrix[customerIdx][self.solutionList[0]]
            d -= cost.distancesMatrix[self.solutionList[-2]][self.solutionList[0]]

        self.totalLength += d

    def deleteCustomer(self, cost, pos=-1):
        '''
        Delete a customer from the solutionList, default position is the end of the solutionList
        '''
        d = 0
        if pos != -1:
            deletedCustomerIdx = self.solutionList.pop(pos)
            d -= cost.distancesMatrix[self.solutionList[pos-1]][deletedCustomerIdx]
            d -= cost.distancesMatrix[deletedCustomerIdx][self.solutionList[pos]]
            d += cost.distancesMatrix[self.solutionList[pos-1]][self.solutionList[pos]]
        else:
            deletedCustomerIdx = self.solutionList.pop()
            d -= cost.distancesMatrix[self.solutionList[-1]][deletedCustomerIdx]
            d -= cost.distancesMatrix[deletedCustomerIdx][self.solutionList[0]]
            d += cost.distancesMatrix[self.solutionList[-1]][self.solutionList[0]]

        self.totalLength += d

    def totalLength(self):
        '''
        Total distance of the current solution path.
        '''
        length = 0

        # add distances from the first node to the last node
        for i in range(len(self.solutionList)-1):
            currentCustomerIndex = int(self.solutionList[i] - 1)
            nextCustomerIndex = int(self.solutionList[i+1] - 1)
            length += self.cost.distancesMatrix[currentCustomerIndex][nextCustomerIndex]

        # add distance from the last node to the first node
        length += self.cost.distancesMatrix[self.solutionList[0] - 1][self.solutionList[-1] - 1]
        
        return length

# list_ = [1, 2, 3]
# dataModel_ = [1, 2]
# s1 = Solution(list_, dataModel_)
# print(s1.totalLength)
# s1.increase(a)
# print(s1.totalLength)