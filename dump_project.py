import os

EXCLUDE_DIRS = {"venv", "__pycache__", ".git"}
EXCLUDE_EXTENSIONS = {".pyc", ".exe", ".dll"}
INCLUDE_EXTENSIONS = {".py", ".json", ".md", ".txt"}

OUTPUT_FILE = "project_dump.txt"


def should_include_file(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in INCLUDE_EXTENSIONS


def is_binary(filepath):
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
            return b"\0" in chunk
    except:
        return True


def write_tree(start_path, file):
    file.write("PROJECT STRUCTURE\n")
    file.write("=" * 80 + "\n\n")

    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]

        level = root.replace(start_path, "").count(os.sep)
        indent = "│   " * level
        folder_name = os.path.basename(root)

        file.write(f"{indent}📁 {folder_name}\n")

        subindent = "│   " * (level + 1)
        for f_name in files:
            if f_name.startswith("."):
                continue
            file.write(f"{subindent}📄 {f_name}\n")

    file.write("\n\n")


def write_files(start_path, file):
    file.write("FILE CONTENTS\n")
    file.write("=" * 80 + "\n\n")

    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]

        for filename in files:
            if filename.startswith("."):
                continue

            filepath = os.path.join(root, filename)

            if not should_include_file(filename):
                continue

            if is_binary(filepath):
                continue

            file.write("\n" + "=" * 80 + "\n")
            file.write(f"FILE: {filepath}\n")
            file.write("=" * 80 + "\n\n")

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    file.write(content)
                    file.write("\n")
            except Exception as e:
                file.write(f"[Error reading file: {e}]\n")


def main():
    project_root = "."
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        write_tree(project_root, out)
        write_files(project_root, out)

    print(f"\nProject dump written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

