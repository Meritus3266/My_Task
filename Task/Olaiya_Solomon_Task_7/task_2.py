# Task 2 
item_list = ["Rice", "Beans", "Yam", "Semo", "Garri"]
price = [2500, 2000, 3000, 1500, 1200]
supermart = {
    "Items": item_list,
    "Price": price
}
print("Welcome to Meritus Supermart.")
print("Check our available goods and price, then order per quantity")
print("\n")
print("--" * 16)
print("Available goods and there price")
print("--" * 16)
for itemm, pricee in zip(supermart["Items"], supermart["Price"]):
    print(f"{itemm:<10} {pricee:>10}")
print("--" * 16)
print("Enter your negotiated price below ")
user_price_1 = int(input("Enter your price for Rrice: "))
user_price_2 = int(input("Enter your price for Beans: "))
user_price_3 = int(input("Enter your price for Yam: "))
user_price_4 = int(input("Enter your price for Semo: "))
user_price_5 = int(input("Enter your price for Garri: "))
user_price = [user_price_1, user_price_2, user_price_3, user_price_4, user_price_5]
supermart.update({"Price": user_price})
print("--" * 16)
print((", ").join(supermart.keys()))
print("--" * 16)
print("Your goods and negotiated price")
print("--" * 16)
for itemm, pricee in zip(supermart["Items"], supermart["Price"]):
    print(f"{itemm:<10} {pricee:>10}")
print("--" * 16)