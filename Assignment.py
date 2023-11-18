import pymongo
import pandas as pd
from datetime import datetime


global user_input,con

class ATM:
    
    con = pymongo.MongoClient("mongodb://localhost:27017")
    
    def varify(self, username, passw):
        db = self.con['User_verification']
        dt = db['User_data']
        self.datas = list(dt.find({'Account_id':username,'Password':passw},{}))
        try:
            self.account_id = self.datas[0]['Account_id']
            return True 
        except:    
            return False
    
    def transaction_history(self):
        # db = con['User_verification']
        # dt = db['User_data']
        # datas = list(dt.find({'Account_id':self.account_id},{}))
        db = self.con['User_account_info']
        dt = db[str(self.account_id)]
        # dt.insert_one({'Date':str(datetime.now()),'Amount_Withdrawals':" ",'Amount_Deposit':20000,'Balance':20000}) 
        df = pd.DataFrame(list(dt.find({},{'_id':0})))
        print(df)
        
    
    def withdraw(self, amount):
        db = self.con['User_account_info']
        dt = db[str(self.account_id)]
        self.datas = list(dt.find().sort({'_id':-1}))
        self.datas = int(self.datas[0]['Balance'])
        if amount > self.datas:
            return "Can't widthdraw money because of insaficiant money in account "
        self.datas -= amount
        dt.insert_one({'Date':str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")),'Amount_Withdrawals':amount,'Amount_Deposit':"",'Balance':self.datas}) 
        return "Successfully withdraw"
    
    def deposit(self,amount):
        db = self.con['User_account_info']
        dt = db[str(self.account_id)]
        self.datas = list(dt.find().sort({'_id':-1}))
        self.datas = int(self.datas[0]['Balance'])
        self.datas += amount
        dt.insert_one({'Date':str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")),'Amount_Withdrawals':"",'Amount_Deposit':amount,'Balance':self.datas}) 
        return "Successfully deposit"
    
    
    def transfer(self,amount,other_account):
        db = self.con['User_account_info']
        dt = db[str(self.account_id)]
        self.datas = list(dt.find().sort({'_id':-1}))
        self.datas = int(self.datas[0]['Balance'])
        if amount > self.datas:
            return "Can't widthdraw money because of insaficiant money in account "
        self.datas -= amount
        dt.insert_one({'Date':str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")),'Amount_Withdrawals':amount,'Amount_Deposit':"",'Balance':self.datas}) 
        
        dt = db[other_account]
        self.datas = list(dt.find().sort({'_id':-1}))
        self.datas = int(self.datas[0]['Balance'])
        self.datas += amount
        dt.insert_one({'Date':str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")),'Amount_Withdrawals':"",'Amount_Deposit':amount,'Balance':self.datas}) 
        return "Tranfer Complete"


while True:
    user_id = input("Please enter User ID :- ")
    passw = input("Please enter Pin :- ")
    if user_id == "Example" and passw == "123":
        break
    else:
        s1 = ATM()
        if s1.varify(user_id,passw):
            print("Access Accepted")
            break
        else:
            print("User ID or Pin is incorrent please try again.")        

while True:
    print("\n1. TRANSACTIONS HISTORY\n2. WITHDRAW\n3. DEPOSIT\n4. TRANSFER\n5. QUIT")
    try:
        user_input = int(input("Enter your choice number :- "))
        if user_input not in range(1,6):
            raise Exception
    except:
        print("Please enter number from given list and try again.")
        continue
    if user_input == 5:
        break
    elif user_input == 1:
        s1.transaction_history()
    elif user_input == 2:
        user_id = int(input("Enter amount :- "))
        print(s1.withdraw(user_id))
    elif user_input == 3:
        user_id = int(input("Enter amount :- "))
        s1.deposit(user_id)
    elif user_input == 4:
        user_id = int(input("Enter amount :- "))
        passw = input("Enter account id :- ")
        print(s1.transfer(user_id, passw))

exit()