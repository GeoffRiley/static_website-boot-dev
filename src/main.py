import os
import shutil

from makesite import copy_directory_contents, generate_pages_recursive

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_directory_contents("static", "public")

    generate_pages_recursive("content", "template.html", "public")


main()

