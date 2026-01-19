# class NigerianStudent:
#     def __init__(self, name, state):  # This runs automatically
#         print(f"Step 1: Creating student object...")
#         self.name = name           # Step 2: Assign name to THIS object
#         self.state_of_origin = state    # Step 3: Assign state to THIS object
#         print(f"Step 6: {self.name} from {self.state_of_origin} is ready!")

#     # When you create an object, here's what happens:
# ayo = NigerianStudent("Ayo Daniel", "Lagos")
# saed = NigerianStudent("saed", "Lagos")
# print(ayo.name)
# print(saed.name) 
       
# class PhoneUser:
#     def __init__(self, name, network):
#         self.name = name
#         self.network = network
#         self.airtime = 0
#         print(f"{self.name} joined {self.network} network")
    
#     def buy_airtime(self, amount):
#         self.airtime += amount  # self ensures it goes to the RIGHT person
#         print(f"{self.name} now has ₦{self.airtime} airtime")

# # Creating multiple users
# abeeb = PhoneUser("Abeeb Bakare", "MTN")     
# onisemo = PhoneUser("Onisemo Williams", "Airtel")  

# # Each person's actions affect only their own account
# print(abeeb.buy_airtime(500))     # Tunde now has ₦500 airtime
# print(onisemo.buy_airtime(1000)) # Blessing now has ₦1000 airtime
# print(abeeb.airtime)              # 500 (Tunde's airtime unchanged)
# print(onisemo.airtime)           # 1000 (Blessing's airtime unchanged)

# class Student0:
#       university = "Federal University of Technology Akure"
# def __init__(self, name, course):
#         self.name = name         
#         self.course = course
# Student1 = Student0
# Student2 = Student0("Federal University of Technology Akure")
# print(Student0.university)     
# print(student1.name)   
# print(student2.university)

# class Student:
#     def __init__(self, name, course, level):
#         # Attributes
#         self.name = name
#         self.course = course
#         self.level = level
#         self.cgpa = 0.0
#         self.fees_paid = False
    

#      # Method: action the student can do
#     def pay_school_fees(self):                   
#         self.fees_paid = True
#         return f"{self.name} has paid school fees for {self.level} level"
    
#     # Method: another action
#     def register_courses(self):                   
#         if self.fees_paid:
#             return f"{self.name} has registered courses for {self.course}"
#         else:
#             return f"{self.name} must pay school fees first!"
    
#       # Method: calculates CGPA
#     def calculate_cgpa(self, grades):           
#         if grades:
#             self.cgpa = sum(grades) / len(grades)
#             return f"{self.name}'s CGPA is now {self.cgpa:.2f}"
#         return "No grades provided"
    
#     # Using methods
# Abiodun = Student("Abiodun Akinola", "Gistology", 600)
# print(Abiodun.pay_school_fees())        
# print(Abiodun.register_courses())       
# print(Abiodun.calculate_cgpa([4.2, 3.8, 4.0, 3.5]))




# class Student: 
#     def __init__(self, name, course, level):

#         self.name = name
#         self.course = course
#         self. level = level
#         self.tax_paid = False

#     def pay_school_tax(self):
#         self.tax_paid = True
#         return f"{self.name} has paid school tax for {self.level} level"
#     def register_courses(self):
#        if self.tax_paid:
#           return f"{self.name} has registered courses for {self.course} level"
#        else:
#           return f"{self.name} must pay the school fees first!"
       
# jide = Student("jide olaiya", "English", "400")
# print(jide.pay_school_tax())
# print(jide.register_courses())


# class Student:
#     university = "Federal University of Technology Akure"  
    
#     def __init__(self, name, course):
#         self.name = name         
#         self.course = course

# student1 = Student("Anthony Johnson", "Engineering")
# student2 = Student("Fadilat Hassan", "Medicine")

# print(student1.name)  
# print(student2.name)
# print(Student.university)     
# print(student1.university)   
# print(student2.university) 

# class BankAccount:
#     def __init__(self, owner, bank_name, balance=0):
#         self.owner = owner
#         self.bank_name = bank_name
#         self.balance = balance
#         self.account_number = self.generate_account_number()

#     def deposit(self, amount):
#         """"Add money to the account"""
#         if amount > 0:
#             self.balance += amount
#             return f"\u20A6{amount:,} deposited to {self.owner}'s {self.bank_name} account. New balance: \u20A6{self.balance:,}"
#         return "Invalid deposit amount"
    
#     def withdraw(self,amount):
#         """Remove money from the account"""  
#         if amount > 0 and amount <= self.balance:
#             self.balance -= amount
#             return f"\u20A6{amount:,} withdrawn from {self.owner}'s account. New balance: \u20A6{self.balance:,}"
#         return "insufficient funds or invalid amount"
    
#     def transfer(self, amount, recipient):
#         """Transfer money to another account"""
#         if amount > 0 and amount <= self.balance:
#             self.balance -= amount
#             return f"\u20A6{amount} Transfered from {self.owner} to {recipient} account. Remaining balance: \u20A6{self.balance}"
#         return "Transfer failed: Insufficient funds"
    
#     def check_balance(self):
#         """check balance"""
#         return f"{self.owner}'s {self.bank_name} account balance: \u20A6{self.balance:,}"
    
#     def generate_account_number(self):
#         """"Generate account number"""
#         import random 
#         return f"01{random.randint(10000000, 99999999)}"
    
# jide_account = BankAccount("Jide Olaiya", "Gt Bank", 10000)

# print(f"Owner: {jide_account.owner}")
# print(f"Bank: {jide_account.bank_name}")
# print(f"Account Number: {jide_account.account_number}")

# print(jide_account.deposit(100000))
# print(jide_account.withdraw(10000))
# print(jide_account.transfer(15000, "Olaiya Maryline"))
# print(jide_account.check_balance)

class NaijaPhone:
    def __init__(self, brand_name, model, network_provider):
        self.brand_name = brand_name
        self.model = model
        self.network_provider = network_provider
        self.airtime_balance = 0
        self.data_balance = 0 
        self.is_on = False

    def power_on(self):
        self.is_on = True
        return f"{self.brand_name} Phone is on. Network: {self.network_provider}"
    
    def buy_airtime(self, amount):
        self.airtime_balance += amount
        return f"\u20A6{amount} airtime purchased. Balance: \u20A6{self.airtime_balance}"
    def make_call(self, number):
        if self.is_on and self.airtime_balance > 0:
            self.airtime_balance -= 10
            return f"Calling {number}... Remaining airtime: \u20A6{self.airtime_balance}" 
        return "Cannot make call. check phone power or airtime"
 
    def send_sms(self, message, number):
        if self.is_on and self.airtime_balance > 0:
            self.airtime_balance -= 5
            return f"SMS sent to {number}: '{message}. remaining airtime: \u20A6{self.airtime_balance}"
        return "Insufficient airtime to send SMS"
    
    def buy_data(self, amount):
        self.data_balance += amount
        return f"{amount} data purchased. Balance: {self.data_balance}"
    
    def data_usage(self):
        if self.is_on and self.data_balance > 0:
            self.data_balance -= 15
            return f"Remaining Data: {self.data_balance}"
        return "Oops you do not have an active data plan to use the internet"

Samsung_phone = NaijaPhone("SAMSUNG", "ULTRA20", "MTN")

print(f"brand_name: {Samsung_phone.brand_name}")
print(f"Model: {Samsung_phone.model}")
print(f"Network: {Samsung_phone.network_provider}")

print(Samsung_phone.power_on())
print(Samsung_phone.buy_airtime(100))
print(Samsung_phone.make_call("09065725764"))
print(Samsung_phone.send_sms('soccer is the game',"09065725764" ))
print(Samsung_phone.buy_data(50))
print(Samsung_phone.data_usage())

class NigerianBankAccount:
    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self._balance = initial_balance        # Protected attribute
        self.__pin = "1234"                   # Private attribute
        self._transaction_history = []        # Protected attribute
    
    # Public methods - anyone can use these
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self._transaction_history.append(f"Deposited ₦{amount:,}")
            return f"₦{amount:,} deposited successfully"
        return "Invalid deposit amount"
    
    def withdraw(self, amount, pin):
        if self.__verify_pin(pin):  # Uses private method
            if amount <= self._balance:
                self._balance -= amount
                self._transaction_history.append(f"Withdrew ₦{amount:,}")
                return f"₦{amount:,} withdrawn successfully"
            return "Insufficient funds"
        return "Invalid PIN"
    
    def check_balance(self, pin):
        if self.__verify_pin(pin):
            return f"Current balance: ₦{self._balance:,}"
        return "Invalid PIN"
    
           # Private method - only the class can use this
    def __verify_pin(self, entered_pin):
        return entered_pin == self.__pin
    
           # Protected method - subclasses can use this
    def _get_transaction_history(self):

ibrahim_account = NigerianBankAccount("Ibrahim Orekunrin", 50000)

           # These work - public interface
print(ibrahim_account.deposit(10000))      # ₦10,000 deposited successfully
print(ibrahim_account.withdraw(5000, "1234"))  # ₦5,000 withdrawn successfully
print(ibrahim_account.check_balance("1234"))   # Current balance: ₦55,000