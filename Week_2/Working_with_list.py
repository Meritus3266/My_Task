# # Method 1: Using square brackets
# empty_list2 = []
# print(empty_list)     # output: []

# # Method 2: using the list() constructor
# empty_list2 = list()
# print(empty_list2)  # Output: []

# # List of integers 
# numbers = [1, 2, 3, 4, 5]
# print(numbers)  # Output: [1, 2, 3, 4, 5]

# #List of strings
# fruits = ["apple, banana, cherry"]
# print(fruits)  # output: ['apple', 'banana', 'cherry']

# # mixed data types
# mixed_list = ["Alice", 25, 5.8, True]
# print(mixed_list) # output: ['Alice, 25, 5.8, True]

# # From a string (each character becomes an element)
# chars = list("Hello")
# print(chars)   #output: ['h', 'e', 'l', 'l', 'o']

# #suares of numbers 0-4
# squares = [x**2 for x in range(5)]
# print(squares)  # Output: [0, 4, 9, 16]

# # Even numbers between 0-10
# evens = [x for x in range (11) if x % 2 == 0]
# print(evens)  # output: [0, 2, 4, 6, 8, 10]

# # Matrix-like list
# matrix = [[1,2], [3,4], [5,6]]
# print(matrix)  # Output: [[1,2], [3,4], [5,6]]

# # Accessing elements in a nested list
# print(matrix[0])  # output: [1, 2]
# print(matrix[0][1])  # output:  2

# fruit = ["mango", "orange", "banana"]
# print(fruit)         # ['mango', 'orange', 'banana']
# print(fruit[0])      # mango     (First element)
# print(fruit[2])      # banana   (Third element)

# items = ["rice", "beans", "yam", "rice"]
# numbers = [1, 2, 3]
# numbers[1] = 20  #  changing element at index 1
# print(numbers)   #  [1, 20, 3]

# mixed = [10, "Nigeria", 3.14, True]
# print(mixed)  #  [10, 'Nigeria', 3.14, True]

# nested_list = [[1, 2], ["a", "b"]]
# print(nested_list)   #   [[1, 2], ['a', 'b']]
# print(nested_list[0][1])   #    2

# names = ["Ada"]
# names.append("Bola")
# names.append("chidi")
# print(names)   #   ['Ada','Bola', 'chidi']

# fruits = ["apple", "banana", "cherry"]
# print(fruits[1])

# numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# print(numbers[::3])

colours = ["Red", "Green", "Blue"]
print("yellow" in colours)