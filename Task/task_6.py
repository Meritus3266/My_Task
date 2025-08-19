print("*** UNILAG Admission Eligibility Checker (2025/2026) ***")
# Collecting user name
name = input("Enter your name: ")
# Age requirement
age = int(input("Enter your age: "))
# UTME requirement
utme_score = int(input("Enter your UTME score: "))
first_choice = input("Did you choose UNILAG as your first choice? (Yes/No): ").title()
# O'Level requirement
olevel_credits = int(input("How many credit passes did you have in one sitting? "))
english_pass = input("Did you pass English Language? (Yes/No): ").title()
math_pass = input("Did you pass Mathematics? (Yes/No): ").title()
# Post-UTME screening
post_utme_score = int(input("Enter your Post-UTME score (0-100): "))
# Step 5: Departmental cut-off (asking user)
dept_cutoff = int(input("Enter your Departmental cut-off mark (200 - 320): "))
# Conditions for considering the user admission
# must be at least 16
meets_age = age >= 16
# must be >= 200 and UNILAG as first choice
meets_utme = (utme_score >= 200) and (first_choice == "Yes")
# must be 5 credits including English & Math
meets_olevel = (olevel_credits >= 5) and (english_pass == "Yes") and (math_pass == "Yes")
# total score for admission = UTME + Post-UTME
total_score = utme_score + post_utme_score
meets_cutoff = total_score >= dept_cutoff
# Final decision
eligibility = meets_age and meets_utme and meets_olevel and meets_cutoff
# mapping true and false to statement for final result
result = {
    True: f"Congratulations {name} you have been offered admission to the course of your choice",
    False: f"Sorry, no admission yet"
}
print("\n=== Admission Status ===")
print(f"Status: {result[eligibility]}")