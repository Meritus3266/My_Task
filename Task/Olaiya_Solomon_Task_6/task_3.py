
# weekdays tuple
weekdays = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
# user 3 days input
print("Choose any three days of the week you have activity ")
day1 = input("Enter your first day: ").capitalize()
day2 = input("Enter your second day: ").capitalize()
day3 = input("Enter your third day: ").capitalize()
# user 3 days activity
print("Enter your activity for three specific days.")
day_1_act = input(f"What is your activity for {day1}: ")
day_2_act = input(f"What is your activity for {day2}: ")
day_3_act = input(f"What is your activity for {day3}: ")
day_list = [day1, day2, day3]
act_list = [day_1_act, day_2_act, day_3_act]
# dictionary
week_plan = { day: activity for day, activity in zip(day_list, act_list)}
print("\nYour full weekly activity schedule:")