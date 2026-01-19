from pathlib import Path

workspace = Path("workspace_files")
workspace.mkdir(exist_ok=True)
file_path = workspace / "notes.txt"
print(file_path)

# # (A) Create or overwrite using 'w'
# f = open(file_path, "w", encoding="utf-8")
# f.write("This is the first line in notes.txt\n")
# f.close()

# f = open(file_path, "w", encoding="utf-8")
# f.write("Shopping List:\n")
# f.write(" - Rice\n")
# f.write(" - Beans\n")
# f.write(" - Garri\n")
# f.close()

# f = open(file_path, "a", encoding="utf-8")
# f.write(" - Groundnut oil\n")
# f.write(" - Maggi\n")
# f.close()

# # Read the whole file
# f = open(file_path, "r", encoding="utf-8")
# content = f.readlines()
# f.close()
# print(content)

# # Read as a list of lines
# f = open(file_path, "r", encoding="utf-8")
# lines = f.readlines()
# f.close()
# print("Lines list:", [line.rstrip() for line in lines])

# #iterate over lines (memory-friendly)
# f = open(file_path, "r", encoding="utf-8")
# for line in f:
#     print("->", line.rstrip())
# f.close()

# # Write safely
# with open(file_path, "w", encoding="utf-8") as f:
#     f.write("My Todo List:\n")
#     f.write(" - Revise Python file handling\n")
#     f.write(" - Practice error handling within a function")
#     f.write(" - Practice JSON & CSV\n")

#     # Append safely
# with open(file_path, "a", encoding="utf-8") as f:
#     f.write(" - Build a small project\n")


# Try to read a file that doesn't exist
try:
    with open(workspace / "missing_file.txt", "r") as f:
        content = f.read()
        print("File content:", content)
except FileNotFoundError:
     print("Oops! That file doesn't exist yet.")
     print("Let's create it first!")

       # Now create the file
     with open(workspace / "missing_file.txt", "w") as f:
        f.write("Now I exist!")
     print("File created successfully!")