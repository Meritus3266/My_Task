# a = 10
# b = 20
# print(a == b)   
# print(a != b)
# print(a >= 10) 
# print(b <= 25)


# score = 75

# print(score >= 50)  # True (Passed)
# print(score < 50)   # False (Failed)
# print(score == 100)

# x = 10
# print("Initial value:", x)

# x += 5
# print("After x += 5:", x)

# x -= 2
# print("After x -= 2:", x)

# x=10
# x *= 3
# print("After x *= 3:", x)

# x=10
# x /= 4
# print("After x /= 4:", x)

# x=10
# x %= 3
# print("After x %= 3:", x)


# x = 4
# x **= 2
# print("After x **= 2:", x)

# x=10
# x //= 3
# print("After x //= 3:", x)

# x=4
# x **= 3
# print("After x **= 3: ", x)

# x=15
# x /= 4
# print("After x /= 4: ", x)

# x=15
# x //= 4
# print("After x //= 4: ", x)

# balance = 1000
# deposit = 200
# withdraw = 150


# balance += deposit   # Add deposit
# balance -= withdraw  # Subtract withdrawal

# print("Updated Balance:", balance) 


# #Define variables
# age = 17
# score = 85


# # Must be younger than 18 AND score above 80
# qualified = (age > 18) and (score > 80)

# print("Scholarship Eligible:", not qualified)
 
# Use case example2 - Event Access
age = 22
has_ticket = False

can_enter = (age >= 18) and (has_ticket or age < 25)

print("Access Granted:", can_enter)  