# Task 5
# names and phone numbers in tuples
names = ("Samuel", "Seyi", "Seun")
phones = (7016723340, 8132457688, 8146739890)
# Create dictionary from tuples
contacts = dict(zip(names, phones))
# name input
search_name = input("Enter a name to find: ").capitalize()
# name number output
number = contacts.get(search_name, "Name not found")
print(number)



