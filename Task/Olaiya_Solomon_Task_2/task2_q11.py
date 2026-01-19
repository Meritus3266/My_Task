# Input statements
naira = float(input("Enter amount in Naira: "))
usd_rate = float(input("Enter exchange rate to US Dollars: "))
gbp_rate = float(input("Enter exchange rate to British Pounds: "))

# Calculations
usd = naira / usd_rate
gbp = naira / gbp_rate

# Output in table-like format
print("\nCurrency Conversion Result")
print("--------------------------------------------")
print("Currency\t\t|\tAmount")
print("--------------------------------------------")
print(f"Naira (₦)\t\t|\t₦{naira:,.2f}")
print(f"US Dollar ($)\t\t|\t${usd:,.2f}")
print(f"British Pound (£)\t|\t£{gbp:,.2f}")
print("--------------------------------------------")
