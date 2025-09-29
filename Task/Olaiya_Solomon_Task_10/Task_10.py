# Simulated USSD Menu Interaction
print("Welcome to the Naija Mobile service")

# conditioning
code = ""
balance = 5000    

# Dial code validation
while code != "*123#":
    code = input("Kindly dial code *123# for interaction: ")

print("\nMenu:")
print(" 1: Check Balance\n 2. Buy Airtime\n 3. Buy Data")

choice = input("Enter your choice: ").strip()

# Selection conditions
if choice == "1":
    print("\nYou selected: Check Balance")
    print(f"Your airtime balance is ₦{balance:,} ")

elif choice == "2":
    print("\nYou selected: Buy Airtime")
    try:
        recharge = int(input("Enter the amount to recharge: "))
        if recharge <= 0:
            print("Invalid amount. Please enter a positive number.")
        elif recharge > balance:
            print("Insufficient fund! You cannot recharge more than your balance.")
        else:
            balance -= recharge
            print(f"You have successfully recharged ₦{recharge:,}")
            print("Your Account balance is ₦", balance)
    except ValueError:
        print("Invalid input. Please enter numbers only!")

elif choice == "3":
    print("\nYou selected: Buy Data")
    data_dictionary = {
        "sn": [1, 2, 3, 4, 5],
        "data": ["100kb", "500kb", "1gb", "3gb", "5gb"],
        "amount": [200, 600, 1500, 3500, 5500]
    }
    
    # Display data bundles
    print(f"\n{'SN'}\t{'Data'}\t{'Amount(₦)'}")
    print("-" * 30)
    for i in range(len(data_dictionary["sn"])):
        print(f"{data_dictionary['sn'][i]}\t{data_dictionary['data'][i]}\t₦{data_dictionary['amount'][i]:,}")
    
    try:
        data_recharge = int(input("Select option from (1 - 5): "))
        if data_recharge in data_dictionary["sn"]:
            index = data_recharge - 1
            if data_dictionary["amount"][index] > balance:
                print("Insufficient fund, kindly recharge.")
            else:
                print(f"\nYou have successfully purchased {data_dictionary['data'][index]} "
                      f"for ₦{data_dictionary['amount'][index]:,}.")
                balance -= data_dictionary["amount"][index]
                print("Your Account balance is ₦", balance)
                print("Thanks for using Naija Mobile Service.")
        else:
            print("Invalid selection! Please try again with numbers between 1 and 5.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")

else:
    print("You have entered an invalid number, please try again.")