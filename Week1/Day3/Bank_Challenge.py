class BankAccount():

    def __init__(self,owner,balance=0):
        self.owner=owner
        self.balance=balance
    
    def deposit(self,amt):
        self.balance+=amt
        return self.balance
    
    def withdraw(self,wd_amt):
        if self.balance >= wd_amt:
            self.balance -= wd_amt
            return f'Withdrawal Accepted: {self.balance}'
        else:
            return 'Funds Unavailable!'

my_money=BankAccount("Swara",2000)
print(my_money.deposit(1000))
print(my_money.withdraw(500))
print(my_money.withdraw(4000))
