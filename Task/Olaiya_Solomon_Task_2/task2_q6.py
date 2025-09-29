# Input statements
name = input("Enter customer's full name: ")
units = int(input("Enter units consumed (kWh): "))
cost_per_unit = float(input("Enter cost per unit (₦): "))

# Calculating total bill
total_bill = units * cost_per_unit

# output
print("Electricity Bill Receipt\n")
print("Customer Name: " + name)
print("Units Consumed: " + str(units) + " kWh")
print("Cost per Unit: ₦" + str(cost_per_unit))
print("Total Bill: ₦" + str(total_bill))
