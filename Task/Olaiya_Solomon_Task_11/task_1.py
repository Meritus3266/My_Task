from pathlib import Path

participant = Path("participant_pkg")
participant.mkdir(exist_ok=True)
file_path_1 = participant / "__init__.py"
file_path_2 = participant / "file_ops.py"
file_path_3 = participant / "contact.csv"
f = open(file_path_3, "w", encoding="utf-8")
f.write(" newly created file\n")
f.close()
