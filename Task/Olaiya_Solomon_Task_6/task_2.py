# collecting names of people attending seminar
name1 = input("Enter name of attendee 1: ")
name2 = input("Enter name of attendee 2: ")
name3 = input("Enter name of attendee 3: ")
name4 = input("Enter name of attendee 4: ")
name5 = input("Enter name of attendee 5: ")
# set will remove any duplicates
attendees = {name1, name2, name3, name4, name5}
print("--" * 15)
print("Attendees in alphabetical order:")
print("--" * 15)
print("\n".join(sorted(attendees.capitalize())))
print("--" * 15)
