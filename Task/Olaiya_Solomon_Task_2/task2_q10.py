
# Input statements
school_name = input("Enter school name: ")
tuition_fee = float(input("Enter tuition fee: "))
hostel_fee = float(input("Enter hostel fee: "))
feeding_fee = float(input("Enter feeding fee: "))

# Calculate total
total_fee = tuition_fee + hostel_fee + feeding_fee

# Receipt output
print("\nSchool Fees Receipt")
print("School Name: " + school_name)
print("Tuition Fee: ₦" + str(tuition_fee))
print("Hostel Fee: ₦" + str(hostel_fee))
print("Feeding Fee: ₦" + str(feeding_fee))
print("Total Fee: ₦" + str(total_fee))
