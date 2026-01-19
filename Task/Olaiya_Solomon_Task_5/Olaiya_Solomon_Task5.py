Nig_dish = []
dish_1 = input("Enter your Nigerian dish: \n")
dish_2 = input("Enter your Nigerian dish: \n")
dish_3 = input("Enter your Nigerian dish: \n")

dishes_list = ('rice', 'beans', 'dodo')
dish_tuple = tuple(dishes_list)
print("\n".join(dish_tuple))

# Task 2
friends_input = input("Enter your 5 best friends name: \n").split()
friends = (friends_input)
friends_tuple = tuple(friends)
print(friends_tuple[::-1]) 

print("Enter your 5 Nigerian state:  ")
state_1 = input("Entre your first Nigerian state: ")
state_2 = input("Entre your seccond Nigerian state: ")
state_3 = input("Entre your third Nigerian state: ")
state_4 = input("Entre your fourth Nigerian state: ")
state_5 = input("Entre your fifth Nigerian state: ")
state_list = (state_1, state_2, state_3, state_4, state_5)
print(f"first state: {state_1} \n last state: {state_5}")
print("lagos" in state_list)
print(len(state_list))

user_input_1 = input('Please enter your first name: ')
user_input_2 = input('Please enter your Age: ')
user_input_3 = input('Please enter your color: ')
user_input_4 = input('Please enter your home town: ')
user_list = [user_input_1, user_input_2, user_input_3, user_input_4]
print(user_list)
user_list2 = tuple(user_list)
user_var = str(user_list2)
print("-----------------------")
print(f"First name: \t| {user_input_1}")
print(f"Age: \t\t| {user_input_2}")
print(f"color: \t\t| {user_input_3}")
print(f"home town: \t| {user_input_4}")

item_1 = input("Enter your first shopping list item: ")
item_2 = input("Enter your second shopping list item: ")
item_3 = input("Enter your third shopping list item: ")
item_list = [item_1, item_2, item_3,]
tuple = 
item_list.append [input("Enter your fourth shopping list item:" )]
item_list.append [input("Enter your fifth shopping list item: ")]
print(item_list.append)