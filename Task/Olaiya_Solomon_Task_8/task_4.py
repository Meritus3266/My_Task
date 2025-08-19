
student_record = {}
# collecting user informations
user_name = input("Enter your name: ")
user_age = int(input("Enter your age: "))
user_scores = [70, 85, 90, 92]
# updating the dictionary
student_record.update({"Name": user_name})
student_record.update({"Age": user_age})
student_record.update({"Scores":user_scores})
# calculating average score and updating the condition to the dictionary
Avg_score = (student_record["Scores"][0] + student_record["Scores"][1] + student_record["Scores"][2] + student_record["Scores"][3]) / 4
student_record["Passed"] = Avg_score >= 50
# teenager condition
teenager = (student_record["Age"] >= 13) and (student_record["Age"] <= 19)
# output
print(f"Student Record: \n Name: {student_record["Name"]}\n Age: {student_record["Age"]}\n Scores: {student_record["Scores"]}\n Passed: {student_record["Passed"]}\n Teenager: {teenager}")