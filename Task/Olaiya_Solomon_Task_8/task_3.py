items = ["Pen", "Pod", "Notepad", "Eraser", "Bulb", "hoe", "set", ]
items_price = [1000, 1000, 100, 100, 500, 300, 300, 100, 100]
# our initioal total before order
cart_total = 0
# taking first 4 items as example for order
cart_total += items_price[0]
cart_total += items_price[1]
cart_total += items_price[2]
cart_total += items_price[3]
# Print items and total
print(f"Items: {items[:4]}")
print(f"Total Price: ₦{cart_total}")