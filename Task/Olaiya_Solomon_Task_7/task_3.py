# Task 3
seats = set(range(1, 51))
# user one booking
print("Available seats:", seats)
user1 = int(input("Enter the seat number you want to book: "))
seats.remove(user1)
print("Remaining seats:", seats)
# Second booking
user2 = int(input("Enter the seat number you want to book: "))
seats.remove(user2)
print("Remaining seats:", seats)
# Third booking
user3 = int(input("Enter the seat number you want to book: "))
seats.remove(user3)
print("Remaining seats:", seats)