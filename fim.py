import os
import hashlib
import json

FOLDER = "monitored_folder"
BASELINE = "baseline.json"


def calculate_hash(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def scan_folder():
    files = {}

    for root, directories, filenames in os.walk(FOLDER):
        for filename in filenames:

            filepath = os.path.join(root, filename)

            relative_path = os.path.relpath(filepath, FOLDER)

            files[relative_path] = calculate_hash(filepath)

    return files


def create_baseline():

    files = scan_folder()

    with open(BASELINE, "w") as file:
        json.dump(files, file, indent=4)

    print("\nBaseline created successfully!")
    print(f"{len(files)} files scanned.\n")


def check_integrity():

    if not os.path.exists(BASELINE):
        print("\nNo baseline found!")
        print("Please select option 1 first.\n")
        return

    with open(BASELINE, "r") as file:
        old_files = json.load(file)

    new_files = scan_folder()

    modified = []
    added = []
    deleted = []

    # Check for modified and added files
    for filepath in new_files:

        if filepath not in old_files:
            added.append(filepath)

        elif new_files[filepath] != old_files[filepath]:
            modified.append(filepath)

    # Check for deleted files
    for filepath in old_files:

        if filepath not in new_files:
            deleted.append(filepath)

    print("\n========== FILE INTEGRITY REPORT ==========")

    print("\nMODIFIED:")

    if modified:
        for file in modified:
            print("  ", file)
    else:
        print("   None")

    print("\nADDED:")

    if added:
        for file in added:
            print("  ", file)
    else:
        print("   None")

    print("\nDELETED:")

    if deleted:
        for file in deleted:
            print("  ", file)
    else:
        print("   None")

    print("\n============================================\n")


def main():

    while True:

        print("================================")
        print("      FILE INTEGRITY MONITOR")
        print("================================")
        print("1. Set Baseline")
        print("2. Scan for Changes")
        print("3. Exit")
        print("================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_baseline()

        elif choice == "2":
            check_integrity()

        elif choice == "3":
            print("\nExiting...")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.\n")


main()