import csv
from pathlib import Path

header = ["Name", "Age", "Phone", "Track"]

def save_participant(file_path, participant_dict):
    file = Path(file_path)
    with open(file, "a", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        
        if not file.exists() or file.stat().st_size == 0:
            writer.writeheader()
        
        writer.writerow(participant_dict)

# def save_participant(data, file_path):
#     file = Path(file_path)
#     file_exists = file.exists()

#     with open(file, mode="a", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=["Name", "Age", "Phone", "Track"])
        
#         if not file_exists:
#             writer.writeheader()
        
#         writer.writerow(data)


def load_participants(file_path):
    file = Path(file_path)
    if not file.exists():
        print("file does not exist")
    else:
        print(f"Loading participants from {file.name}")
        with open(file, mode="r", newline="", encoding="utf-8") as f:
            print(f.read())

