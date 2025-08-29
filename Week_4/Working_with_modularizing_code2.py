# #1. Import the whole module

# import math


# # Lets put it to use

# print(math.sqrt(9))
# # - Note that you must specify the module name when calling a function within it.

# 1. import as an alias

# import math as m

# # lets put it to use

# print(m.sqrt(25))

# # - This shortens the module name, this is common with libraries like numpy, pandas, etc

# 3. Import specific functions or variables

# from math import sqrt, pi

# print(sqrt(36))
# print(pi)

# # - here you dont need the prefix 'math.' anymore

# my_module/first.py

# def add(a, b):
#     return a + b


# def subtract(a, b):
#     return a - b


# def multiply(a, b):
#     return a * b


# def divide(a, b):
#     if b != 0:
#         return a / b
#     else:
#         return "Cannot divide by zero"
    
    
import first
import second

# lets use the functions in the first.py file
print("=== Math Functions ===")
print("5 + 3 =", first.add(5, 3))
print("10 - 4 =", first.subtract(10, 4))
print("6 * 7 =", first.multiply(6, 7))
print("20 / 5 =", first.divide(20, 5))


# Lets us the functions in the second.py file
print("\n=== String Functions ===")
print(second.greet("Ridwan"))
print("Reverse of 'Python' =", second.reverse_string("Python"))
print("Character count in sentence =", second.count_characters("Python modules are powerful"))
print("Word count in sentence =", second.count_words("Python modules are powerful"))
