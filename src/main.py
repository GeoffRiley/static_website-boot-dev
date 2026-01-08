import os
import shutil

from makesite import copy_directory_contents, generate_pages_recursive

def main(base_path):
    if os.path.exists("docs"):
        shutil.rmtree("docs")

    copy_directory_contents("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", base_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"

    main(base_path)

