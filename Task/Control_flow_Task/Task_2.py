names = []
scores = []
# collecting user names
for i in range(3):
    name= input(f"Enter name of the student {i+1}: ")
    score = int(input(f"Enter score for {name}: "))
    names.append(name)
    scores.append(score)
# output
print("\n STUDENT SCORES")
print("-" * 30)
print(f"Name: \t Score")
print("-" * 30)
for i in range(len(names)):
    print(f"{names[i]} \t {scores[i]}")