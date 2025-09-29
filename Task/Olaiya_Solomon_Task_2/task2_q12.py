# 1. Welcome screen
print("Welcome to Naija Mobile Service!")

# 2. Dial USSD code
ussd_code = input("Please dial a USSD code (e.g., *123#): ")

# 3. Display menu 
print("\nMenu:\n1. Check Balance\n2. Buy Airtime\n3. Buy Data")

# 4. Choose an option
choice = input("Enter your choice (1, 2, or 3): ")

# 5. Display confirmation message
print("You selected option " + choice)

# 6. Amount
amount = float(input("Enter amount: "))

# 7. Final transaction summary
print(f"Transaction complete. You selected option {choice} with amount ₦{amount:.2f}")
