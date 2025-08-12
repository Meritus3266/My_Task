# Basic usage of input()
name = input("Enter your nmae: ")
print("Hello,", name)

# Convert input to integer
age = int(input("Enter your age:" ))
print(f"You will be {age + 1} years old next year.")

# Calculator using input 
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
sum_result = num1 + num2
print(f"The sum of {num1} and {num2} is {sum_result}.")

# step 1 Welcome to meritus restaurant
# step 2 enter your order
# step 3 show the order 
print("Welcome to meritus restaurant")
order = input("What do you want to order: ")
print(f"you {order} is ready")