# Absolute path example
absolute_path = r"c:\User\Chris\Desktop\my_path.py"

# Relative path example
relative_path = "my_path.py"

print("Absolute Path:", absolute_path)
print("Relative Path:", relative_path)


import os
folder = "C:/Users/Chris/Desktop"
filename = "my_path.py"

path = os.path.join(folder, filename)
print("Full path:", path)
# This way python handles slashes (/ vs \) automatically.

import os
path = "my_path.py"

if os.path.exists(path):
  print("Yes, the file exists!")
else: 
  print("File not found.")

from pathlib import Path 

# Current working directory
print("Current directory:", Path.cwd())

# Create a path object
file = Path("myfile.txt")

# Check if it exists
print("File exists: ", file.exists())

# Combine paths
folder = Path("C:/Users/Chris/Desktop")
full_path = folder / "myfile.txt"
print("Full path:", full_path)

from pathlib import Path

#  Get parent folder of current file
print("Parent folder:", Path.cwd().parent)

# List all files in a directory
for file in Path.cwd().iterdir():
    print(file)