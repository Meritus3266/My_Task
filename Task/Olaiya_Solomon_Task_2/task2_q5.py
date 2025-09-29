# Input statements
market_name = input("Enter market name: ")
traders = int(input("Enter number of traders: "))
revenue = float(input("Enter daily revenue in naira: "))

# Output with f-string
print(f"The {market_name} market has {traders:,} traders and makes ₦{revenue:,} daily.")
