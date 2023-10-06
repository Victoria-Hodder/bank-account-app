""" 
Logic for different account types 

Account (parent class)
    --> open_account()
    --> delete_account()

CurrentAccount (child, inherits from Account)
    --> account_type = 'current'
    --> inherit methods from Account (for opening/deleting)
SavingsAccount (child, inherits from Account)
    --> account_type = 'savings'
    --> inherit methods from Account (for opening/deleting)

Where would I put the logic for checking the account type ('current'/'savings')?

"""

class Accounts:
    
    def open_account():
        return "Welcome! You opened a new account"
    
    def close_account():
        return "You closed your account. Thank you for using V's banking."