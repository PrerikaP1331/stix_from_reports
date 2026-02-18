import os

EXCLUDE_DIRS = {"venv", "__pycache__", ".git"}
EXCLUDE_FILES = {".DS_Store"}

def print_tree(start_path=".", indent=""):
    items = sorted(os.listdir(start_path))

    # Filter unwanted files/folders
    items = [
        item for item in items
        if item not in EXCLUDE_DIRS
        and item not in EXCLUDE_FILES
        and not item.startswith(".")
    ]

    for index, item in enumerate(items):
        path = os.path.join(start_path, item)
        is_last = index == len(items) - 1

        connector = "└── " if is_last else "├── "
        print(indent + connector + item)

        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            print_tree(path, indent + extension)


if __name__ == "__main__":
    print("\nProject Structure:\n")
    print_tree()
