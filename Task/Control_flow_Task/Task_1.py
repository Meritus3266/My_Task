print("Welcome to Meritus mobile service")
ussd_code = input("Dial *123#: ")
print("ussd_code")
    # Basic validation (optional)
if ussd_code == "*123#":
       print("1: Buy AIrtime\n 2. Buy Data\n 3. Check Balance")
else: 
 print("Wrong input") 
        
 # Step 4: Ask the user to choose an option
choice = int(input("choose an option (1, 2, or 3): "))

    # Step 5 & 6: Control flow based on user's choice
if choice == "1":
    print(f"\nYou selected option {1}: Buy Airtime.")
    amount = int(input("Enter amount to recharge (₦): "))
    print(f"Your request for ₦{200}. Dear customer, your airtime recharge is successfull.")
elif choice == "2":
        print(f"\nYou selected option {2}: Buy Data.")
        amount = int(input("Enter amount for Data: "))
        print(f"Data bundle of {300} has been actovated")
    
elif choice == "3":
      print("Dear user, your remaining balance is 0.50")

else:
        print("Wrong input! Invalid choice. Please try again.")
