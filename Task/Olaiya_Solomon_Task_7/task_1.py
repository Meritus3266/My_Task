# collecting student bio data
data_1 = input("Please enter your name: ")
data_2 = input("Please enter your age: ")
data_3 = input("Please enter your gender: ")
data_4 = input("Please entre your three courses separated by space: ").title().split()
print(data_4)
# student bio data
student_data = {
    "name": data_1.title(),
    "age": data_2.title(),
    "gender": data_3.title(),
    "course": data_4
}
print("--------------------------------------------------------")
print("Your student bio-data")
print("--------------------------------------------------------")
print(f" Name: \t\t|\t {student_data['name']}\n Age: \t\t|\t {student_data['age']}\n Gender \t|\t {student_data['gender']}\n course: \t|\t {", ".join(student_data['course'])}")
print("--------------------------------------------------------")