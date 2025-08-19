# creating dictionary
store = {"Book": 10, "Pen": 20, "Bag": 5, "Pencil": 12, "Eraser": 9, "Shoe": 4, "math set": 8, "graph book": 7, "card board": 3}
# storing the initial dictionary before ammeded
before_order = store.copy()
# collecting user order
order = input("Which item will you like to buy: ").capitalize()
# order quantity
order_quant = int(input(f"How many {order} do you want: "))
# removing the order quantity from the dictionary
store[order] -= order_quant
# making a copy of the removed order in case there's another order
after_order = store.copy()
# output
print(before_order)
print(after_order)