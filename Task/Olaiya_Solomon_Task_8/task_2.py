# name = input("Enter your name: ") # collecting the user name
# age = int(input("Enter your age: ")) # collecting the user age
# score = int(input("Enter your test score: ")) # collecting the user score 

# eligibility = (age < 18) and (score > 70)
# print(f"Candidate: {name}\nAge: {age}\nScore: {score}\nEligible: {eligibility}")

# Eligibility status
print("Federal Government Scholarship Key Eligibility Requirement")
user_name = input("Kindly enter your name: ").capitalize()
user_citz = input("Are you a citizen of Nigeria: ").capitalize()
user_inst = input("Are you a registered fulltime undergraduate: ").capitalize()
user_ships = input("Are you currently receiving any other scholarship from an entity in the Oil and Gas industry, whether national or international: ").capitalize()
user_academy = input("Did you have five distinctions (As and Bs) in your WAEC/WASSCE including English and Mathemetics: ").capitalize()

eligibility = (user_citz == "Yes") and (user_inst == "Yes") and (user_ships == "No") and (user_academy == "Yes")
result = {True: "Congretulations you are eligible for the scholarship" , False: "Sorry you are not eligible for the scholaship"}
print(f"{user_name}, {result[eligibility]}")