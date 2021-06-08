def checkSolution(solution, quantity_customers):
    checkCustomer = [False for i in range(quantity_customers)]
    for customer in solution:
        if checkCustomer[customer - 1] == False:
            checkCustomer[customer - 1] = True
        else:
            return False
    if False not in checkCustomer:
        return True


