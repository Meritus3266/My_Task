# # Tuple with multiple items
# fruits = ("apple", "banana", "cherry")
# print(fruits)

# # Without parentheses (tuple packing)
# numbers = 1, 2, 3,
# print(numbers)#

# # single-item tuple (must include a comma)
# single_item = ("apple")
# print(single_item)
# print(type(single_item))

# # Using the tuple() constructor
# fruits_list = ["apple", "banana", "cherry"]
# fruits_tuple = tuple(fruits_list)
# print(fruits_tuple)

# # Ordered
# colors = ("Red", "Green", "Blue")
# print(colors[0])

# # immutable(uncomment and run. This will cause an error)
# colors[1] = "yellow"

# Allow duplicates
# numbers = (1, 2, 2, 3,)
# print(numbers)

# # mixed data types
# mixed = ("apple", 3, True, 5.6)
# print(mixed)

# # Nested tuples
# nested = (("a, b"), (1, 2))
# print(nested)

# # indexing
# fruits = ("apple", "banana", "cherry")
# print(fruits[1])
# print(fruits[-1])

# # Slicing
# print(fruits[0:2])
# print(fruits[::-1])

# # concatenation
# tuple1 = (1,2)
# tuple2 = (3,4)
# result = tuple1 + tuple2
# print(result)

# # repition
# nums = (1,2)
# print(nums * 3)

# # Membership
# fruits = ("apple", "banana", "cherry")
# print("banana" in fruits)
# print("grape" not in fruits)

# # Iteration
# for fruit in fruits:
# print(fruit)

# dot count()   dot index()
numbers = (1 ,2, 2 ,3 ,4)
print(numbers.count(2))
print(numbers.index(3))

# Tuple to list
t= (1, 2, 3)
Ist = list(t)
Ist.append(4)
print(Ist)

# List back to tuple
t = tuple(Ist)
print(t)

# Built-in Functions with tuples
nums = (4, 1, 7, 3)
print(len(nums))
print(max(nums))
print(min(nums))
print(sum(nums))