

























student = {"name": "Ada","age": 20,"course": "Computer Science"}
print(student)
student_info = dict(name="John", age=25, course="Maths")
print(student_info)

evens_cube = {x: x**3 for x in range(1, 10) if x % 2 == 0}
print(evens_cube)

": 85, "John": 40, "Musa": 65}

# Filter students who passed (score >= 50)

passed_students = {name: score for name, score in students.items() if score >= 50}
print(passed_students)